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

    close = float(df["Close"].iloc[-1])
    volume = float(df["Volume"].iloc[-1])
    avg20 = float(df["Volume"].tail(20).mean())
    high52 = float(df["Close"].max())

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


def score_forward_eps(stock_price: float | None, forecast_eps: int):
    if not stock_price or forecast_eps <= 0:
        return {
            "name": "2026E EPS / Forward PER",
            "score": 0.0,
            "forward_per": None,
            "forecast_eps": forecast_eps,
            "comment": "주가 또는 EPS 입력값 없음."
        }

    fwd_per = stock_price / forecast_eps

    # 강관 업종 현실적 밸류에이션 기준
    if fwd_per <= 8.0:
        score = 1.0
    elif fwd_per <= 10.0:
        score = 0.75
    elif fwd_per <= 12.0:
        score = 0.50
    elif fwd_per <= 15.0:
        score = 0.25
    else:
        score = 0.0

    return {
        "name": "2026E EPS / Forward PER",
        "score": score,
        "forward_per": round(fwd_per, 2),
        "forecast_eps": forecast_eps,
        "comment": "EPS는 config.yaml 수동 입력. 증권사 컨센서스가 바뀌면 직접 수정. 강관 업종 기준 적용."
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

    eps = score_forward_eps(stock.get("price"), int(cfg["forecast_eps"]))

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
    }

    score_total, score_detail = weighted_score(signals, cfg["weights"])
    report = build_report(cfg, signals, score_total, score_detail, stock)

    REPORT_FILE.write_text(report, encoding="utf-8")
    append_history(score_total, stock)
    save_state(state)

    print(report)

    short_msg = (
        f"세아제강지주 일일점수: {score_total}/100\n"
        f"판단: {rating(score_total)}\n"
        f"현재가: {stock.get('price')}\n"
        f"거래량배율: {stock.get('volume_ratio_20d')}\n"
        f"Forward PER: {eps.get('forward_per')}"
    )
    send_telegram_if_enabled(cfg, short_msg)


if __name__ == "__main__":
    main()
