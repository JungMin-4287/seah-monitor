# 세아제강지주 일일 업황 모니터

세아제강지주 투자 논리를 매일 점수화하는 간단한 모니터링 코드입니다.

## 확인하는 지표

1. 미국 Pipe/OCTG 가격 proxy
   - FRED/BLS `WPU10170652` 탄소강 파이프 PPI 사용
   - 실제 OCTG spot price가 아니라 무료 대체지표입니다.

2. 미국 Rig Count proxy
   - Baker Hughes rig count 관련 뉴스에서 숫자를 보조 추출합니다.
   - 첫 실행 또는 뉴스 문구가 달라지는 경우 수동 검증이 필요합니다.

3. SeAH Steel USA 가동률 proxy
   - SeAH Steel USA, OCTG, line pipe, utilization 뉴스 검색

4. ADNOC·중동 수주 proxy
   - ADNOC, XRG, Hail & Ghasha, line pipe, clad pipe 뉴스 검색

5. 아프리카 LNG·해상 개발 proxy
   - Rovuma LNG, Mozambique LNG, Namibia FPSO, Venus, Mopane, Nigeria LNG Train 8 뉴스 검색

6. 2026E EPS / Forward PER
   - `config.yaml`의 `forecast_eps`를 사용합니다.

7. 주가·거래량 추세
   - yfinance `003030.KS` 기준 52주 고가권과 20일 평균 거래량 대비 배율을 확인합니다.

## 로컬 실행

```bash
pip install -r requirements.txt
python seah_daily_monitor.py
```

윈도우에서는 `run_windows.bat`를 더블클릭해도 됩니다.

## 결과물

실행 후 아래 파일이 생성됩니다.

- `data/seah_daily_report.md`: 일일 리포트
- `data/seah_daily_history.csv`: 일별 점수 히스토리
- `data/state.json`: rig count 비교용 상태값

## GitHub Actions 자동 실행

이 저장소는 `.github/workflows/seah-monitor.yml`로 평일 한국시간 오전 7시 30분에 자동 실행됩니다.

1. Actions 탭에서 workflow 허용
2. 필요 시 `config.yaml` 수정
3. 실행 결과는 `data/seah_daily_report.md`에 자동 커밋

## 텔레그램 알림 선택 사항

`config.yaml`에서 아래를 true로 바꿉니다.

```yaml
telegram:
  enabled: true
```

GitHub Repository Settings → Secrets and variables → Actions에서 다음 2개를 추가합니다.

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## 점수 해석

| 종합점수 | 해석 |
|---:|---|
| 75점 이상 | 강세 확인: 추세추종 보유/추가 검토 |
| 60~75점 | 우호적: 보유 우위, 돌파·거래량 확인 |
| 45~60점 | 중립: 모멘텀 확인 필요 |
| 45점 미만 | 약세: 테마 약화 또는 실적 확인 전 |

## 중요한 한계

- OCTG 직접 가격은 무료 데이터로 완전히 대체하기 어렵습니다. Argus, Pipe Logix 같은 유료 데이터가 더 정확합니다.
- SeAH Steel USA 가동률은 회사가 매일 공시하지 않으므로 뉴스 proxy를 사용합니다.
- 2026E EPS는 자동 컨센서스가 아니라 사용자가 `config.yaml`에서 직접 조정하는 방식입니다.
- 이 코드는 투자판단 보조 도구입니다. 매수·매도 추천이 아닙니다.
