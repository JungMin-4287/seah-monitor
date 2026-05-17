# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-05-17 23:15:03
- 현재가: 193400.0
- 거래량 배율(20일): 1.075256204737887
- 52주 고가권: False
- 사이클 판단: [슈퍼사이클] 업황점수 0.764
- 본업EPS 90,000 + SeAHWind ADD 16,000 = 106,000원
- Forward PER: 1.8배
- 종합점수: **74.0/100**
- 판단: **우호적: 보유 우위, 돌파·거래량 확인**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 170.5 | 1M:+1.1% 3M:+2.8% 6M:+5.1% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 1.0 | 5.0 | 현재 551기 / 전주 대비 +136기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 0.8 | 8.0 | $101.6 | 1M:+1.9% 3M:+57.3% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.25 | 2.25 | Census API 데이터 없음 (2~4개월 지연) |
| 美Steel PPI | 8 | 0.65 | 5.2 | WPU1017=344.2 | 1M:+3.8% 3M:+9.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.65 | 6.5 | $61.77 | 1W:+3.3% 1M:+5.4% 3M:+25.1% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정46/부정2건(21일) [영문10+한국어27건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [슈퍼사이클] 업황0.76 → 본업90,000+Wind16,000=106,000원 → PER 1.8배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 1.0 | 12.0 | 1W 7/7상승(1.0) / 1M 7/7상승(1.0) → 1.0 |

## 시나리오
저점=12.9x  약한=6.4x  기본=4.3x  강세=3.0x  슈퍼=2.1x

## 원자료

### Pipe/OCTG PPI
- name: Pipe/OCTG PPI
- score: 1.0
- latest: 170.455
- latest_date: 2026-03-01
- mom_1m: 0.010852483320978656
- mom_3m: 0.0277722506617466
- comment: 170.5 | 1M:+1.1% 3M:+2.8% 6M:+5.1% (FRED WPU10170652)

### Rig Count(후행)
- name: Rig Count(후행)
- score: 1.0
- latest: 551
- previous: 415
- comment: 현재 551기 / 전주 대비 +136기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

### WTI 유가
- name: WTI 유가
- score: 0.8
- latest: 101.56
- latest_date: 2026-05-11
- mom_1m: 0.019474001204577318
- mom_3m: 0.5731102850061958
- comment: $101.6 | 1M:+1.9% 3M:+57.3% (FRED DCOILWTICO, 일간)

### 韓강관 對美수출볼륨
- name: 韓강관 對美수출볼륨
- score: 0.25
- comment: Census API 데이터 없음 (2~4개월 지연)

### 美Steel PPI
- name: 美Steel PPI
- score: 0.65
- latest: 344.202
- latest_date: 2026-04-01
- mom_1m: 0.03812258340823127
- mom_3m: 0.09158545364594417
- comment: WPU1017=344.2 | 1M:+3.8% 3M:+9.2% (美HRC↑=韓수출경쟁력↑, FRED 월간)

### Tenaris(TS) OCTG선행
- name: Tenaris(TS) OCTG선행
- score: 0.65
- price: 61.77
- ret_1w: 0.0328
- ret_1m: 0.0539
- ret_3m: 0.2509
- latest_date: 2026-05-15
- comment: $61.77 | 1W:+3.3% 1M:+5.4% 3M:+25.1% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 46
- negative_news_count: 2
- kr_news_count: 27
- en_news_count: 10
- comment: 긍정46/부정2건(21일) [영문10+한국어27건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - RWE Offshore Wind Approvals Expand UK Pipeline And Raise Valuation Questions - Trending Now Sustainable Construction
  - Iberdrola Q1 2026 slides: profit jumps 11%, guidance raised to >8% - Investing.com Canada
  - National Grid commits record £70bn to power the next decade of energy networks - Business Matters
  - All-Energy: 'Power policy stable despite uncertainty' - reNews
  - Study: UK's offshore wind capacity to increase by around 20 per cent in 2026 - BusinessGreen

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 슈퍼사이클
- avg_cycle_score: 0.764
- base_eps: 90000
- wind_add_eps: 16000
- total_eps: 106000
- forward_per: 1.8
- scenarios: 저점=12.9x  약한=6.4x  기본=4.3x  강세=3.0x  슈퍼=2.1x
- comment: [슈퍼사이클] 업황0.76 → 본업90,000+Wind16,000=106,000원 → PER 1.8배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 1.075256204737887
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 1.0
- score_1w: 1.0
- score_1m: 1.0
- positive_1w: 7/7
- positive_1m: 7/7
- ticker_returns: DNOW:+1%/+10%  TS:+3%/+5%  BKR:+0%/+8%  HAL:+5%/+12%  SLB:+4%/+5%  HP:+5%/+17%  PTEN:+9%/+32%
- comment: 1W 7/7상승(1.0) / 1M 7/7상승(1.0) → 1.0
