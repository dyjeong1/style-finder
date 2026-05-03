# 로컬 Ollama 설치 가이드

이 문서는 이 저장소에서 `Ollama + gemma3:4b` 조합으로 로컬 비전 분석을 바로 확인할 수 있게 설치부터 점검까지 한 번에 정리한 안내서입니다.

## 1. 권장 기준
- 기본 권장 경로: `Ollama + gemma3:4b`
- 사용 목적:
  - 로컬 무료 반복 실험
  - `backend/src/services/vision_outfit_analyzer.py`의 `ollama` provider 확인
  - 업로드 분석 CLI와 데이터셋 비교 스크립트 실행
- 전제:
  - macOS 로컬 개발 환경
  - 이 저장소를 이미 내려받은 상태

## 2. 설치

### macOS(Homebrew)
```bash
brew install --cask ollama
```

### macOS(공식 앱)
- [Ollama 공식 사이트](https://ollama.com)에서 macOS 앱을 설치합니다.
- 설치 후 한 번 실행해 권한 안내와 초기 런타임 구동을 마칩니다.

## 3. 모델 pull

이 저장소의 기본 권장 모델은 `gemma3:4b`입니다.

```bash
ollama pull gemma3:4b
```

설치된 모델 확인:

```bash
ollama list
```

정상 예시:
- 목록에 `gemma3:4b`가 보입니다.

## 4. 서버 실행

터미널에서 직접 실행:

```bash
ollama serve
```

또는:
- Ollama 데스크톱 앱을 실행해 백그라운드 서버를 켭니다.

기본 API 엔드포인트:
- `http://127.0.0.1:11434/api/chat`

간단 확인:

```bash
curl http://127.0.0.1:11434/api/tags
```

정상 예시:
- JSON 응답이 오고 `gemma3:4b`가 목록에 포함됩니다.

## 5. 저장소 설정

백엔드 설정 파일을 준비합니다.

```bash
cd backend
cp .env.example .env
```

`.env`에서 최소 권장값:

```env
OLLAMA_VISION_ENABLED=true
OLLAMA_VISION_PROVIDER=ollama
OLLAMA_VISION_MODEL=gemma3:4b
OLLAMA_API_BASE_URL=http://127.0.0.1:11434/api/chat
OLLAMA_VISION_TIMEOUT_SECONDS=90.0
```

필요하면 함께 확인할 값:
- `VISION_OUTFIT_ANALYZER_ENABLED`
- `VISION_OUTFIT_ANALYZER_PROVIDER`
- `GEMINI_CORRECTION_ENABLED`

운영 메모:
- 현재 런타임은 `backend/.env`를 기준으로 읽습니다.
- `ollama` provider 사용 시 `OLLAMA_VISION_MODEL`, `OLLAMA_API_BASE_URL`이 공통 `VISION_*`보다 우선 적용됩니다.

## 6. 단일 이미지 확인

가장 빠른 점검 명령:

```bash
cd backend
PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama
```

타임아웃을 더 넉넉하게 보고 싶으면:

```bash
cd backend
PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120
```

정상 예시:
- JSON 출력이 나오고 `analysis` 안에 `dominant_tone`, `style_mood`, `preferred_categories`, `detected_items`가 채워집니다.

## 7. 데이터셋 비교

규칙 기반과 로컬 Ollama를 비교:

```bash
cd backend
PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --format text
```

한 샘플만 빠르게 확인:

```bash
cd backend
PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --sample-ids codytest_2 --format text
```

실제 런타임 순서와 같은 경로(`ollama -> 선택적 gemini 보정 -> rule fallback`) 비교:

```bash
cd backend
PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate runtime-ollama+gemini --format text
```

## 8. 프론트까지 같이 보기

백엔드:

```bash
cd backend
./scripts/run-dev.sh
```

프론트:

```bash
cd frontend
npm run local
```

그 다음:
- `/upload`에서 이미지를 올립니다.
- 추천 페이지에서 `AI 분석 기준`과 업로드 분석 요약이 기대대로 보이는지 확인합니다.

## 9. 자주 겪는 문제

### `connection refused` 또는 provider unavailable
- `ollama serve`가 꺼져 있을 수 있습니다.
- 데스크톱 앱이 종료되었는지 확인합니다.
- `OLLAMA_API_BASE_URL`이 `http://127.0.0.1:11434/api/chat`인지 확인합니다.

### 모델을 찾을 수 없음
- `ollama list`에서 `gemma3:4b`가 보이는지 확인합니다.
- 없다면 다시 실행합니다:

```bash
ollama pull gemma3:4b
```

### 응답이 너무 느리거나 타임아웃
- 먼저 단일 샘플로 확인합니다.
- `--timeout-seconds 120`으로 늘려 봅니다.
- 동시에 여러 비교를 돌리기보다 `--sample-ids`로 좁혀 점검합니다.

### 여전히 규칙 fallback으로만 보임
- `.env`에서 `OLLAMA_VISION_ENABLED=true`인지 확인합니다.
- 백엔드를 재시작합니다.
- `scripts/check_upload_analysis.py --provider ollama`로 직접 결과가 나오는지 먼저 확인합니다.

## 10. 권장 순서 요약

처음 셋업할 때는 아래 순서만 따라가면 됩니다.

```bash
brew install --cask ollama
ollama pull gemma3:4b
ollama serve
cd backend
cp .env.example .env
PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama
```

이 단계가 통과하면 그 다음부터는:
- 백엔드 실행
- 프론트 실행
- `/upload` 실제 업로드 확인
- 필요 시 `compare_vision_predictors.py`로 정밀 비교

