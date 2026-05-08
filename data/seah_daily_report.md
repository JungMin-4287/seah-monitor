# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-05-08 23:15:54
- 현재가: 205000.0
- 거래량 배율(20일): 1.1228805000690998
- 52주 고가권: False
- 사이클 판단: [강세] 업황점수 0.557
- 본업EPS 65,000 + SeAHWind ADD 16,000 = 81,000원
- Forward PER: 2.5배
- 종합점수: **61.7/100**
- 판단: **우호적: 보유 우위, 돌파·거래량 확인**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 170.5 | 1M:+1.1% 3M:+2.8% 6M:+5.1% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 548기 / 전주 대비 +1기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 1.0 | 10.0 | $109.8 | 1M:+7.7% 3M:+74.9% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.0 | 0.0 | 2026-03 $45.4M | MoM:-44.4% YoY:-32.2% (Census HS7306 한국산 강관 수입금액) |
| 美Steel PPI | 8 | 0.5 | 4.0 | WPU1017=331.7 | 1M:+2.1% 3M:+6.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.3 | 3.0 | $59.81 | 1W:-6.1% 1M:-0.1% 3M:+25.9% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정56/부정5건(21일) [영문10+한국어39건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [강세] 업황0.56 → 본업65,000+Wind16,000=81,000원 → PER 2.5배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 0.6 | 7.2 | 1W 0/7상승(0.0) / 1M 6/7상승(1.0) → 0.6 |

## 시나리오
저점=13.7x  약한=6.8x  기본=4.6x  강세=3.2x  슈퍼=2.3x

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
- previous: 547
- comment: 현재 548기 / 전주 대비 +1기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

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
- score: 0.0
- latest_ym: 2026-03
- latest_val: 45350252
- mom: -0.4440752424471238
- yoy: -0.32174403988691214
- comment: 2026-03 $45.4M | MoM:-44.4% YoY:-32.2% (Census HS7306 한국산 강관 수입금액)

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
- score: 0.3
- price: 59.81
- ret_1w: -0.0611
- ret_1m: -0.0013
- ret_3m: 0.2589
- latest_date: 2026-05-08
- comment: $59.81 | 1W:-6.1% 1M:-0.1% 3M:+25.9% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 56
- negative_news_count: 5
- kr_news_count: 39
- en_news_count: 10
- comment: 긍정56/부정5건(21일) [영문10+한국어39건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - UK sets initial CfD CIB budget for AR8 - reNews
  - UK needs 5GW of offshore wind every year to stay on track for government goals - Offshore Energies UK (OEUK)
  - Madrid summit: Wind’s record expansion at risk as political intervention threatens revenue - Recharge News
  - Iberdrola Q1 2026 slides: profit jumps 11%, guidance raised to >8% - Investing.com
  - Iberdrola S.A. stock (ES0144580F34): Is renewable energy expansion strong enough to unlock new upsid - AD HOC NEWS

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 강세
- avg_cycle_score: 0.557
- base_eps: 65000
- wind_add_eps: 16000
- total_eps: 81000
- forward_per: 2.5
- scenarios: 저점=13.7x  약한=6.8x  기본=4.6x  강세=3.2x  슈퍼=2.3x
- comment: [강세] 업황0.56 → 본업65,000+Wind16,000=81,000원 → PER 2.5배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 1.1228805000690998
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 0.6
- score_1w: 0.0
- score_1m: 1.0
- positive_1w: 0/7
- positive_1m: 6/7
- ticker_returns: DNOW:-3%/+7%  TS:-6%/-0%  BKR:-7%/+2%  HAL:-4%/+6%  SLB:-6%/+3%  HP:-7%/+9%  PTEN:-5%/+14%
- comment: 1W 0/7상승(0.0) / 1M 6/7상승(1.0) → 0.6
