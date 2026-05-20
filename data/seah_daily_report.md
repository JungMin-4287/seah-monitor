# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-05-20 23:44:38
- 현재가: 167900.0
- 거래량 배율(20일): 0.5101996093971312
- 52주 고가권: False
- 사이클 판단: [강세] 업황점수 0.657
- 본업EPS 65,000 + SeAHWind ADD 16,000 = 81,000원
- Forward PER: 2.1배
- 종합점수: **68.8/100**
- 판단: **우호적: 보유 우위, 돌파·거래량 확인**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 170.5 | 1M:+1.1% 3M:+2.8% 6M:+5.1% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 551기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 1.0 | 10.0 | $112.2 | 1M:+16.4% 3M:+73.2% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.25 | 2.25 | Census API 데이터 없음 (2~4개월 지연) |
| 美Steel PPI | 8 | 0.65 | 5.2 | WPU1017=344.2 | 1M:+3.8% 3M:+9.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.3 | 3.0 | $60.69 | 1W:-2.7% 1M:-0.4% 3M:+18.4% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정40/부정0건(21일) [영문10+한국어20건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [강세] 업황0.66 → 본업65,000+Wind16,000=81,000원 → PER 2.1배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 0.9 | 10.8 | 1W 6/7상승(0.75) / 1M 6/7상승(1.0) → 0.9 |

## 시나리오
저점=11.2x  약한=5.6x  기본=3.7x  강세=2.6x  슈퍼=1.9x

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
- score: 0.5
- latest: 551
- previous: 551
- comment: 현재 551기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

### WTI 유가
- name: WTI 유가
- score: 1.0
- latest: 112.25
- latest_date: 2026-05-18
- mom_1m: 0.16369479577026746
- mom_3m: 0.7322530864197532
- comment: $112.2 | 1M:+16.4% 3M:+73.2% (FRED DCOILWTICO, 일간)

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
- score: 0.3
- price: 60.69
- ret_1w: -0.0269
- ret_1m: -0.0044
- ret_3m: 0.1842
- latest_date: 2026-05-20
- comment: $60.69 | 1W:-2.7% 1M:-0.4% 3M:+18.4% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 40
- negative_news_count: 0
- kr_news_count: 20
- en_news_count: 10
- comment: 긍정40/부정0건(21일) [영문10+한국어20건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - National Grid commits record £70bn to power the next decade of energy networks - Business Matters
  - RWE Offshore Wind Approvals Expand UK Pipeline And Raise Valuation Questions - Trending Now Sustainable Construction
  - OnPath Energy Targets £1 bn Renewable Energy Investment in Scotland with 121 MW Wind Expansion - GreentechLead
  - Study: UK's offshore wind capacity to increase by around 20 per cent in 2026 - BusinessGreen
  - Reform government could cause Truss-style chaos, says renewables industry | Renewable energy - The Guardian

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 강세
- avg_cycle_score: 0.657
- base_eps: 65000
- wind_add_eps: 16000
- total_eps: 81000
- forward_per: 2.1
- scenarios: 저점=11.2x  약한=5.6x  기본=3.7x  강세=2.6x  슈퍼=1.9x
- comment: [강세] 업황0.66 → 본업65,000+Wind16,000=81,000원 → PER 2.1배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 0.5101996093971312
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 0.9
- score_1w: 0.75
- score_1m: 1.0
- positive_1w: 6/7
- positive_1m: 6/7
- ticker_returns: DNOW:+0%/+7%  TS:-3%/-0%  BKR:+2%/+7%  HAL:+3%/+8%  SLB:+3%/+5%  HP:+8%/+13%  PTEN:+2%/+14%
- comment: 1W 6/7상승(0.75) / 1M 6/7상승(1.0) → 0.9
