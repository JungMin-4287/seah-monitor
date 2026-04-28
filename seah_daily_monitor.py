from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote_plus

import feedparser
import pandas as pd
import requests
import yaml
import yfinance as yf

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "state.json"
REPORT_FILE = DATA_DIR / "seah_daily_report.md"
CSV_FILE = DATA_DIR / "seah_daily_history.csv"


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_float(x):
    try:
        if x is None:
            return None
        if isinstance(x, pd.Series):
            x = x.iloc[0]
        if pd.isna(x):
            return None
        return float(x)
    except Exception:
        return None


def fred_csv(series_id: str) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    df = pd.read_csv(url)
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().sort_values("date")


def pct_change_latest(df: pd.DataFrame, periods: int) -> float | None:
    if len(df) <= periods:
        return None
    latest = safe_float(df["value"].iloc[-1])
    prev = safe_float(df["value"].iloc[-1 - periods])
    if latest is None or prev in (None, 0):
        return None
    return latest / prev - 1


def score_pipe_price_proxy(cfg: dict) -> dict:
    """무료 OCTG 가격 proxy. 실제 OCTG spot price는 Argus/PipeLogix 등 유료 데이터가 더 정확합니다."""
    series = cfg["fred_series"]["carbon_pipe_ppi"]
    try:
        df = fred_csv(series)
    except Exception as e:
        return {"name": "미국 Pipe/OCTG 가격 proxy", "score": 0.0, "comment": f"FRED 수집 실패: {e}"}

    latest = safe_float(df["value"].iloc[-1])
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
        "mom_1m": None if mom_1m is None else round(mom_1m * 100, 2),
        "mom_3m": None if mom_3m is None else round(mom_3m * 100, 2),
        "mom_6m": None if mom_6m is None else round(mom_6m * 100, 2),
        "comment": "FRED/BLS carbon steel pipe PPI 기준. OCTG 직접 가격은 아님.",
    }


def google_news(query: str, days: int = 14, lang: str = "en-US", country: str = "US") -> list[dict]:
    url = "https://news.google.com/rss/search?" + f"q={quote_plus(query)}&hl={lang}&gl={country}&ceid={country}:en"
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
            "published": published.isoformat() if published else None,
        })
    return items


def keyword_news_score(queries: list[str], positive_keywords: list[str], negative_keywords: list[str], days: int) -> tuple:
    all_items = []
    for q in queries:
        try:
            all_items.extend(google_news(q, days=days))
        except Exception:
            continue

    seen = set()
    unique = []
    for item in all_items:
        key = (item["title"] + item.get("published", "")).lower()
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
    if raw >= 6:
        score = 1.0
    elif raw >= 4:
        score = 0.75
    elif raw >= 2:
        score = 0.50
    elif raw >= 0:
        score = 0.25
    else:
        score = 0.0

    return score, unique[:12], pos_count, neg_count


def score_rig_count_proxy(state: dict) -> dict:
    """Baker Hughes rig count를 Google News RSS에서 보조 추출합니다."""
    items = google_news("Baker Hughes U.S. rig count oil gas rigs", days=10)
    text_blob = " ".join([x["title"] + " " + x["summary"] for x in items])

    patterns = [
        r"(?:U\.S\.|US|United States).*?rig count.*?(?:to|at)\s+(\d{3,4})",
        r"(?:rig count|total rig count).*?(?:rose|rises|increased|up).*?(?:to|at)\s+(\d{3,4})",
        r"(?:rig count|total rig count).*?(?:fell|falls|declined|down).*?(?:to|at)\s+(\d{3,4})",
    ]

    latest = None
    for p in patterns:
        m = re.search(p, text_blob, flags=re.IGNORECASE)
        if m:
            latest = int(m.group(1))
            break

    prev = state.get("last_us_rig_count")
    if latest is None:
        return {"name": "미국 Rig Count proxy", "score": 0.25, "latest": None, "previous": prev, "comment": "자동 숫자 추출 실패. Baker Hughes 원자료 수동 확인 권장."}

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

    return {"name": "미국 Rig Count proxy", "score": score, "latest": latest, "previous": prev, "comment": "Baker Hughes rig count 뉴스에서 숫자 추출. 첫 실행은 전주 비교가 제한됨."}


