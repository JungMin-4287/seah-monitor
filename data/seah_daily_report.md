# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-06-17 23:53:50
- 현재가: 142000.0
- 거래량 배율(20일): 1.4997879555858038
- 52주 고가권: False
- 사이클 판단: [기본회복] 업황점수 0.414
- 본업EPS 45,000 + SeAHWind ADD 16,000 = 61,000원
- Forward PER: 2.3배
- 종합점수: **50.2/100**
- 판단: **중립: 모멘텀 확인 필요**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 167.5 | 1M:+2.0% 3M:+3.8% 6M:+3.9% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 433기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 0.5 | 5.0 | $95.0 | 1M:-3.8% 3M:+27.4% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.25 | 2.25 | Census API 데이터 없음 (2~4개월 지연) |
| 美Steel PPI | 8 | 0.5 | 4.0 | WPU1017=348.5 | 1M:+2.1% 3M:+7.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.15 | 1.5 | $59.11 | 1W:-3.8% 1M:-2.8% 3M:+7.5% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정139/부정0건(21일) [영문10+한국어108건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [기본회복] 업황0.41 → 본업45,000+Wind16,000=61,000원 → PER 2.3배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 0.0 | 0.0 | 1W 0/7상승(0.0) / 1M 1/7상승(0.0) → 0.0 |

## 시나리오
저점=9.5x  약한=4.7x  기본=3.2x  강세=2.2x  슈퍼=1.6x

## 원자료

### Pipe/OCTG PPI
- name: Pipe/OCTG PPI
- score: 1.0
- latest: 167.469
- latest_date: 2026-02-01
- mom_1m: 0.01974717766979639
- mom_3m: 0.03765366313076246
- comment: 167.5 | 1M:+2.0% 3M:+3.8% 6M:+3.9% (FRED WPU10170652)

### Rig Count(후행)
- name: Rig Count(후행)
- score: 0.5
- latest: 433
- previous: 433
- comment: 현재 433기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

### WTI 유가
- name: WTI 유가
- score: 0.5
- latest: 95.0
- latest_date: 2026-06-08
- mom_1m: -0.03797468354430378
- mom_3m: 0.2737999463663181
- comment: $95.0 | 1M:-3.8% 3M:+27.4% (FRED DCOILWTICO, 일간)

### 韓강관 對美수출볼륨
- name: 韓강관 對美수출볼륨
- score: 0.25
- comment: Census API 데이터 없음 (2~4개월 지연)

### 美Steel PPI
- name: 美Steel PPI
- score: 0.5
- latest: 348.53
- latest_date: 2026-05-01
- mom_1m: 0.02122559964370052
- mom_3m: 0.0720536442072559
- comment: WPU1017=348.5 | 1M:+2.1% 3M:+7.2% (美HRC↑=韓수출경쟁력↑, FRED 월간)

### Tenaris(TS) OCTG선행
- name: Tenaris(TS) OCTG선행
- score: 0.15
- price: 59.11
- ret_1w: -0.0384
- ret_1m: -0.0284
- ret_3m: 0.075
- latest_date: 2026-06-17
- comment: $59.11 | 1W:-3.8% 1M:-2.8% 3M:+7.5% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 139
- negative_news_count: 0
- kr_news_count: 108
- en_news_count: 10
- comment: 긍정139/부정0건(21일) [영문10+한국어108건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - Trouble ahead on Teesside: SeAH Wind faces a financial storm - North East Bylines
  - Tees Valley Mayor Ben Houchen challenged on SeAH Wind 'success' in Teesside - Teesside Live
  - Teesside and North Yorkshire residents recognised in King’s Birthday Honours list - Teesside Live
  - King's Birthday Honours: Olympic team manager and literacy heroine among Teessiders recognised - Teesside Live
  - UK sets out AR8 Contracts for Difference timetable - reNews

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 기본회복
- avg_cycle_score: 0.414
- base_eps: 45000
- wind_add_eps: 16000
- total_eps: 61000
- forward_per: 2.3
- scenarios: 저점=9.5x  약한=4.7x  기본=3.2x  강세=2.2x  슈퍼=1.6x
- comment: [기본회복] 업황0.41 → 본업45,000+Wind16,000=61,000원 → PER 2.3배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 1.4997879555858038
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 0.0
- score_1w: 0.0
- score_1m: 0.0
- positive_1w: 0/7
- positive_1m: 1/7
- ticker_returns: DNOW:-2%/+4%  TS:-4%/-3%  BKR:-5%/-8%  HAL:-9%/-15%  SLB:-9%/-11%  HP:-9%/-13%  PTEN:-14%/-18%
- comment: 1W 0/7상승(0.0) / 1M 1/7상승(0.0) → 0.0
