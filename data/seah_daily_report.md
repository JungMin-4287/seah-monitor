# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-06-23 23:33:34
- 현재가: 115500.0
- 거래량 배율(20일): 0.5963210026278553
- 52주 고가권: False
- 사이클 판단: [약한회복] 업황점수 0.332
- 본업EPS 30,000 + SeAHWind ADD 16,000 = 46,000원
- Forward PER: 2.5배
- 종합점수: **44.5/100**
- 판단: **약세: 테마 약화 또는 실적 확인 전**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 167.5 | 1M:+2.0% 3M:+3.8% 6M:+3.9% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 563기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 0.0 | 0.0 | $84.7 | 1M:-19.0% 3M:-2.5% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.25 | 2.25 | Census API 데이터 없음 (2~4개월 지연) |
| 美Steel PPI | 8 | 0.5 | 4.0 | WPU1017=348.5 | 1M:+2.1% 3M:+7.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.075 | 0.75 | $58.03 | 1W:-5.9% 1M:-5.8% 3M:+3.4% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정117/부정1건(21일) [영문10+한국어92건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [약한회복] 업황0.33 → 본업30,000+Wind16,000=46,000원 → PER 2.5배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 0.0 | 0.0 | 1W 0/7상승(0.0) / 1M 1/7상승(0.0) → 0.0 |

## 시나리오
저점=7.7x  약한=3.9x  기본=2.6x  강세=1.8x  슈퍼=1.3x

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
- latest: 563
- previous: 563
- comment: 현재 563기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

### WTI 유가
- name: WTI 유가
- score: 0.0
- latest: 84.65
- latest_date: 2026-06-15
- mom_1m: -0.19010715652506693
- mom_3m: -0.024769585253456072
- comment: $84.7 | 1M:-19.0% 3M:-2.5% (FRED DCOILWTICO, 일간)

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
- score: 0.075
- price: 58.03
- ret_1w: -0.0587
- ret_1m: -0.0581
- ret_3m: 0.034
- latest_date: 2026-06-23
- comment: $58.03 | 1W:-5.9% 1M:-5.8% 3M:+3.4% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 117
- negative_news_count: 1
- kr_news_count: 92
- en_news_count: 10
- comment: 긍정117/부정1건(21일) [영문10+한국어92건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - Tees Valley Mayor Ben Houchen challenged on SeAH Wind 'success' in Teesside - Teesside Live
  - GOW 2026: TNuOS ‘must be fixed’ for Scots arrays - reNews
  - Contracts for Difference Allocation Round 8 (AR8): What we know so far - Burges Salmon
  - GOW 2026: ORE Catapult calls for ‘coordinated action’ on deepwater wind - reNews
  - Iberdrola Stock - strategy and grid expansion in focus - AD HOC NEWS

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 약한회복
- avg_cycle_score: 0.332
- base_eps: 30000
- wind_add_eps: 16000
- total_eps: 46000
- forward_per: 2.5
- scenarios: 저점=7.7x  약한=3.9x  기본=2.6x  강세=1.8x  슈퍼=1.3x
- comment: [약한회복] 업황0.33 → 본업30,000+Wind16,000=46,000원 → PER 2.5배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 0.5963210026278553
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 0.0
- score_1w: 0.0
- score_1m: 0.0
- positive_1w: 0/7
- positive_1m: 1/7
- ticker_returns: DNOW:-2%/+3%  TS:-6%/-6%  BKR:-6%/-11%  HAL:-8%/-15%  SLB:-11%/-16%  HP:-4%/-11%  PTEN:-6%/-17%
- comment: 1W 0/7상승(0.0) / 1M 1/7상승(0.0) → 0.0
