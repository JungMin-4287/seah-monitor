# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-05-12 23:33:08
- 현재가: 185400.0
- 거래량 배율(20일): 1.1385833220742305
- 52주 고가권: False
- 사이클 판단: [강세] 업황점수 0.621
- 본업EPS 65,000 + SeAHWind ADD 16,000 = 81,000원
- Forward PER: 2.3배
- 종합점수: **66.0/100**
- 판단: **우호적: 보유 우위, 돌파·거래량 확인**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 170.5 | 1M:+1.1% 3M:+2.8% 6M:+5.1% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 548기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 1.0 | 10.0 | $109.8 | 1M:+7.7% 3M:+74.9% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.25 | 2.25 | Census API 데이터 없음 (2~4개월 지연) |
| 美Steel PPI | 8 | 0.5 | 4.0 | WPU1017=331.7 | 1M:+2.1% 3M:+6.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.5 | 5.0 | $62.50 | 1W:-1.5% 1M:+6.1% 3M:+28.5% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정42/부정5건(21일) [영문10+한국어37건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [강세] 업황0.62 → 본업65,000+Wind16,000=81,000원 → PER 2.3배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 0.6 | 7.2 | 1W 0/7상승(0.0) / 1M 7/7상승(1.0) → 0.6 |

## 시나리오
저점=12.4x  약한=6.2x  기본=4.1x  강세=2.9x  슈퍼=2.1x

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
- latest: 548
- previous: 548
- comment: 현재 548기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

### WTI 유가
- name: WTI 유가
- score: 1.0
- latest: 109.76
- latest_date: 2026-05-04
- mom_1m: 0.07713444553483817
- mom_3m: 0.7491633466135459
- comment: $109.8 | 1M:+7.7% 3M:+74.9% (FRED DCOILWTICO, 일간)

### 韓강관 對美수출볼륨
- name: 韓강관 對美수출볼륨
- score: 0.25
- comment: Census API 데이터 없음 (2~4개월 지연)

### 美Steel PPI
- name: 美Steel PPI
- score: 0.5
- latest: 331.671
- latest_date: 2026-03-01
- mom_1m: 0.020566976525214775
- mom_3m: 0.06165295605134258
- comment: WPU1017=331.7 | 1M:+2.1% 3M:+6.2% (美HRC↑=韓수출경쟁력↑, FRED 월간)

### Tenaris(TS) OCTG선행
- name: Tenaris(TS) OCTG선행
- score: 0.5
- price: 62.5
- ret_1w: -0.0154
- ret_1m: 0.0608
- ret_3m: 0.2847
- latest_date: 2026-05-12
- comment: $62.50 | 1W:-1.5% 1M:+6.1% 3M:+28.5% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 42
- negative_news_count: 5
- kr_news_count: 37
- en_news_count: 10
- comment: 긍정42/부정5건(21일) [영문10+한국어37건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - Iberdrola Q1 2026 slides: profit jumps 11%, guidance raised to >8% - Investing.com
  - Iberdrola S.A. stock (ES0144580F34): Is renewable energy expansion strong enough to unlock new upsid - AD HOC NEWS
  - Study: UK's offshore wind capacity to increase by around 20 per cent in 2026 - Business Green
  - Reform government could cause Truss-style chaos, says renewables industry - The Guardian
  - News Content Hub - UK needs 5 GW of offshore wind every year to meet government goals - rivieramm.com

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 강세
- avg_cycle_score: 0.621
- base_eps: 65000
- wind_add_eps: 16000
- total_eps: 81000
- forward_per: 2.3
- scenarios: 저점=12.4x  약한=6.2x  기본=4.1x  강세=2.9x  슈퍼=2.1x
- comment: [강세] 업황0.62 → 본업65,000+Wind16,000=81,000원 → PER 2.3배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 1.1385833220742305
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 0.6
- score_1w: 0.0
- score_1m: 1.0
- positive_1w: 0/7
- positive_1m: 7/7
- ticker_returns: DNOW:-2%/+12%  TS:-2%/+6%  BKR:-4%/+6%  HAL:-0%/+11%  SLB:-1%/+8%  HP:-6%/+15%  PTEN:-3%/+22%
- comment: 1W 0/7상승(0.0) / 1M 7/7상승(1.0) → 0.6
