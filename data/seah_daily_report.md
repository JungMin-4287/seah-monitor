# 세아제강지주 일일 체크 리포트

- 생성시각: 2026-04-28 13:06:34
- 티커: 003030.KS
- 현재가: 250000.0
- 20일 평균 대비 거래량 배율: 2.097662623269813
- 52주 고가권 여부: True
- 종합점수: **64.8/100**
- 판단: **우호적: 보유 우위, 돌파·거래량 확인**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| 미국 Pipe/OCTG 가격 proxy | 18 | 1.0 | 18.0 | FRED/BLS carbon steel pipe PPI 기준. OCTG 직접 가격은 아님. |
| 미국 Rig Count proxy | 12 | 0.5 | 6.0 | Baker Hughes rig count 뉴스에서 숫자 추출. 수동 검증 권장. |
| SeAH Steel USA 가동률 proxy | 12 | 0.25 | 3.0 | 직접 가동률 공시는 드묾. SeAH USA/OCTG/line pipe 뉴스로 proxy 추적. |
| ADNOC·중동 수주 proxy | 18 | 0.5 | 9.0 | ADNOC, XRG, API pipeline, clad pipe 관련 뉴스 추적. |
| 미국 미드스트림·Alaska LNG proxy | 10 | 0.25 | 2.5 | ET Hugh Brinson/Desert SW, Alaska LNG 739마일 API 5L 라인파이프 뉴스 추적. |
| 2026E EPS / Forward PER | 15 | 0.75 | 11.25 | EPS는 config.yaml 수동 입력. 증권사 컨센서스가 바뀌면 직접 수정. 강관 업종 기준 적용. |
| 주가 돌파 신호 | 15 | 1.0 | 15.0 | 52주 고가 98% 이상 + 거래량 2배 이상 동시 충족 시 1.0. 강관 테마 과열 경보로도 활용. |

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
- previous: None
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

### 2026E EPS / Forward PER
- name: 2026E EPS / Forward PER
- score: 0.75
- forward_per: 10.0
- forecast_eps: 25000
- comment: EPS는 config.yaml 수동 입력. 증권사 컨센서스가 바뀌면 직접 수정. 강관 업종 기준 적용.

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 1.0
- near_52w_high: True
- volume_ratio_20d: 2.097662623269813
- comment: 52주 고가 98% 이상 + 거래량 2배 이상 동시 충족 시 1.0. 강관 테마 과열 경보로도 활용.
