# 세아제강지주 일일 체크 리포트

- 생성시각: 2026-04-28 14:27:53
- 티커: 003030.KS
- 현재가: 250000.0
- 20일 평균 대비 거래량 배율: 2.097662623269813
- 52주 고가권 여부: True
- 종합점수: **73.5/100**
- 판단: **우호적: 보유 우위, 돌파·거래량 확인**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| 미국 Pipe/OCTG 가격 proxy | 15 | 1.0 | 15.0 | FRED/BLS carbon steel pipe PPI 기준. OCTG 직접 가격은 아님. |
| 미국 Rig Count proxy | 10 | 0.5 | 5.0 | Baker Hughes rig count 뉴스에서 숫자 추출. 수동 검증 권장. |
| Henry Hub 천연가스 | 10 | 0.0 | 0.0 | 2.81 | 1M:-9.9%  3M:-6.3%  E&P capex 선행지표 | 상승=OCTG 수요↑ |
| WTI 유가 | 15 | 0.5 | 7.5 | 91.06 | 1M:-5.3%  3M:+49.6%  중동 프로젝트 드라이버 | 상승=발주↑ |
| 철강 PPI (Steel mill) | 10 | 0.6 | 6.0 | 331.67 | 1M:+2.1%  3M:+6.2%  파이프라인 수요 proxy | 상승=강관 수요↑ |
| Forward PER (사이클 자동판단) | 15 | 1.0 | 15.0 | [강세] 업황점수 0.60 → EPS 55,000원 자동선택 → PER 4.5배 |
| 주가 돌파 신호 | 15 | 1.0 | 15.0 | 52주 고가 98% 이상 + 거래량 2배 이상 동시 충족 시 1.0. |
| 미국 에너지·강관 proxy 주가 | 10 | 1.0 | 10.0 | 1W 7/7상승(점수 1.0) / 1M 7/7상승(점수 1.0) → 종합 1.0 |

## 원자료

### 미국 Pipe/OCTG 가격 proxy
- name: 미국 Pipe/OCTG 가격 proxy
- score: 1.0
- latest: 170.455
- latest_date: 2026-03-01
- mom_1m: 0.010852483320978656
- mom_3m: 0.0277722506617466
- mom_6m: 0.05144496190975545
- comment: FRED/BLS carbon steel pipe PPI 기준. OCTG 직접 가격은 아님.

### 미국 Rig Count proxy
- name: 미국 Rig Count proxy
- score: 0.5
- latest: 544
- previous: 544
- comment: Baker Hughes rig count 뉴스에서 숫자 추출. 수동 검증 권장.

### Henry Hub 천연가스
- name: Henry Hub 천연가스
- score: 0.0
- latest: 2.81
- latest_date: 2026-04-20
- mom_1m: -0.09935897435897434
- mom_3m: -0.06333333333333335
- comment: 2.81 | 1M:-9.9%  3M:-6.3%  E&P capex 선행지표 | 상승=OCTG 수요↑

### WTI 유가
- name: WTI 유가
- score: 0.5
- latest: 91.06
- latest_date: 2026-04-20
- mom_1m: -0.05264253017062004
- mom_3m: 0.4964667214461791
- comment: 91.06 | 1M:-5.3%  3M:+49.6%  중동 프로젝트 드라이버 | 상승=발주↑

### 철강 PPI (Steel mill)
- name: 철강 PPI (Steel mill)
- score: 0.6
- latest: 331.671
- latest_date: 2026-03-01
- mom_1m: 0.020566976525214775
- mom_3m: 0.06165295605134258
- comment: 331.67 | 1M:+2.1%  3M:+6.2%  파이프라인 수요 proxy | 상승=강관 수요↑

### Forward PER (사이클 자동판단)
- name: Forward PER (사이클 자동판단)
- score: 1.0
- forward_per: 4.5
- forecast_eps: 55000
- cycle_label: 강세
- avg_cycle_score: 0.6
- scenarios: 저점=10.0x  약한=7.1x  기본=5.6x  강세=4.5x  슈퍼=3.6x
- comment: [강세] 업황점수 0.60 → EPS 55,000원 자동선택 → PER 4.5배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 1.0
- near_52w_high: True
- volume_ratio_20d: 2.097662623269813
- comment: 52주 고가 98% 이상 + 거래량 2배 이상 동시 충족 시 1.0.

### 미국 에너지·강관 proxy 주가
- name: 미국 에너지·강관 proxy 주가
- score: 1.0
- score_1w: 1.0
- score_1m: 1.0
- positive_1w: 7/7
- positive_1m: 7/7
- ticker_returns: DNOW:+8%/+11%  TS:+4%/+10%  BKR:+14%/+13%  HAL:+6%/+3%  SLB:+6%/+9%  HP:+9%/+8%  PTEN:+11%/+6%
- comment: 1W 7/7상승(점수 1.0) / 1M 7/7상승(점수 1.0) → 종합 1.0
