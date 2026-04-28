import os
import re
import json
import time
import math
import yaml
import feedparser
import requests
import pandas as pd
import yfinance as yf

from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

STATE_FILE = DATA_DIR / "state.json"
REPORT_FILE = DATA_DIR / "seah_daily_report.md"
HISTORY_FILE = DATA_DIR / "seah_daily_history.csv"


def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def fred_csv(series_id: str) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    df = pd.read_csv(url)
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().sort_values("date")


def pct_change_latest(df: pd.DataFrame, periods: int) -> float | None:
    if len(df) <= periods:
        return None
    latest = df["value"].iloc[-1]
    prev = df["value"].iloc[-1 - periods]
    if prev == 0 or pd.isna(prev):
        return None
    return latest / prev - 1


def score_pipe_price_proxy(cfg):
    """
    무료 OCTG 가격 proxy.
    실제 OCTG spot price는 Argus/PipeLogix 등 유료 데이터가 더 정확함.
    """
    series = cfg["fred_series"]["carbon_pipe_ppi"]
    df = fred_csv(series)

    latest = float(df["value"].iloc[-1])
    latest_date = df["date"].iloc[-1].date().isoformat()

    mom_1m = pct_change_latest(df, 1)
    mom_3m = pct_change_latest(df, 3)
    mom_6m = pct_change_latest(df, 6)

    score = 0.0
    if mom_1m is not None and mom_1m > 0:
        score += 0.35
    if mom_3m is not None and mom_3m > 0.015:
        score += 0.40
    if mom_6m is not None and mom_6m > 0.03:
        score += 0.25

    return {
        "name": "미국 Pipe/OCTG 가격 proxy",
        "score": round(score, 3),
        "latest": latest,
        "latest_date": latest_date,
        "mom_1m": mom_1m,
        "mom_3m": mom_3m,
        "mom_6m": mom_6m,
        "comment": "FRED/BLS carbon steel pipe PPI 기준. OCTG 직접 가격은 아님."
    }


def google_news(query: str, days: int = 14, lang="en-US", country="US") -> list[dict]:
    url = (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query)}&hl={lang}&gl={country}&ceid={country}:en"
    )
    feed = feedparser.parse(url)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    items = []
    for entry in feed.entries:
        published = None
        if getattr(entry, "published_parsed", None):
            published = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)
        if published and published < cutoff:
            continue

        items.append({
            "title": re.sub("<.*?>", "", entry.get("title", "")),
            "summary": re.sub("<.*?>", "", entry.get("summary", "")),
            "link": entry.get("link", ""),
            "published": published.isoformat() if published else None
        })
    return items


