# 세아제강지주(003030) 일일 체크 리포트

- 생성시각: 2026-05-27 23:41:29
- 현재가: 169300.0
- 거래량 배율(20일): 0.4541194705018338
- 52주 고가권: False
- 사이클 판단: [기본회복] 업황점수 0.507
- 본업EPS 45,000 + SeAHWind ADD 16,000 = 61,000원
- Forward PER: 2.8배
- 종합점수: **56.5/100**
- 판단: **중립: 모멘텀 확인 필요**

## 지표별 점수

| 지표 | 가중치 | 점수 | 가중점수 | 코멘트 |
|---|---:|---:|---:|---|
| Pipe/OCTG PPI | 10 | 1.0 | 10.0 | 170.5 | 1M:+1.1% 3M:+2.8% 6M:+5.1% (FRED WPU10170652) |
| Rig Count(후행) | 5 | 0.5 | 2.5 | 현재 558기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소. |
| WTI 유가 | 10 | 1.0 | 10.0 | $112.2 | 1M:+16.4% 3M:+73.2% (FRED DCOILWTICO, 일간) |
| 韓강관 對美수출볼륨 | 9 | 0.25 | 2.25 | Census API 데이터 없음 (2~4개월 지연) |
| 美Steel PPI | 8 | 0.65 | 5.2 | WPU1017=344.2 | 1M:+3.8% 3M:+9.2% (美HRC↑=韓수출경쟁력↑, FRED 월간) |
| Tenaris(TS) OCTG선행 | 10 | 0.15 | 1.5 | $60.68 | 1W:-0.3% 1M:-2.0% 3M:+13.7% 세계1위 OCTG peer, 가격선행지표 |
| SeAH Wind ★ | 12 | 1.0 | 12.0 | 긍정35/부정0건(21일) [영문10+한국어10건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식. |
| Forward EPS/PER | 13 | 1.0 | 13.0 | [기본회복] 업황0.51 → 본업45,000+Wind16,000=61,000원 → PER 2.8배 |
| 주가 돌파 신호 | 11 | 0.0 | 0.0 | 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0 |
| US Proxy 주가군 | 12 | 0.0 | 0.0 | 1W 1/7상승(0.0) / 1M 2/7상승(0.0) → 0.0 |

## 시나리오
저점=11.3x  약한=5.6x  기본=3.8x  강세=2.6x  슈퍼=1.9x

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
- latest: 558
- previous: 558
- comment: 현재 558기 / 전주 대비 0기. ※후행지표(리그당생산량 24배↑) — 가중치 최소.

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
- score: 0.15
- price: 60.68
- ret_1w: -0.0026
- ret_1m: -0.0202
- ret_3m: 0.1372
- latest_date: 2026-05-27
- comment: $60.68 | 1W:-0.3% 1M:-2.0% 3M:+13.7% 세계1위 OCTG peer, 가격선행지표

### SeAH Wind ★
- name: SeAH Wind ★
- score: 1.0
- positive_news_count: 35
- negative_news_count: 0
- kr_news_count: 10
- en_news_count: 10
- comment: 긍정35/부정0건(21일) [영문10+한국어10건] | 영국CfD AR8·CIB 유일수혜. 수주잔고~2조, 26H2 매출인식.
- 뉴스:
  - Cadeler installs first complete monopile foundation at Hornsea 3 - Ocean Energy Resources
  - OnPath Energy Targets £1 bn Renewable Energy Investment in Scotland with 121 MW Wind Expansion - GreentechLead
  - News Content Hub - UK needs 5 GW of offshore wind every year to meet government goals - rivieramm.com
  - Homegrown policy must match homegrown energy ambition - Offshore Energies UK (OEUK)
  - Cadeler installs first complete monopile foundation at Ørsted’s Hornsea 3 offshore wind farm - BW Group

### Forward EPS/PER
- name: Forward EPS/PER
- score: 1.0
- cycle_label: 기본회복
- avg_cycle_score: 0.507
- base_eps: 45000
- wind_add_eps: 16000
- total_eps: 61000
- forward_per: 2.8
- scenarios: 저점=11.3x  약한=5.6x  기본=3.8x  강세=2.6x  슈퍼=1.9x
- comment: [기본회복] 업황0.51 → 본업45,000+Wind16,000=61,000원 → PER 2.8배

### 주가 돌파 신호
- name: 주가 돌파 신호
- score: 0.0
- near_52w_high: False
- volume_ratio_20d: 0.4541194705018338
- comment: 52주고가 98%+ & 거래량 2배+ 동시 충족 시 1.0

### US Proxy 주가군
- name: US Proxy 주가군
- score: 0.0
- score_1w: 0.0
- score_1m: 0.0
- positive_1w: 1/7
- positive_1m: 2/7
- ticker_returns: DNOW:+1%/+1%  TS:-0%/-2%  BKR:-3%/-6%  HAL:-8%/-3%  SLB:-0%/+2%  HP:-6%/-1%  PTEN:-10%/-3%
- comment: 1W 1/7상승(0.0) / 1M 2/7상승(0.0) → 0.0
