import os
import re
import json
import time
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

STATE_FILE    = DATA_DIR / "state.json"
REPORT_FILE   = DATA_DIR / "seah_daily_report.md"
HISTORY_FILE  = DATA_DIR / "seah_daily_history.csv"


# ─────────────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────────────

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def fred_csv(series_id: str) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    df  = pd.read_csv(url)
    df.columns = ["date", "value"]
    df["date"]  = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().sort_values("date")

def pct_change_latest(df: pd.DataFrame, periods: int):
    if len(df) <= periods:
        return None
    latest = df["value"].iloc[-1]
    prev   = df["value"].iloc[-1 - periods]
    if prev == 0 or pd.isna(prev):
        return None
    return latest / prev - 1

def google_news(query: str, days: int = 14, lang="en-US", country="US") -> list:
    url = (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query)}&hl={lang}&gl={country}&ceid={country}:en"
    )
    feed   = feedparser.parse(url)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    items  = []
    for entry in feed.entries:
        published = None
        if getattr(entry, "published_parsed", None):
            published = datetime.fromtimestamp(
                time.mktime(entry.published_parsed), tz=timezone.utc
            )
        if published and published < cutoff:
            continue
        items.append({
            "title":     re.sub("<.*?>", "", entry.get("title", "")),
            "summary":   re.sub("<.*?>", "", entry.get("summary", "")),
            "link":      entry.get("link", ""),
            "published": published.isoformat() if published else None,
        })
    return items