def keyword_news_score(queries, positive_keywords, negative_keywords, days=14):
    all_items = []
    for q in queries:
        try:
            all_items.extend(google_news(q, days=days))
        except Exception:
            pass

    # 중복 제거
    seen = set()
    unique = []
    for item in all_items:
        key = item["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    pos_count = 0
    neg_count = 0

    for item in unique:
        text = (item["title"] + " " + item["summary"]).lower()
        if any(k.lower() in text for k in positive_keywords):
            pos_count += 1
        if any(k.lower() in text for k in negative_keywords):
            neg_count += 1

    raw = pos_count - neg_count

    if raw >= 5:
        score = 1.0
    elif raw >= 3:
        score = 0.75
    elif raw >= 1:
        score = 0.50
    elif raw == 0:
        score = 0.25
    else:
        score = 0.0

    return score, unique[:10], pos_count, neg_count


def parse_rig_count_from_news(state):
    """
    Baker Hughes 공식 최신표를 완전 자동 파싱하기 어렵거나 레이아웃이 바뀔 수 있어
    Google News RSS에서 'U.S. rig count rose/fell to N' 형태를 보조적으로 추출.
    첫 실행에서는 점수가 보수적으로 나올 수 있음.
    """
    items = google_news("Baker Hughes U.S. rig count oil gas rigs", days=10)
    text_blob = " ".join([x["title"] + " " + x["summary"] for x in items])

    patterns = [
        r"(?:rig count|total rig count).*?(?:rose|rises|increased|up).*?(?:to|at)\s+(\d{3,4})",
        r"(?:rig count|total rig count).*?(?:fell|falls|declined|down).*?(?:to|at)\s+(\d{3,4})",
        r"U\.S\..*?rig count.*?(?:to|at)\s+(\d{3,4})",
    ]

    latest = None
    for p in patterns:
        m = re.search(p, text_blob, flags=re.IGNORECASE)
        if m:
            latest = int(m.group(1))
            break

    prev = state.get("last_us_rig_count")

    if latest is None:
        return {
            "name": "미국 Rig Count proxy",
            "score": 0.25,
            "latest": None,
            "previous": prev,
            "comment": "자동 숫자 추출 실패. Baker Hughes 원자료 확인 권장."
        }

    state["last_us_rig_count"] = latest

    if prev is None:
        score = 0.50
    else:
        change = latest - int(prev)
        if change >= 10:
            score = 1.0
        elif change >= 3:
            score = 0.75
        elif change >= 0:
            score = 0.50
        elif change > -5:
            score = 0.25
        else:
            score = 0.0

    return {
        "name": "미국 Rig Count proxy",
        "score": score,
        "latest": latest,
        "previous": prev,
        "comment": "Baker Hughes rig count 뉴스에서 숫자 추출. 수동 검증 권장."
    }


def get_stock_signal(ticker: str):
    df = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
    if df.empty:
        return {
            "price": None,
            "volume": None,
            "volume_ratio_20d": None,
            "near_52w_high": None,
            "breakout_score": 0.0,
        }

    # yfinance 최신버전은 MultiIndex 반환 → squeeze()로 Series 변환
    close_col  = df["Close"].squeeze()
    volume_col = df["Volume"].squeeze()
    close  = float(close_col.iloc[-1])
    volume = float(volume_col.iloc[-1])
    avg20  = float(volume_col.tail(20).mean())
    high52 = float(close_col.max())

    volume_ratio = volume / avg20 if avg20 > 0 else None
    near_high = close >= high52 * 0.98

    score = 0.0
    if near_high:
        score += 0.5
    if volume_ratio and volume_ratio >= 2.0:
        score += 0.5
    elif volume_ratio and volume_ratio >= 1.5:
        score += 0.3

    return {
        "price": close,
        "volume": volume,
        "volume_ratio_20d": volume_ratio,
        "near_52w_high": near_high,
        "breakout_score": round(score, 3),
    }


def determine_cycle_stage(cycle_signals: dict) -> dict:
    """
    비EPS 업황 지표들의 평균 점수로 에너지 강관 사이클 단계를 자동 판단.
    매일 아침 신호 → 사이클 → EPS 시나리오를 자동 결정.

    사이클 단계 기준:
        avg ≥ 0.70 → 슈퍼사이클  EPS 70,000원 (2022~23년 수준 재현)
        avg ≥ 0.55 → 강세        EPS 55,000원 (강한 CAPEX 사이클)
        avg ≥ 0.40 → 기본회복    EPS 45,000원 (북미 OCTG+해외법인 개선)
        avg ≥ 0.25 → 약한회복    EPS 35,000원 (부분 회복)
        avg  < 0.25→ 저점        EPS 25,000원 (사이클 미반영)
    """
    EPS_MAP = [
        (0.70, "슈퍼사이클", 70000),
        (0.55, "강세",       55000),
        (0.40, "기본회복",   45000),
        (0.25, "약한회복",   35000),
        (0.00, "저점",       25000),
    ]

    scores = [v.get("score", 0.0) for v in cycle_signals.values()]
    avg = sum(scores) / len(scores) if scores else 0.0

    label, eps = "저점", 25000
    for threshold, lbl, e in EPS_MAP:
        if avg >= threshold:
            label, eps = lbl, e
            break

    return {
        "label":           label,
        "eps":             eps,
        "avg_cycle_score": round(avg, 3),
        "signal_count":    len(scores),
    }


def score_forward_eps(stock_price: float | None, cycle: dict) -> dict:
    """
    determine_cycle_stage() 결과를 받아 Forward PER 채점.
    EPS는 사이클 자동 판단값 사용 — config.yaml 수동 입력 불필요.
    """
    forecast_eps = cycle["eps"]
    cycle_label  = cycle["label"]
    avg_score    = cycle["avg_cycle_score"]

    if not stock_price or forecast_eps <= 0:
        return {
            "name": "Forward PER (사이클 자동판단)",
            "score": 0.0,
            "forward_per": None,
            "forecast_eps": forecast_eps,
            "cycle_label": cycle_label,
            "comment": "주가 없음."
        }

    fwd_per = stock_price / forecast_eps

    # 사이클주 PER 기준: 4~8배 정상, 5배 이하 = 강한 진입 시그널
    if fwd_per <= 5.0:
        score = 1.0
    elif fwd_per <= 6.5:
        score = 0.75
    elif fwd_per <= 8.0:
        score = 0.50
    elif fwd_per <= 10.0:
        score = 0.25
    else:
        score = 0.0

    # 전체 시나리오 맵 (현재가 기준 자동 계산, 텔레그램 출력용)
    scen_str = "  ".join(
        f"{lbl}={round(stock_price/e, 1)}x"
        for _, lbl, e in [
            (0, "저점",    25000),
            (0, "약한",    35000),
            (0, "기본",    45000),
            (0, "강세",    55000),
            (0, "슈퍼",    70000),
        ]
    )

    return {
        "name": "Forward PER (사이클 자동판단)",
        "score": score,
        "forward_per": round(fwd_per, 1),
        "forecast_eps": forecast_eps,
        "cycle_label": cycle_label,
        "avg_cycle_score": avg_score,
        "scenarios": scen_str,
        "comment": (
            f"[{cycle_label}] 업황점수 {avg_score:.2f} → EPS {forecast_eps:,}원 자동선택 "
            f"→ PER {round(fwd_per,1)}배"
        )
    }


def score_us_proxy_stocks(cfg):
    """
    미국 에너지·강관 업황 proxy 주가 모멘텀 채점.
    DNOW, TS, BKR, HAL, SLB, HP, PTEN 1개월 수익률 기준.
    """
    tickers = {
        "DNOW": "PVF 유통 proxy",
        "TS":   "OCTG·라인파이프 peer",
        "BKR":  "LNG·가스 인프라",
        "HAL":  "북미 유정 서비스",
        "SLB":  "글로벌 E&P CAPEX",
        "HP":   "미국 육상 rig",
        "PTEN": "drilling/completion",
    }

    results = {}
    returns = []

    for ticker, desc in tickers.items():
        try:
            df = yf.download(ticker, period="3mo", auto_adjust=True, progress=False)
            if df.empty:
                results[ticker] = {"return_1m": None, "desc": desc}
                continue
            close = df["Close"].squeeze()
            latest   = float(close.iloc[-1])
            month_ago = float(close.iloc[-21]) if len(close) >= 21 else float(close.iloc[0])
            ret = (latest / month_ago) - 1
            results[ticker] = {"return_1m": round(ret, 4), "price": round(latest, 2), "desc": desc}
            returns.append(ret)
        except Exception:
            results[ticker] = {"return_1m": None, "desc": desc}

    if not returns:
        score = 0.25
    else:
        pos_ratio = sum(1 for r in returns if r > 0) / len(returns)
        avg_ret   = sum(returns) / len(returns)
        if pos_ratio >= 0.71 and avg_ret > 0.03:
            score = 1.0
        elif pos_ratio >= 0.57:
            score = 0.75
        elif pos_ratio >= 0.43:
            score = 0.50
        elif pos_ratio >= 0.29:
            score = 0.25
        else:
            score = 0.0

    pos_cnt = sum(1 for r in returns if r > 0)
    ticker_lines = ", ".join(
        f"{t}:{v['return_1m']:+.1%}" if v["return_1m"] is not None else f"{t}:N/A"
        for t, v in results.items()
    )

    return {
        "name": "미국 에너지·강관 proxy 주가",
        "score": score,
        "positive_count": pos_cnt,
        "total_count": len(returns),
        "ticker_returns": ticker_lines,
        "comment": f"DNOW·TS·BKR·HAL·SLB·HP·PTEN 1M 수익률. {pos_cnt}/{len(returns)} 상승."
    }


def weighted_score(signals, weights):
    total = 0.0
    detail = {}

    for key, sig in signals.items():
        w = weights.get(key, 0)
        s = sig.get("score", 0.0)
        total += w * s
        detail[key] = {
            "weight": w,
            "score_0_1": s,
            "weighted": round(w * s, 2)
        }

    return round(total, 1), detail


def rating(total_score):
    if total_score >= 75:
        return "강세 확인: 추세추종 보유/추가 검토"
    if total_score >= 60:
        return "우호적: 보유 우위, 돌파·거래량 확인"
    if total_score >= 45:
        return "중립: 모멘텀 확인 필요"
    return "약세: 테마 약화 또는 실적 확인 전"


def append_history(score_total, stock):
    today = datetime.now().strftime("%Y-%m-%d")
    row = {
        "date": today,
        "score": score_total,
        "price": stock.get("price"),
        "volume_ratio_20d": stock.get("volume_ratio_20d"),
        "near_52w_high": stock.get("near_52w_high"),
    }
    if HISTORY_FILE.exists():
        hist = pd.read_csv(HISTORY_FILE)
        # 오늘 날짜 중복 방지
        hist = hist[hist["date"] != today]
        hist = pd.concat([hist, pd.DataFrame([row])], ignore_index=True)
    else:
        hist = pd.DataFrame([row])
    hist.to_csv(HISTORY_FILE, index=False)


def build_report(cfg, signals, score_total, score_detail, stock):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append(f"# 세아제강지주 일일 체크 리포트")
    lines.append("")
    lines.append(f"- 생성시각: {now}")
    lines.append(f"- 티커: {cfg['ticker']}")
    lines.append(f"- 현재가: {stock.get('price')}")
    lines.append(f"- 20일 평균 대비 거래량 배율: {stock.get('volume_ratio_20d')}")
    lines.append(f"- 52주 고가권 여부: {stock.get('near_52w_high')}")
    lines.append(f"- 종합점수: **{score_total}/100**")
    lines.append(f"- 판단: **{rating(score_total)}**")
    lines.append("")

    lines.append("## 지표별 점수")
    lines.append("")
    lines.append("| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |")
    lines.append("|---|---:|---:|---:|---|")

    for key, sig in signals.items():
        d = score_detail[key]
        lines.append(
            f"| {sig.get('name', key)} | {d['weight']} | {d['score_0_1']} | {d['weighted']} | {sig.get('comment','')} |"
        )

    lines.append("")
    lines.append("## 원자료")
    lines.append("")
    for key, sig in signals.items():
        lines.append(f"### {sig.get('name', key)}")
        for k, v in sig.items():
            if k in ["items"]:
                continue
            lines.append(f"- {k}: {v}")
        if "items" in sig:
            lines.append("- 뉴스:")
            for item in sig["items"][:5]:
                lines.append(f"  - {item['title']}")
        lines.append("")

    return "\n".join(lines)


def send_telegram_if_enabled(cfg, text):
    tg = cfg.get("telegram", {})
    if not tg.get("enabled"):
        return

    token = os.getenv(tg.get("bot_token_env", "TELEGRAM_BOT_TOKEN"))
    chat_id = os.getenv(tg.get("chat_id_env", "TELEGRAM_CHAT_ID"))
    if not token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text[:3500],
        "parse_mode": "Markdown"
    }, timeout=10)