def get_stock_signal(ticker: str, price_override=None) -> dict:
    try:
        df = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
    except Exception:
        df = pd.DataFrame()

    if df.empty:
        price = safe_float(price_override)
        return {"name": "주가·거래량 추세", "score": 0.0, "price": price, "volume": None, "volume_ratio_20d": None, "near_52w_high": None, "comment": "yfinance 데이터 수집 실패. stock_price_override만 반영."}

    close = safe_float(df["Close"].iloc[-1])
    if price_override is not None:
        close = safe_float(price_override)

    volume = safe_float(df["Volume"].iloc[-1])
    avg20 = safe_float(df["Volume"].tail(20).mean())
    high52 = safe_float(df["Close"].max())

    volume_ratio = volume / avg20 if volume and avg20 else None
    near_high = close >= high52 * 0.98 if close and high52 else False

    score = 0.0
    if near_high:
        score += 0.5
    if volume_ratio and volume_ratio >= 2.0:
        score += 0.5
    elif volume_ratio and volume_ratio >= 1.5:
        score += 0.3

    return {"name": "주가·거래량 추세", "score": round(score, 3), "price": close, "volume": volume, "volume_ratio_20d": None if volume_ratio is None else round(volume_ratio, 2), "near_52w_high": near_high, "comment": "52주 고가권 + 20일 평균 대비 거래량으로 추세추종 신호를 평가."}


def score_forward_eps(stock_price: float | None, forecast_eps: int) -> dict:
    if not stock_price or forecast_eps <= 0:
        return {"name": "2026E EPS / Forward PER", "score": 0.0, "forward_per": None, "forecast_eps": forecast_eps, "comment": "주가 또는 EPS 입력값 없음."}

    fwd_per = stock_price / forecast_eps
    if forecast_eps >= 50000 and fwd_per <= 5.5:
        score = 1.0
    elif forecast_eps >= 50000 and fwd_per <= 6.5:
        score = 0.75
    elif forecast_eps >= 45000 and fwd_per <= 7.0:
        score = 0.50
    elif forecast_eps >= 35000 and fwd_per <= 8.0:
        score = 0.25
    else:
        score = 0.0

    return {"name": "2026E EPS / Forward PER", "score": score, "forward_per": round(fwd_per, 2), "forecast_eps": forecast_eps, "comment": "EPS는 config.yaml 수동 입력. 컨센서스 변경 시 forecast_eps 수정."}


def weighted_score(signals: dict, weights: dict) -> tuple[float, dict]:
    total = 0.0
    detail = {}
    for key, sig in signals.items():
        w = weights.get(key, 0)
        s = sig.get("score", 0.0)
        total += w * s
        detail[key] = {"weight": w, "score_0_1": s, "weighted": round(w * s, 2)}
    return round(total, 1), detail


def rating(total_score: float) -> str:
    if total_score >= 75:
        return "강세 확인: 추세추종 보유/추가 검토"
    if total_score >= 60:
        return "우호적: 보유 우위, 돌파·거래량 확인"
    if total_score >= 45:
        return "중립: 모멘텀 확인 필요"
    return "약세: 테마 약화 또는 실적 확인 전"


