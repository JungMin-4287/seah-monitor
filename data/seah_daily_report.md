# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-06-30 23:41:56
- 현재가: 113800.0
- 거래량 배율(20일): 0.7841588717064928
- 52주 고가권: False
- 사이클 판단: [약한회복] 업황점수 0.321
- 본업EPS 30,000 + SeAHWind ADD 16,000 = 46,000원
- Forward PER: 2.5배
- 종합점수: **43.8/100**
- 판단: **약세: 테마 약화 또는 실적 확인 전**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 167.5 | 1M:+2.0% 3M:+3.8% 6M:+3.9% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 573기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 0.0 | 0.0 | $78.9 | 1M:-29.6% 3M:-17.8% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.25 | 2.25 | Census API 데이터 없음 (2~4개월 지연) |
| 美Steel PPI | 8 | 0.5 | 4.0 | WPU1017=348.5 | 1M:+2.1% 3M:+7.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.0 | 0.0 | $55.49 | 1W:-4.4% 1M:-11.4% 3M:-2.7% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정109/부정1건(21일) [영문10+한국어91건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [약한회복] 업황0.32 → 본업30,000+Wind16,000=46,000원 → PER 2.5배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 0.0 | 0.0 | 1W 0/7상승(0.0) / 1M 1/7상승(0.0) → 0.0 |

## 시나리오
저점=7.6x  약한=3.8x  기본=2.5x  강세=1.8x  슈퍼=1.3x

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
- latest: 573
- previous: 573
- comment: 현재 573기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

### WTI 유가
- name: WTI 유가
- score: 0.0
- latest: 78.94
- latest_date: 2026-06-22
- mom_1m: -0.2957444910339906
- mom_3m: -0.17779397979377154
- comment: $78.9 | 1M:-29.6% 3M:-17.8% (FRED DCOILWTICO, 일간)

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
- score: 0.0
- price: 55.49
- ret_1w: -0.0438
- ret_1m: -0.1139
- ret_3m: -0.0274
- latest_date: 2026-06-30
- comment: $55.49 | 1W:-4.4% 1M:-11.4% 3M:-2.7% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 109
- negative_news_count: 1
- kr_news_count: 91
- en_news_count: 10
- comment: 긍정109/부정1건(21일) [영문10+한국어91건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - Tees Valley Mayor Ben Houchen challenged on SeAH Wind 'success' in Teesside - Teesside Live
  - Contracts for Difference Allocation Round 8 (AR8): What we know so far - Burges Salmon
  - GOW 2026: TNuOS ‘must be fixed’ for Scots arrays - reNEWS
  - Iberdrola Stock - strategy and grid expansion in focus - AD HOC NEWS
  - GOW 2026: Scots eyes ‘game changing’ offshore - reNEWS

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 약한회복
- avg_cycle_score: 0.321
- base_eps: 30000
- wind_add_eps: 16000
- total_eps: 46000
- forward_per: 2.5
- scenarios: 저점=7.6x  약한=3.8x  기본=2.5x  강세=1.8x  슈퍼=1.3x
- comment: [약한회복] 업황0.32 → 본업30,000+Wind16,000=46,000원 → PER 2.5배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 0.7841588717064928
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 0.0
- score_1w: 0.0
- score_1m: 0.0
- positive_1w: 0/7
- positive_1m: 1/7
- ticker_returns: DNOW:-3%/+0%  TS:-4%/-11%  BKR:-5%/-12%  HAL:-3%/-13%  SLB:-3%/-15%  HP:-8%/-17%  PTEN:-9%/-20%
- comment: 1W 0/7상승(0.0) / 1M 1/7상승(0.0) → 0.0