def main():
    cfg = load_config()
    state = load_state()

    stock = get_stock_signal(cfg["ticker"])

    pipe = score_pipe_price_proxy(cfg)
    rig = parse_rig_count_from_news(state)

    seah_score, seah_items, seah_pos, seah_neg = keyword_news_score(
        cfg["news_queries"]["seah_usa_proxy"],
        cfg["positive_keywords"],
        cfg["negative_keywords"],
        days=14
    )

    adnoc_score, adnoc_items, adnoc_pos, adnoc_neg = keyword_news_score(
        cfg["news_queries"]["adnoc_middle_east"],
        cfg["positive_keywords"],
        cfg["negative_keywords"],
        days=14
    )

    # 아프리카 → 미국 미드스트림/알래스카 LNG (실제 자본배분 본류)
    midstream_score, midstream_items, midstream_pos, midstream_neg = keyword_news_score(
        cfg["news_queries"]["us_midstream_alaska"],
        cfg["positive_keywords"],
        cfg["negative_keywords"],
        days=21
    )

    us_proxy = score_us_proxy_stocks(cfg)

    eps_cycle_inputs = {
        "pipe_price_proxy": pipe,
        "rig_count_proxy":  rig,
        "seah_usa_proxy":   {"score": seah_score},
        "adnoc_middle_east":{"score": adnoc_score},
        "us_midstream_alaska":{"score": midstream_score},
        "us_proxy_stocks":  us_proxy,
    }
    cycle = determine_cycle_stage(eps_cycle_inputs)
    eps   = score_forward_eps(stock.get("price"), cycle)

    signals = {
        "pipe_price_proxy": pipe,
        "rig_count_proxy": rig,
        "seah_usa_proxy": {
            "name": "SeAH Steel USA 가동률 proxy",
            "score": seah_score,
            "positive_news_count": seah_pos,
            "negative_news_count": seah_neg,
            "items": seah_items,
            "comment": "직접 가동률 공시는 드묾. SeAH USA/OCTG/line pipe 뉴스로 proxy 추적."
        },
        "adnoc_middle_east": {
            "name": "ADNOC·중동 수주 proxy",
            "score": adnoc_score,
            "positive_news_count": adnoc_pos,
            "negative_news_count": adnoc_neg,
            "items": adnoc_items,
            "comment": "ADNOC, XRG, API pipeline, clad pipe 관련 뉴스 추적."
        },
        # [변경] africa_projects → us_midstream_alaska
        # Energy Transfer 미드스트림 CAPEX + Alaska LNG 라인파이프가 실제 자본배분 본류
        "us_midstream_alaska": {
            "name": "미국 미드스트림·Alaska LNG proxy",
            "score": midstream_score,
            "positive_news_count": midstream_pos,
            "negative_news_count": midstream_neg,
            "items": midstream_items,
            "comment": "ET Hugh Brinson/Desert SW, Alaska LNG 739마일 API 5L 라인파이프 뉴스 추적."
        },
        "forward_eps": eps,
        # [신규] breakout_signal — 기존 코드에서 계산했지만 종합점수에 미반영됐던 항목
        "breakout_signal": {
            "name": "주가 돌파 신호",
            "score": stock.get("breakout_score", 0.0),
            "near_52w_high": stock.get("near_52w_high"),
            "volume_ratio_20d": stock.get("volume_ratio_20d"),
            "comment": "52주 고가 98% 이상 + 거래량 2배 이상 동시 충족 시 1.0. 강관 테마 과열 경보로도 활용."
        },
        # [신규] 미국 에너지·강관 proxy 주가 모멘텀
        "us_proxy_stocks": us_proxy,
    }

    score_total, score_detail = weighted_score(signals, cfg["weights"])
    report = build_report(cfg, signals, score_total, score_detail, stock)

    REPORT_FILE.write_text(report, encoding="utf-8")
    append_history(score_total, stock)
    save_state(state)

    print(report)

    # 한글은 폭 2칸 → display_pad 로 보정
    def dw(s):
        return sum(2 if ord(c) > 0x2E7F else 1 for c in s)

    def dpad(s, width):
        return s + ' ' * max(0, width - dw(s))

    # 지표 단축명 (고정폭 정렬용)
    SHORT = {
        "pipe_price_proxy":    "Pipe PPI",
        "rig_count_proxy":     "Rig Count",
        "seah_usa_proxy":      "SeAH USA",
        "adnoc_middle_east":   "ADNOC/중동",
        "us_midstream_alaska": "Alaska/ET",
        "forward_eps":         "EPS/PER",
        "breakout_signal":     "돌파신호",
        "us_proxy_stocks":     "US Proxy",
    }

    rows = ""
    for key, sig in signals.items():
        d = score_detail[key]
        name = SHORT.get(key, sig.get("name", key)[:10])
        rows += f"{dpad(name,12)} {d['score_0_1']:.2f}  {d['weight']:>2}  {d['weighted']:>4.1f}\n"

    price_str = f"{int(stock.get('price', 0)):,}" if stock.get('price') else "N/A"
    vol_str   = f"{stock.get('volume_ratio_20d', 0):.2f}x" if stock.get('volume_ratio_20d') else "N/A"
    per_str   = str(eps.get('forward_per', 'N/A'))

    # US proxy 종목별 수익률 한 줄 요약
    proxy_line = us_proxy.get("ticker_returns", "")

    short_msg = (
        f"📊 세아제강지주(003030) 일일 모니터\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"종합점수: *{score_total}/100*  |  {rating(score_total).split(':')[0]}\n"
        f"현재가: {price_str}원  |  거래량배율: {vol_str}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"```\n"
        f"지표          점수  가중  합산\n"
        f"{rows}"
        f"```\n"
        f"🔄 사이클판단: *{cycle['label']}* "
        f"(업황점수 {cycle['avg_cycle_score']:.2f} → EPS {cycle['eps']:,}원 자동선택)\n"
        f"Forward PER: {per_str}배\n"
        f"📐 시나리오: {eps.get('scenarios', '')}\n"
        f"📈 US proxy: {proxy_line}"
    )
    send_telegram_if_enabled(cfg, short_msg)


if __name__ == "__main__":
    main()
