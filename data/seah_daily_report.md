# 세아제강지주 일일 체크 리포트

- 생성시각: 2026-04-28 13:23:57
- 티커: 003030.KS
- 현재가: 250000.0
- 20일 평균 대비 거래량 배율: 2.097662623269813
- 52주 고가권 여부: True
- 종합점수: **72.5/100**
- 판단: **우호적: 보유 우위, 돌파·거래량 확인**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| 미국 Pipe/OCTG 가격 proxy | 15 | 1.0 | 15.0 | FRED/BLS carbon steel pipe PPI 기준. OCTG 직접 가격은 아님. |
| 미국 Rig Count proxy | 10 | 0.5 | 5.0 | Baker Hughes rig count 뉴스에서 숫자 추출. 수동 검증 권장. |
| SeAH Steel USA 가동률 proxy | 10 | 0.25 | 2.5 | 직접 가동률 공시는 드묾. SeAH USA/OCTG/line pipe 뉴스로 proxy 추적. |
| ADNOC·중동 수주 proxy | 15 | 0.5 | 7.5 | ADNOC, XRG, API pipeline, clad pipe 관련 뉴스 추적. |
| 미국 미드스트림·Alaska LNG proxy | 10 | 0.25 | 2.5 | ET Hugh Brinson/Desert SW, Alaska LNG 739마일 API 5L 라인파이프 뉴스 추적. |
| Forward PER (사이클 자동판단) | 15 | 1.0 | 15.0 | [강세] 업황점수 0.58 → EPS 55,000원 자동선택 → PER 4.5배 |
| 주가 돌파 신호 | 15 | 1.0 | 15.0 | 52주 고가 98% 이상 + 거래량 2배 이상 동시 충족 시 1.0. 강관 테마 과열 경보로도 활용. |
| 미국 에너지·강관 proxy 주가 | 10 | 1.0 | 10.0 | 1W 7/7상승(점수 1.0) / 1M 6/7상승(점수 1.0) → 종합 1.0 |

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

### SeAH Steel USA 가동률 proxy
- name: SeAH Steel USA 가동률 proxy
- score: 0.25
- positive_news_count: 0
- negative_news_count: 0
- comment: 직접 가동률 공시는 드묾. SeAH USA/OCTG/line pipe 뉴스로 proxy 추적.
- 뉴스:

### ADNOC·중동 수주 proxy
- name: ADNOC·중동 수주 proxy
- score: 0.5
- positive_news_count: 2
- negative_news_count: 0
- comment: ADNOC, XRG, API pipeline, clad pipe 관련 뉴스 추적.
- 뉴스:
  - ADNOC Sets Sights on U.S. Gas With Multibillion-Dollar Expansion Plan - Crude Oil Prices Today | OilPrice.com
  - UAE's ADNOC to invest tens of billions to build US gas business, FT reports - Reuters
  - ADNOC’s US Gas Business Investment: XRG’s $80B Strategy Explained - Discovery Alert
  - Adnoc to invest ‘tens of billions’ in push to build a US gas business - Financial Times
  - ADNOC plans to invest tens of billions of dollars to build the entire US natural gas industry chain - Bitget

### 미국 미드스트림·Alaska LNG proxy
- name: 미국 미드스트림·Alaska LNG proxy
- score: 0.25
- positive_news_count: 0
- negative_news_count: 0
- comment: ET Hugh Brinson/Desert SW, Alaska LNG 739마일 API 5L 라인파이프 뉴스 추적.
- 뉴스:

### Forward PER (사이클 자동판단)
- name: Forward PER (사이클 자동판단)
- score: 1.0
- forward_per: 4.5
- forecast_eps: 55000
- cycle_label: 강세
- avg_cycle_score: 0.583
- scenarios: 저점=10.0x  약한=7.1x  기본=5.6x  강세=4.5x  슈퍼=3.6x
- comment: [강세] 업황점수 0.58 → EPS 55,000원 자동선택 → PER 4.5배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 1.0
- near_52w_high: True
- volume_ratio_20d: 2.097662623269813
- comment: 52주 고가 98% 이상 + 거래량 2배 이상 동시 충족 시 1.0. 강관 테마 과열 경보로도 활용.

### 미국 에너지·강관 proxy 주가
- name: 미국 에너지·강관 proxy 주가
- score: 1.0
- score_1w: 1.0
- score_1m: 1.0
- positive_1w: 7/7
- positive_1m: 6/7
- ticker_returns: DNOW:+6%/+4%  TS:+6%/+8%  BKR:+16%/+8%  HAL:+9%/-1%  SLB:+6%/+3%  HP:+15%/+7%  PTEN:+17%/+1%
- comment: 1W 7/7상승(점수 1.0) / 1M 6/7상승(점수 1.0) → 종합 1.0