def build_report(cfg: dict, signals: dict, score_total: float, score_detail: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock = signals.get("stock_trend", {})

    lines = []
    lines.append("# 세아제강지주 일일 체크 리포트")
    lines.append("")
    lines.append(f"- 생성시각: {now}")
    lines.append(f"- 종목: {cfg.get('company_name')} / {cfg.get('ticker')}")
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
        lines.append(f"| {sig.get('name', key)} | {d['weight']} | {d['score_0_1']} | {d['weighted']} | {sig.get('comment','')} |")

    lines.append("")
    lines.append("## 원자료")
    lines.append("")
    for key, sig in signals.items():
        lines.append(f"### {sig.get('name', key)}")
        for k, v in sig.items():
            if k == "items":
                continue
            lines.append(f"- {k}: {v}")
        if "items" in sig:
            lines.append("- 뉴스:")
            for item in sig["items"][:5]:
                lines.append(f"  - {item['title']}")
                if item.get("link"):
                    lines.append(f"    - {item['link']}")
        lines.append("")
    return "\n".join(lines)


def append_history(score_total: float, signals: dict) -> None:
    row = {"date": datetime.now().strftime("%Y-%m-%d"), "total_score": score_total}
    for key, sig in signals.items():
        row[f"{key}_score"] = sig.get("score")
    row["price"] = signals.get("stock_trend", {}).get("price")
    row["forward_per"] = signals.get("forward_eps", {}).get("forward_per")

    new = pd.DataFrame([row])
    if CSV_FILE.exists():
        old = pd.read_csv(CSV_FILE)
        old = old[old["date"] != row["date"]]
        out = pd.concat([old, new], ignore_index=True)
    else:
        out = new
    out.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")


def send_telegram_if_enabled(cfg: dict, text: str) -> None:
    tg = cfg.get("telegram", {})
    if not tg.get("enabled"):
        return
    token = os.getenv(tg.get("bot_token_env", "TELEGRAM_BOT_TOKEN"))
    chat_id = os.getenv(tg.get("chat_id_env", "TELEGRAM_CHAT_ID"))
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text[:3500], "parse_mode": "Markdown"}, timeout=10)


def main() -> None:
    cfg = load_config()
    state = load_state()

    stock = get_stock_signal(cfg["ticker"], cfg.get("stock_price_override"))
    pipe = score_pipe_price_proxy(cfg)
    rig = score_rig_count_proxy(state)

    seah_score, seah_items, seah_pos, seah_neg = keyword_news_score(cfg["news_queries"]["seah_usa_proxy"], cfg["positive_keywords"], cfg["negative_keywords"], days=cfg.get("news_days", {}).get("seah_usa_proxy", 21))
    adnoc_score, adnoc_items, adnoc_pos, adnoc_neg = keyword_news_score(cfg["news_queries"]["adnoc_middle_east"], cfg["positive_keywords"], cfg["negative_keywords"], days=cfg.get("news_days", {}).get("adnoc_middle_east", 21))
    africa_score, africa_items, africa_pos, africa_neg = keyword_news_score(cfg["news_queries"]["africa_projects"], cfg["positive_keywords"], cfg["negative_keywords"], days=cfg.get("news_days", {}).get("africa_projects", 30))
    eps = score_forward_eps(stock.get("price"), int(cfg["forecast_eps"]))

    signals = {
        "pipe_price_proxy": pipe,
        "rig_count_proxy": rig,
        "seah_usa_proxy": {"name": "SeAH Steel USA 가동률 proxy", "score": seah_score, "positive_news_count": seah_pos, "negative_news_count": seah_neg, "items": seah_items, "comment": "직접 가동률 공시는 드묾. SeAH USA/OCTG/line pipe 뉴스로 proxy 추적."},
        "adnoc_middle_east": {"name": "ADNOC·중동 수주 proxy", "score": adnoc_score, "positive_news_count": adnoc_pos, "negative_news_count": adnoc_neg, "items": adnoc_items, "comment": "ADNOC, XRG, API pipeline, clad pipe 관련 뉴스 추적."},
        "africa_projects": {"name": "아프리카 LNG·해상 개발 proxy", "score": africa_score, "positive_news_count": africa_pos, "negative_news_count": africa_neg, "items": africa_items, "comment": "Rovuma, Mozambique LNG, Namibia FPSO, Venus/Mopane 등 추적."},
        "forward_eps": eps,
        "stock_trend": stock,
    }

    score_total, score_detail = weighted_score(signals, cfg["weights"])
    report = build_report(cfg, signals, score_total, score_detail)
    REPORT_FILE.write_text(report, encoding="utf-8")
    append_history(score_total, signals)
    save_state(state)

    print(report)

    short_msg = f"세아제강지주 일일점수: {score_total}/100\n판단: {rating(score_total)}\n현재가: {stock.get('price')}\n거래량배율: {stock.get('volume_ratio_20d')}\nForward PER: {eps.get('forward_per')}"
    send_telegram_if_enabled(cfg, short_msg)


if __name__ == "__main__":
    main()