def keyword_news_score(queries, positive_keywords, negative_keywords, days=14):
    all_items = []
    for q in queries:
        try:
            all_items.extend(google_news(q, days=days))
        except Exception:
            pass
    seen, unique = set(), []
    for item in all_items:
        key = item["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    pos_count = neg_count = 0
    for item in unique:
        text = (item["title"] + " " + item["summary"]).lower()
        if any(k.lower() in text for k in positive_keywords):
            pos_count += 1
        if any(k.lower() in text for k in negative_keywords):
            neg_count += 1
    raw = pos_count - neg_count
    if   raw >= 5: score = 1.0
    elif raw >= 3: score = 0.75
    elif raw >= 1: score = 0.50
    elif raw == 0: score = 0.25
    else:          score = 0.0
    return score, unique[:10], pos_count, neg_count


# ─────────────────────────────────────────────
# 지표 1. Pipe/OCTG PPI  (FRED WPU10170652, 월간)
# ─────────────────────────────────────────────

def score_pipe_price_proxy(cfg):
    series = cfg["fred_series"]["carbon_pipe_ppi"]
    df     = fred_csv(series)
    latest      = float(df["value"].iloc[-1])
    latest_date = df["date"].iloc[-1].date().isoformat()
    mom_1m = pct_change_latest(df, 1)
    mom_3m = pct_change_latest(df, 3)
    mom_6m = pct_change_latest(df, 6)
    score  = 0.0
    if mom_1m is not None and mom_1m > 0:     score += 0.35
    if mom_3m is not None and mom_3m > 0.015: score += 0.40
    if mom_6m is not None and mom_6m > 0.03:  score += 0.25
    m1s = f"{mom_1m:+.1%}" if mom_1m is not None else "N/A"
    m3s = f"{mom_3m:+.1%}" if mom_3m is not None else "N/A"
    m6s = f"{mom_6m:+.1%}" if mom_6m is not None else "N/A"
    return {
        "name":    "Pipe/OCTG PPI",
        "score":   round(score, 3),
        "latest":  latest,
        "latest_date": latest_date,
        "mom_1m":  mom_1m,
        "mom_3m":  mom_3m,
        "comment": f"{latest:.1f} | 1M:{m1s} 3M:{m3s} 6M:{m6s} (FRED WPU10170652)",
    }


# ─────────────────────────────────────────────
# 지표 2. Rig Count  (뉴스 파싱, 후행지표 — 가중치 최소)
# ─────────────────────────────────────────────

def parse_rig_count_from_news(state):
    """
    분석글 근거: 퍼미안 리그당 생산량 2007년 57bbl → 현재 1,372bbl(24배).
    리그 수는 후행지표 — 4월에 OCTG가격이 리그카운트보다 먼저 상승.
    가중치 6으로 최소화, 단독 판단 금지.
    """
    items     = google_news("Baker Hughes U.S. rig count oil gas rigs", days=10)
    text_blob = " ".join([x["title"] + " " + x["summary"] for x in items])
    patterns  = [
        r"(?:rig count|total rig count).*?(?:rose|rises|increased|up).*?(?:to|at)\s+(\d{3,4})",
        r"(?:rig count|total rig count).*?(?:fell|falls|declined|down).*?(?:to|at)\s+(\d{3,4})",
        r"U\.S\..*?rig count.*?(?:to|at)\s+(\d{3,4})",
    ]
    latest = None
    for p in patterns:
        m = re.search(p, text_blob, re.IGNORECASE)
        if m:
            latest = int(m.group(1))
            break
    prev = state.get("last_us_rig_count")
    if latest is None:
        return {"name": "Rig Count(후행)", "score": 0.25, "latest": None,
                "comment": "추출 실패. ※후행지표 — 단독 판단 금지."}
    state["last_us_rig_count"] = latest
    change = (latest - int(prev)) if prev is not None else None
    if   change is None:  score = 0.50
    elif change >= 10:    score = 1.0
    elif change >= 3:     score = 0.75
    elif change >= 0:     score = 0.50
    elif change > -5:     score = 0.25
    else:                 score = 0.0
    chg_str = f"{'+' if change and change >= 0 else ''}{change}" if change is not None else "N/A"
    return {
        "name":    "Rig Count(후행)",
        "score":   score,
        "latest":  latest,
        "previous": prev,
        "comment": f"현재 {latest}기 / 전주 대비 {chg_str}기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.",
    }


# ─────────────────────────────────────────────
# 지표 3. WTI 유가  (FRED, 일간) — 중동 프로젝트 드라이버
# ─────────────────────────────────────────────

def score_wti() -> dict:
    df          = fred_csv("DCOILWTICO")
    latest      = float(df["value"].iloc[-1])
    latest_date = df["date"].iloc[-1].date().isoformat()
    mom_1m      = pct_change_latest(df, 22)
    mom_3m      = pct_change_latest(df, 66)
    score = 0.0
    if mom_1m is not None:
        if   mom_1m > 0.05: score += 0.50
        elif mom_1m > 0.01: score += 0.30
        elif mom_1m > 0:    score += 0.15
    if mom_3m is not None:
        if   mom_3m > 0.10: score += 0.50
        elif mom_3m > 0.03: score += 0.30
        elif mom_3m > 0:    score += 0.15
    score = min(round(score, 3), 1.0)
    m1s = f"{mom_1m:+.1%}" if mom_1m is not None else "N/A"
    m3s = f"{mom_3m:+.1%}" if mom_3m is not None else "N/A"
    return {
        "name":        "WTI 유가",
        "score":       score,
        "latest":      latest,
        "latest_date": latest_date,
        "mom_1m":      mom_1m,
        "mom_3m":      mom_3m,
        "comment":     f"${latest:.1f} | 1M:{m1s} 3M:{m3s} (FRED DCOILWTICO, 일간)",
    }


# ─────────────────────────────────────────────
# 지표 4. 한국산 강관 對美 수출 볼륨  (US Census HS7306)
# ─────────────────────────────────────────────

def score_korean_pipe_exports() -> dict:
    """
    US Census Bureau API — 한국산 강관(HS7306) 대미 수입 금액 모멘텀.
    단가 직접 계산은 불가(HS4 수량=0)이나 금액 추이 자체가 수출 볼륨 직접 proxy.
    약 2개월 지연 (2월 데이터 → 4월 공개).
    MoM + YoY 증감률로 채점.
    """
    from datetime import date as _date

    url = "https://api.census.gov/data/timeseries/intltrade/imports/hs"

    def fetch_val(ym: str):
        params = {
            "get":         "GEN_VAL_MO",
            "I_COMMODITY": "7306",
            "CTY_CODE":    "5800",
            "COMM_LVL":    "HS4",
            "time":        ym,
        }
        try:
            r = requests.get(url, params=params, timeout=12)
            if r.status_code != 200:
                return None
            data = r.json()
            if len(data) < 2:
                return None
            return int(data[1][0]) if data[1][0] else None
        except Exception:
            return None

    # 최신 가용 월 탐색 (2~5개월 전)
    today = _date.today()
    latest_val, latest_ym = None, None
    for delta in range(2, 6):
        m = today.month - delta
        y = today.year + (m - 1) // 12
        m = ((m - 1) % 12) + 1
        ym = f"{y}-{m:02d}"
        v = fetch_val(ym)
        if v is not None and v > 0:
            latest_val, latest_ym = v, ym
            break

    if latest_val is None:
        return {
            "name":    "韓강관 對美수출볼륨",
            "score":   0.25,
            "comment": "Census API 데이터 없음 (2~4개월 지연)",
        }

    y, m     = int(latest_ym[:4]), int(latest_ym[5:])
    prev_m   = m - 1 if m > 1 else 12
    prev_y   = y if m > 1 else y - 1
    ym_prev  = f"{prev_y}-{prev_m:02d}"
    ym_yoy   = f"{y-1}-{m:02d}"

    prev_val = fetch_val(ym_prev)
    yoy_val  = fetch_val(ym_yoy)

    mom = (latest_val / prev_val - 1) if (prev_val and prev_val > 0) else None
    yoy = (latest_val / yoy_val  - 1) if (yoy_val  and yoy_val  > 0) else None

    score = 0.0
    if mom is not None:
        if   mom > 0.20: score += 0.40
        elif mom > 0.05: score += 0.25
        elif mom > 0:    score += 0.15
    if yoy is not None:
        if   yoy > 0.30: score += 0.60
        elif yoy > 0.10: score += 0.40
        elif yoy > 0:    score += 0.25
    score = min(round(score, 3), 1.0)

    mom_s = f"{mom:+.1%}" if mom is not None else "N/A"
    yoy_s = f"{yoy:+.1%}" if yoy is not None else "N/A"

    return {
        "name":       "韓강관 對美수출볼륨",
        "score":      score,
        "latest_ym":  latest_ym,
        "latest_val": latest_val,
        "mom":        mom,
        "yoy":        yoy,
        "comment": (
            f"{latest_ym} ${latest_val/1e6:.1f}M | "
            f"MoM:{mom_s} YoY:{yoy_s} "
            f"(Census HS7306 한국산 강관 수입금액)"
        ),
    }




def score_steel_ppi() -> dict:
    """
    FRED WPU1017 — 미국 Steel Mill Products PPI (월간).
    Census HS7306(2개월 지연)과 보완 관계:
    PPI는 당월 반영되므로 수출 볼륨 데이터 공백 구간을 메워줌.
    미국 철강 PPI 상승 = 미국 내 생산 단가 상승 = 한국산 수입이 더 유리해짐.
    """
    df          = fred_csv("WPU1017")
    latest      = float(df["value"].iloc[-1])
    latest_date = df["date"].iloc[-1].date().isoformat()
    mom_1m      = pct_change_latest(df, 1)
    mom_3m      = pct_change_latest(df, 3)
    score = 0.0
    if mom_1m is not None:
        if   mom_1m > 0.08: score += 0.50
        elif mom_1m > 0.03: score += 0.35
        elif mom_1m > 0:    score += 0.20
    if mom_3m is not None:
        if   mom_3m > 0.15: score += 0.50
        elif mom_3m > 0.05: score += 0.30
        elif mom_3m > 0:    score += 0.15
    score = min(round(score, 3), 1.0)
    m1s = f"{mom_1m:+.1%}" if mom_1m is not None else "N/A"
    m3s = f"{mom_3m:+.1%}" if mom_3m is not None else "N/A"
    return {
        "name":        "美Steel PPI",
        "score":       score,
        "latest":      latest,
        "latest_date": latest_date,
        "mom_1m":      mom_1m,
        "mom_3m":      mom_3m,
        "comment":     f"WPU1017={latest:.1f} | 1M:{m1s} 3M:{m3s} (美HRC↑=韓수출경쟁력↑, FRED 월간)",
    }


def score_tenaris() -> dict:
    """
    세계 최대 OCTG 메이커 Tenaris(TS NYSE).
    분석글: OCTG 가격이 리그 카운트보다 먼저 오름 → TS 주가가 선행지표.
    1W×30% + 1M×40% + 3M×30%
    """
    try:
        df    = yf.download("TS", period="6mo", auto_adjust=True, progress=False)
        close = df["Close"].squeeze()
        latest    = float(close.iloc[-1])
        week_ago  = float(close.iloc[-6])  if len(close) >= 6  else float(close.iloc[0])
        month_ago = float(close.iloc[-21]) if len(close) >= 21 else float(close.iloc[0])
        q3_ago    = float(close.iloc[-63]) if len(close) >= 63 else float(close.iloc[0])
        r1w = (latest / week_ago)  - 1
        r1m = (latest / month_ago) - 1
        r3m = (latest / q3_ago)    - 1
        last_date = df.index[-1].date().isoformat()

        def s(r, hi, lo):
            return 1.0 if r > hi else (0.5 if r > lo else (0.25 if r > 0 else 0.0))

        score = round(s(r1w, 0.05, 0.02)*0.30 + s(r1m, 0.08, 0.03)*0.40 + s(r3m, 0.15, 0.05)*0.30, 3)
        return {
            "name":    "Tenaris(TS) OCTG선행",
            "score":   score,
            "price":   round(latest, 2),
            "ret_1w":  round(r1w, 4),
            "ret_1m":  round(r1m, 4),
            "ret_3m":  round(r3m, 4),
            "latest_date": last_date,
            "comment": f"${latest:.2f} | 1W:{r1w:+.1%} 1M:{r1m:+.1%} 3M:{r3m:+.1%} 세계1위 OCTG peer, 가격선행지표",
        }
    except Exception as e:
        return {"name": "Tenaris(TS) OCTG선행", "score": 0.25, "comment": f"오류: {e}"}


# ─────────────────────────────────────────────
# 지표 6. SeAH Wind 모멘텀  ★ 핵심 신규 지표
# ─────────────────────────────────────────────

def score_seah_wind(cfg) -> dict:
    """
    SeAH Wind + 영국/대만/한국/글로벌 해상풍력 종합 모멘텀.
    한국어 쿼리는 hl=ko&gl=KR, 영문 쿼리는 hl=en-US&gl=US 분리 처리.
    """
    all_queries = cfg["news_queries"]["seah_wind"]

    # 한국어 쿼리 / 영문 쿼리 분리
    kr_queries = [q for q in all_queries if any(ord(c) > 0x2E7F for c in q)]
    en_queries = [q for q in all_queries if q not in kr_queries]

    pos_kw = (cfg["positive_keywords"]
              + ["monopile", "foundation", "offshore wind", "AR8", "CfD", "CIB",
                 "Teesside", "local content", "substructure", "SeAH Wind",
                 "해상풍력", "모노파일", "하부구조물", "수주", "계약"])
    neg_kw = (cfg["negative_keywords"]
              + ["cancel bid", "competition delay", "FID postpone",
                 "사업 취소", "입찰 실패", "공사 중단"])

    # 영문 뉴스 수집
    en_score, en_items, en_pos, en_neg = keyword_news_score(
        en_queries, pos_kw, neg_kw, days=21
    )

    # 한국어 뉴스 수집 (hl=ko&gl=KR)
    kr_items_raw = []
    for q in kr_queries:
        try:
            kr_items_raw.extend(google_news(q, days=21, lang="ko", country="KR"))
        except Exception:
            pass

    # 한국어 뉴스 중복 제거 및 채점
    seen_kr = set()
    kr_items = []
    for item in kr_items_raw:
        key = item["title"].lower()
        if key not in seen_kr:
            seen_kr.add(key)
            kr_items.append(item)

    kr_pos = kr_neg = 0
    for item in kr_items:
        text = (item["title"] + " " + item["summary"]).lower()
        if any(k.lower() in text for k in pos_kw):
            kr_pos += 1
        if any(k.lower() in text for k in neg_kw):
            kr_neg += 1

    # 영문 + 한국어 합산
    total_pos = en_pos + kr_pos
    total_neg = en_neg + kr_neg
    raw       = total_pos - total_neg

    if   raw >= 5: score = 1.0
    elif raw >= 3: score = 0.75
    elif raw >= 1: score = 0.50
    elif raw == 0: score = 0.25
    else:          score = 0.0

    all_items = (en_items + kr_items)[:10]

    return {
        "name":                "SeAH Wind ★",
        "score":               score,
        "positive_news_count": total_pos,
        "negative_news_count": total_neg,
        "kr_news_count":       len(kr_items),
        "en_news_count":       len(en_items),
        "items":               all_items,
        "comment": (
            f"긍정{total_pos}/부정{total_neg}건(21일) "
            f"[영문{len(en_items)}+한국어{len(kr_items)}건] | "
            "영국CfD AR8·CIB 유일수혜. "
            "수주잔고~2조, 26H2 매출인식."
        ),
    }


# ─────────────────────────────────────────────
# 지표 7. Forward EPS/PER — 사이클 자동판단 + SeAH Wind ADD
# ─────────────────────────────────────────────

def determine_cycle_and_eps(cycle_signals: dict, seah_wind_score: float,
                             stock_price) -> dict:
    """
    본업 사이클 EPS (분석글 기준):
      피크(22~23년): 5,600~5,900억 OP → EPS ~70~90k
      저점(25년):    2,000억 OP       → EPS ~15k
      26E 기본:      4,000~4,500억    → EPS ~45~55k

    SeAH Wind ADD EPS (77% 연결, 발행주수 4,141천주):
      score ≥ 0.70 → ADD 16,000원 (연 ADD OP ~2,400억 반영)
      score ≥ 0.50 → ADD 10,000원 (연 ADD OP ~1,500억)
      score ≥ 0.30 → ADD  5,000원 (26H2 부분 인식)
      score  < 0.30→ ADD      0원
    """
    EPS_CYCLE = [
        (0.70, "슈퍼사이클", 90000),
        (0.55, "강세",       65000),
        (0.40, "기본회복",   45000),
        (0.25, "약한회복",   30000),
        (0.00, "저점",       15000),
    ]
    WIND_ADD = [(0.70, 16000), (0.50, 10000), (0.30, 5000), (0.00, 0)]

    scores = [v.get("score", 0.0) for v in cycle_signals.values()]
    avg    = sum(scores) / len(scores) if scores else 0.0

    cycle_label, base_eps = "저점", 15000
    for thr, lbl, e in EPS_CYCLE:
        if avg >= thr:
            cycle_label, base_eps = lbl, e
            break

    wind_add = 0
    for thr, add in WIND_ADD:
        if seah_wind_score >= thr:
            wind_add = add
            break

    total_eps = base_eps + wind_add

    fwd_per, score = None, 0.0
    if stock_price and total_eps > 0:
        fwd_per = stock_price / total_eps
        if   fwd_per <= 3.5:  score = 1.0
        elif fwd_per <= 5.0:  score = 0.85
        elif fwd_per <= 6.5:  score = 0.70
        elif fwd_per <= 8.0:  score = 0.50
        elif fwd_per <= 10.0: score = 0.25
        else:                 score = 0.0

    scenarios = ""
    if stock_price:
        scenarios = "  ".join(
            f"{lbl}={round(stock_price/e,1)}x"
            for lbl, e in [("저점",15000),("약한",30000),("기본",45000),("강세",65000),("슈퍼",90000)]
        )

    return {
        "name":            "Forward EPS/PER",
        "score":           round(score, 3),
        "cycle_label":     cycle_label,
        "avg_cycle_score": round(avg, 3),
        "base_eps":        base_eps,
        "wind_add_eps":    wind_add,
        "total_eps":       total_eps,
        "forward_per":     round(fwd_per, 1) if fwd_per else None,
        "scenarios":       scenarios,
        "comment": (
            f"[{cycle_label}] 업황{avg:.2f} → 본업{base_eps:,}"
            f"+Wind{wind_add:,}={total_eps:,}원 → PER {round(fwd_per,1) if fwd_per else 'N/A'}배"
        ),
    }


# ─────────────────────────────────────────────
# 지표 8. 주가 돌파 신호  (yfinance 003030.KS)
# ─────────────────────────────────────────────

def get_stock_signal(ticker: str) -> dict:
    import math as _math

    df_5d = yf.download(ticker, period="5d", auto_adjust=True, progress=False)
    df_1y = yf.download(ticker, period="1y", auto_adjust=True, progress=False)

    if df_5d.empty or df_1y.empty:
        return {"price": None, "volume": None,
                "volume_ratio_20d": None, "near_52w_high": None, "breakout_score": 0.0}

    # yfinance 버그: 당일 Close=NaN, Volume=유효 행이 추가되는 경우 있음 → dropna 제거
    close_5d  = df_5d["Close"].squeeze().dropna()
    vol_5d    = df_5d["Volume"].squeeze()
    close_1y  = df_1y["Close"].squeeze().dropna()
    volume_1y = df_1y["Volume"].squeeze()

    if close_5d.empty or close_1y.empty:
        return {"price": None, "volume": None,
                "volume_ratio_20d": None, "near_52w_high": None, "breakout_score": 0.0}

    close   = float(close_5d.iloc[-1])
    # Volume은 NaN 행의 거래량이 실제 당일 거래량일 수 있으므로 마지막 유효값 사용
    vol_valid = vol_5d.dropna()
    volume  = float(vol_valid.iloc[-1]) if not vol_valid.empty else 0.0
    avg20   = float(volume_1y.tail(20).mean())
    high52  = float(close_1y.max())

    if _math.isnan(close):
        return {"price": None, "volume": None,
                "volume_ratio_20d": None, "near_52w_high": None, "breakout_score": 0.0}
    if _math.isnan(avg20) or avg20 == 0: avg20 = 1.0
    if _math.isnan(high52): high52 = close
    vol_r   = volume / avg20 if avg20 > 0 else None
    near_h  = close >= high52 * 0.98
    score   = 0.0
    if near_h: score += 0.5
    if vol_r and vol_r >= 2.0:  score += 0.5
    elif vol_r and vol_r >= 1.5: score += 0.3
    return {
        "price":            close,
        "volume":           volume,
        "volume_ratio_20d": vol_r,
        "near_52w_high":    near_h,
        "breakout_score":   round(score, 3),
    }


# ─────────────────────────────────────────────
# 지표 9. US Proxy 주가군  (1W/1M)
# ─────────────────────────────────────────────

def score_us_proxy_stocks(cfg) -> dict:
    """1W×0.4 + 1M×0.6"""
    tickers = {
        "DNOW": "PVF유통", "TS": "OCTG peer", "BKR": "LNG인프라",
        "HAL": "북미유정", "SLB": "글로벌E&P", "HP": "육상rig", "PTEN": "drilling",
    }
    results, r1w_list, r1m_list = {}, [], []
    for ticker, desc in tickers.items():
        try:
            df    = yf.download(ticker, period="3mo", auto_adjust=True, progress=False)
            if df.empty:
                results[ticker] = {"ret_1w": None, "ret_1m": None}
                continue
            close     = df["Close"].squeeze()
            latest    = float(close.iloc[-1])
            week_ago  = float(close.iloc[-6])  if len(close) >= 6  else float(close.iloc[0])
            month_ago = float(close.iloc[-21]) if len(close) >= 21 else float(close.iloc[0])
            r1w = (latest / week_ago) - 1
            r1m = (latest / month_ago) - 1
            results[ticker] = {"ret_1w": round(r1w, 4), "ret_1m": round(r1m, 4), "price": round(latest,2)}
            r1w_list.append(r1w)
            r1m_list.append(r1m)
        except Exception:
            results[ticker] = {"ret_1w": None, "ret_1m": None}

    def ps(returns):
        if not returns: return 0.25
        pos = sum(1 for r in returns if r > 0) / len(returns)
        avg_r = sum(returns) / len(returns)
        if pos >= 0.71 and avg_r > 0.03: return 1.0
        elif pos >= 0.57: return 0.75
        elif pos >= 0.43: return 0.50
        elif pos >= 0.29: return 0.25
        else: return 0.0

    s1w = ps(r1w_list)
    s1m = ps(r1m_list)
    score = round(s1w * 0.4 + s1m * 0.6, 3)
    n   = len(r1w_list)
    p1w = sum(1 for r in r1w_list if r > 0)
    p1m = sum(1 for r in r1m_list if r > 0)
    ticker_lines = "  ".join(
        f"{t}:{v['ret_1w']:+.0%}/{v['ret_1m']:+.0%}"
        if v["ret_1w"] is not None else f"{t}:N/A"
        for t, v in results.items()
    )
    return {
        "name":           "US Proxy 주가군",
        "score":          score,
        "score_1w":       s1w,
        "score_1m":       s1m,
        "positive_1w":    f"{p1w}/{n}",
        "positive_1m":    f"{p1m}/{n}",
        "ticker_returns": ticker_lines,
        "comment":        f"1W {p1w}/{n}상승({s1w}) / 1M {p1m}/{n}상승({s1m}) → {score}",
    }


# ─────────────────────────────────────────────
# 집계 / 리포트 / 텔레그램
# ─────────────────────────────────────────────

def weighted_score(signals, weights):
    total, detail = 0.0, {}
    for key, sig in signals.items():
        w = weights.get(key, 0)
        s = sig.get("score", 0.0)
        total += w * s
        detail[key] = {"weight": w, "score_0_1": s, "weighted": round(w * s, 2)}
    return round(total, 1), detail


def rating(total_score):
    if total_score >= 75: return "강세 확인: 추세추종 보유/추가 검토"
    if total_score >= 60: return "우호적: 보유 우위, 돌파·거래량 확인"
    if total_score >= 45: return "중립: 모멘텀 확인 필요"
    return "약세: 테마 약화 또는 실적 확인 전"


def append_history(score_total, stock, eps_info):
    today = datetime.now().strftime("%Y-%m-%d")
    row   = {
        "date":            today,
        "score":           score_total,
        "price":           stock.get("price"),
        "volume_ratio_20d": stock.get("volume_ratio_20d"),
        "cycle_label":     eps_info.get("cycle_label"),
        "total_eps":       eps_info.get("total_eps"),
        "forward_per":     eps_info.get("forward_per"),
    }
    if HISTORY_FILE.exists():
        hist = pd.read_csv(HISTORY_FILE)
        hist = hist[hist["date"] != today]
        hist = pd.concat([hist, pd.DataFrame([row])], ignore_index=True)
    else:
        hist = pd.DataFrame([row])
    hist.to_csv(HISTORY_FILE, index=False)


def build_report(cfg, signals, score_total, score_detail, stock, eps_info):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 세아제강지주(003030) 일일 체크 리포트", "",
        f"- 생성시각: {now}",
        f"- 현재가: {stock.get('price')}",
        f"- 거래량 배율(20일): {stock.get('volume_ratio_20d')}",
        f"- 52주 고가권: {stock.get('near_52w_high')}",
        f"- 사이클 판단: [{eps_info.get('cycle_label')}] 업황점수 {eps_info.get('avg_cycle_score')}",
        f"- 본업EPS {eps_info.get('base_eps'):,} + SeAHWind ADD {eps_info.get('wind_add_eps'):,} = {eps_info.get('total_eps'):,}원",
        f"- Forward PER: {eps_info.get('forward_per')}배",
        f"- 종합점수: **{score_total}/100**",
        f"- 판단: **{rating(score_total)}**", "",
        "## 지표별 점수", "",
        "| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |",
        "|---|---:|---:|---:|---|",
    ]
    for key, sig in signals.items():
        d = score_detail[key]
        lines.append(f"| {sig.get('name',key)} | {d['weight']} | {d['score_0_1']} | {d['weighted']} | {sig.get('comment','')} |")
    lines += ["", "## 시나리오", f"{eps_info.get('scenarios','')}", "", "## 원자료", ""]
    for key, sig in signals.items():
        lines.append(f"### {sig.get('name',key)}")
        for k, v in sig.items():
            if k == "items": continue
            lines.append(f"- {k}: {v}")
        if "items" in sig:
            lines.append("- 뉴스:")
            for item in sig["items"][:5]:
                lines.append(f"  - {item['title']}")
        lines.append("")
    return "\n".join(lines)


