# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-04-30 23:15:21
- 현재가: 240000.0
- 거래량 배율(20일): 1.6651412724164052
- 52주 고가권: False
- 사이클 판단: [슈퍼사이클] 업황점수 0.836
- 본업EPS 90,000 + SeAHWind ADD 16,000 = 106,000원
- Forward PER: 2.3배
- 종합점수: **84.3/100**
- 판단: **강세 확인: 추세추종 보유/추가 검토**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 170.5 | 1M:+1.1% 3M:+2.8% 6M:+5.1% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 544기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 1.0 | 10.0 | $99.9 | 1M:+9.2% 3M:+65.4% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 1.0 | 9.0 | 2026-02 $81.6M | MoM:+120.0% YoY:+105.1% (Census HS7306 한국산 강관 수입금액) |
| 美Steel PPI | 8 | 0.5 | 4.0 | WPU1017=331.7 | 1M:+2.1% 3M:+6.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.85 | 8.5 | $63.90 | 1W:+2.0% 1M:+10.3% 3M:+44.2% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정32/부정6건(21일) [영문10+한국어15건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [슈퍼사이클] 업황0.84 → 본업90,000+Wind16,000=106,000원 → PER 2.3배 |
| 주가 돌파 신호 | 11 | 0.3 | 3.3 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 1.0 | 12.0 | 1W 7/7상승(1.0) / 1M 7/7상승(1.0) → 1.0 |

## 시나리오
저점=16.0x  약한=8.0x  기본=5.3x  강세=3.7x  슈퍼=2.7x

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
- latest: 544
- previous: 544
- comment: 현재 544기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

### WTI 유가
- name: WTI 유가
- score: 1.0
- latest: 99.89
- latest_date: 2026-04-27
- mom_1m: 0.09157469129056928
- mom_3m: 0.6543557469360715
- comment: $99.9 | 1M:+9.2% 3M:+65.4% (FRED DCOILWTICO, 일간)

### 韓강관 對美수출볼륨
- name: 韓강관 對美수출볼륨
- score: 1.0
- latest_ym: 2026-02
- latest_val: 81576241
- mom: 1.2004372700685928
- yoy: 1.0513651246880342
- comment: 2026-02 $81.6M | MoM:+120.0% YoY:+105.1% (Census HS7306 한국산 강관 수입금액)

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
- score: 0.85
- price: 63.9
- ret_1w: 0.0203
- ret_1m: 0.1032
- ret_3m: 0.4424
- latest_date: 2026-04-30
- comment: $63.90 | 1W:+2.0% 1M:+10.3% 3M:+44.2% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 32
- negative_news_count: 6
- kr_news_count: 15
- en_news_count: 10
- comment: 긍정32/부정6건(21일) [영문10+한국어15건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - Westwood Insight – How Mainland China is reshaping the offshore wind foundation market - Westwood Global Energy Group
  - Contracts for Difference and the economics of renewable energy deployment. - UK Parliament
  - SSE plc stock (GB0007908733): Is renewable energy expansion strong enough to unlock new upside? - AD HOC NEWS
  - Elia Group stock (BE0003822393): Why grid expansion strategy matters more now for energy transition - AD HOC NEWS
  - Iberdrola Q1 2026 slides: profit jumps 11%, guidance raised to >8% - Investing.com

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 슈퍼사이클
- avg_cycle_score: 0.836
- base_eps: 90000
- wind_add_eps: 16000
- total_eps: 106000
- forward_per: 2.3
- scenarios: 저점=16.0x  약한=8.0x  기본=5.3x  강세=3.7x  슈퍼=2.7x
- comment: [슈퍼사이클] 업황0.84 → 본업90,000+Wind16,000=106,000원 → PER 2.3배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.3
- near_52w_high: False
- volume_ratio_20d: 1.6651412724164052
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 1.0
- score_1w: 1.0
- score_1m: 1.0
- positive_1w: 7/7
- positive_1m: 7/7
- ticker_returns: DNOW:+8%/+14%  TS:+2%/+10%  BKR:+8%/+15%  HAL:+7%/+11%  SLB:+4%/+14%  HP:+7%/+17%  PTEN:+10%/+18%
- comment: 1W 7/7상승(1.0) / 1M 7/7상승(1.0) → 1.0