def send_telegram_if_enabled(cfg, text):
    tg = cfg.get("telegram", {})
    if not tg.get("enabled"): return
    token   = os.getenv(tg.get("bot_token_env", "TELEGRAM_BOT_TOKEN"))
    chat_id = os.getenv(tg.get("chat_id_env",   "TELEGRAM_CHAT_ID"))
    if not token or not chat_id: return
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text[:3500], "parse_mode": "Markdown"},
        timeout=10,
    )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    cfg   = load_config()
    state = load_state()

    stock = get_stock_signal(cfg["ticker"])

    pipe        = score_pipe_price_proxy(cfg)
    rig         = parse_rig_count_from_news(state)
    wti         = score_wti()
    export_comp = score_korean_pipe_exports()
    steel_ppi   = score_steel_ppi()
    tenaris     = score_tenaris()
    seah_wind   = score_seah_wind(cfg)
    us_proxy    = score_us_proxy_stocks(cfg)

    cycle_inputs = {
        "pipe": pipe, "rig": rig, "wti": wti,
        "export_comp": export_comp, "steel_ppi": steel_ppi,
        "tenaris": tenaris, "us_proxy": us_proxy,
    }
    eps_info = determine_cycle_and_eps(
        cycle_inputs, seah_wind.get("score", 0.0), stock.get("price")
    )

    signals = {
        "pipe_ppi":        pipe,
        "rig_count":       rig,
        "wti_price":       wti,
        "export_comp":     export_comp,
        "steel_ppi":       steel_ppi,
        "tenaris":         tenaris,
        "seah_wind":       seah_wind,
        "forward_eps":     eps_info,
        "breakout_signal": {
            "name":             "주가 돌파 신호",
            "score":            stock.get("breakout_score", 0.0),
            "near_52w_high":    stock.get("near_52w_high"),
            "volume_ratio_20d": stock.get("volume_ratio_20d"),
            "comment":          "52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0",
        },
        "us_proxy":        us_proxy,
    }

    score_total, score_detail = weighted_score(signals, cfg["weights"])
    report = build_report(cfg, signals, score_total, score_detail, stock, eps_info)

    REPORT_FILE.write_text(report, encoding="utf-8")
    append_history(score_total, stock, eps_info)
    save_state(state)
    print(report)

    # ── 텔레그램 메시지
    def dw(s):  return sum(2 if ord(c) > 0x2E7F else 1 for c in s)
    def dpad(s, w): return s + ' ' * max(0, w - dw(s))

    SHORT = {
        "pipe_ppi":        "Pipe PPI",
        "rig_count":       "Rig(후행)",
        "wti_price":       "WTI유가",
        "export_comp":     "韓강관수출",
        "steel_ppi":       "美Steel PPI",
        "tenaris":         "TS선행",
        "seah_wind":       "SeAHWind★",
        "forward_eps":     "EPS/PER",
        "breakout_signal": "돌파신호",
        "us_proxy":        "US Proxy",
    }

    rows = ""
    for key, sig in signals.items():
        d    = score_detail[key]
        name = SHORT.get(key, key[:10])
        rows += f"{dpad(name,12)} {d['score_0_1']:.2f}  {d['weight']:>2}  {d['weighted']:>4.1f}\n"

    import math
    _price = stock.get("price")
    price_str = (f"{int(_price):,}" if (_price is not None and not math.isnan(_price))
                 else "N/A")
    _vol = stock.get("volume_ratio_20d")
    vol_str = (f"{_vol:.2f}x" if (_vol is not None and not math.isnan(_vol))
               else "N/A")
    wind_add = eps_info.get("wind_add_eps", 0) or 0
    wind_add_str = (f"+{int(wind_add):,}원" if wind_add > 0 else "ADD미반영(26H2전)")

    def fmt_pct(v):
        return f"{v:+.1%}" if (v is not None and not math.isnan(v)) else "N/A"

    ts_price = tenaris.get("price")
    ts_line = (
        f"TS ${ts_price:.2f}  "
        f"1W:{fmt_pct(tenaris.get('ret_1w'))} "
        f"1M:{fmt_pct(tenaris.get('ret_1m'))} "
        f"3M:{fmt_pct(tenaris.get('ret_3m'))}"
        if (ts_price is not None and not math.isnan(float(ts_price))) else ""
    )

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
        f"🔄 사이클: *{eps_info['cycle_label']}* (업황 {eps_info['avg_cycle_score']:.2f})\n"
        f"   본업EPS {eps_info['base_eps']:,} | SeAHWind {wind_add_str}\n"
        f"   합산EPS {eps_info['total_eps']:,}원 → PER *{eps_info['forward_per']}배*\n"
        f"📐 {eps_info.get('scenarios','')}\n"
        f"🌊 SeAH Wind: 긍정{seah_wind['positive_news_count']}/부정{seah_wind['negative_news_count']}건\n"
        f"🔩 {ts_line}\n"
        f"📈 US: {us_proxy.get('ticker_returns','')}"
    )
    send_telegram_if_enabled(cfg, short_msg)


if __name__ == "__main__":
    main()
