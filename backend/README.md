# Backend Scaffold (FastAPI)

## 실행 준비
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 개발 서버 실행
```bash
./scripts/run-dev.sh
```

## 헬스체크
- `GET /health`
- 예시: `curl http://localhost:8000/health`

## 로컬 실행 모드
- 현재 백엔드는 단일 사용자 로컬 모드로 동작합니다.
- 로그인 없이 업로드, 추천, 찜 API를 바로 호출할 수 있습니다.

## 구현된 주요 엔드포인트
- `POST /images/upload`
- `GET /recommendations`
- `GET /wishlist`
- `POST /wishlist`
- `DELETE /wishlist/{product_id}`

## 네이버 쇼핑 검색 API 연동
- 추천 API는 네이버 쇼핑 검색 API 키가 있으면 실제 네이버 쇼핑 상품 후보를 조회합니다.
- 키가 없거나 호출에 실패하면 기존 샘플 상품 데이터로 자동 fallback 합니다.
- 호출 실패 시 응답에 `fallback_reason`, `fallback_message`를 포함해 인증 실패/네트워크 오류 등을 확인할 수 있습니다.
- 설정 파일 예시는 `backend/.env.example`을 참고하세요.

```bash
cd backend
cp .env.example .env
# .env에 NAVER_SHOPPING_CLIENT_ID, NAVER_SHOPPING_CLIENT_SECRET 입력
```

사용하는 주요 설정:
- `NAVER_SHOPPING_CLIENT_ID`
- `NAVER_SHOPPING_CLIENT_SECRET`
- `NAVER_SHOPPING_DISPLAY`
- `NAVER_SHOPPING_TIMEOUT_SECONDS`

## 선택적 CLIP 비전 재정렬
- 기본 추천은 휴리스틱/색상/텍스트 점수로 동작합니다.
- 추가로 CLIP 기반 이미지 임베딩 재정렬을 켜면 업로드 이미지와 상품 이미지의 시각 유사도를 더 반영할 수 있습니다.
- 패키지가 없거나 비활성화되어 있으면 자동으로 기존 점수 체계로 fallback 합니다.

설치 예시:
```bash
cd backend
pip install -e ".[vision]"
```

주요 설정:
- `VISION_RERANKER_ENABLED=true`
- `VISION_RERANKER_PROVIDER=clip`
- `VISION_RERANKER_MODEL_NAME=openai/clip-vit-base-patch32`
- `VISION_RERANKER_TIMEOUT_SECONDS=1.5`
- `VISION_RERANKER_MAX_IMAGE_BYTES=2000000`
- `VISION_RERANKER_MAX_CANDIDATES=10`

## AI 비전 기반 착장 분석기
- 현재 업로드 분석은 기본적으로 규칙 기반으로 동작합니다.
- 여기에 AI 비전 모델을 붙일 수 있도록 `vision_outfit_analyzer` 인터페이스가 추가되었습니다.
- 현재는 `disabled`, `mock`, `openai`, `gemini`, `ollama` provider를 지원합니다.
- 비전 결과가 일부만 있으면 해당 카테고리만 우선 적용하고, 나머지는 규칙 기반 결과로 fallback 합니다.
- OpenAI 호출이 실패하거나 응답이 비어 있으면 업로드 분석은 자동으로 기존 규칙 기반으로 fallback 합니다.
- Gemini 호출이 실패하거나 응답이 비어 있어도 동일하게 규칙 기반으로 fallback 합니다.
- Ollama 로컬 호출이 실패하거나 서버가 꺼져 있어도 동일하게 규칙 기반으로 fallback 합니다.

주요 설정:
- `VISION_OUTFIT_ANALYZER_ENABLED`
- `VISION_OUTFIT_ANALYZER_PROVIDER`
- `VISION_OUTFIT_ANALYZER_MODEL_NAME`
- `VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES`
- `VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS`
- `OPENAI_API_KEY`

OpenAI 호환 별칭 설정:
- `OPENAI_VISION_ENABLED`
- `OPENAI_VISION_PROVIDER`
- `OPENAI_VISION_MODEL`
- `OPENAI_VISION_MAX_IMAGE_BYTES`
- `OPENAI_VISION_TIMEOUT_SECONDS`

Gemini 호환 별칭 설정:
- `GEMINI_API_KEY`
- `GEMINI_VISION_ENABLED`
- `GEMINI_VISION_PROVIDER`
- `GEMINI_VISION_MODEL`
- `GEMINI_VISION_MAX_IMAGE_BYTES`
- `GEMINI_VISION_TIMEOUT_SECONDS`

Ollama 호환 별칭 설정:
- `OLLAMA_API_KEY`
- `OLLAMA_VISION_ENABLED`
- `OLLAMA_VISION_PROVIDER`
- `OLLAMA_VISION_MODEL`
- `OLLAMA_VISION_MAX_IMAGE_BYTES`
- `OLLAMA_VISION_TIMEOUT_SECONDS`
- `OLLAMA_API_BASE_URL`

OpenAI Vision 예시:
```bash
cd backend
cp .env.example .env
# .env에 아래 값을 입력
# OPENAI_API_KEY=sk-...
# OPENAI_VISION_ENABLED=true
# OPENAI_VISION_PROVIDER=openai
# OPENAI_VISION_MODEL=gpt-4o
```

Gemini Vision 예시:
```bash
cd backend
cp .env.example .env
# .env에 아래 값을 입력
# GEMINI_API_KEY=...
# GEMINI_VISION_ENABLED=true
# GEMINI_VISION_PROVIDER=gemini
# GEMINI_VISION_MODEL=gemini-2.5-flash
```

선택적 Gemini 보정 예시:
```bash
cd backend
cp .env.example .env
# .env에 아래 값을 입력
# VISION_OUTFIT_ANALYZER_ENABLED=true
# VISION_OUTFIT_ANALYZER_PROVIDER=ollama
# OLLAMA_VISION_MODEL=gemma3:4b
# GEMINI_API_KEY=...
# GEMINI_CORRECTION_ENABLED=true
```

Ollama Vision 예시:
```bash
cd backend
cp .env.example .env
# .env에 아래 값을 입력
# OLLAMA_VISION_ENABLED=true
# OLLAMA_VISION_PROVIDER=ollama
# OLLAMA_VISION_MODEL=gemma3:4b
# OLLAMA_API_BASE_URL=http://127.0.0.1:11434/api/chat
```

Ollama 실행 메모:
- 먼저 로컬에 Ollama를 설치한 뒤 `ollama pull gemma3:4b`를 실행합니다.
- 그 다음 `ollama serve` 또는 데스크톱 앱으로 로컬 서버를 켭니다.
- 이 저장소 기준 기본 권장 로컬 무료 경로는 `Ollama + gemma3:4b`입니다.

실호출 메모:
- Gemini `generateContent`는 구조화 출력 시 `responseJsonSchema` 형식을 사용한다.
- 2026-04-27 로컬 검증에서 `codytest_2.jpg`는 `하늘색 라운드넥 가디건`, `화이트 나시탑`, `블랙 스티치 와이드 팬츠`, `블랙 안경테`, `블랙 링 귀걸이`로 분석되었다.

개인 비상업 프로젝트 메모:
- 비용이 민감하면 OpenAI보다 Gemini 무료 티어를 우선 추천합니다.
- 단, 무료 티어도 호출량 한도와 정책 제한은 있으니 실제 운영 전에는 Google AI Studio의 quota/billing 상태를 확인해야 합니다.
- 반복 실험량이 많으면 Gemini보다 `Ollama + gemma3:4b` 조합을 우선 추천합니다.
- 2026-04-29 로컬 검증에서 `codytest_2.jpg`는 `화이트 셔츠`, `회색 가디건`, `청바지 팬츠`, `검정 선글라스`로 응답했고, 단일 샘플 비교도 timeout 없이 완료되었습니다.
- 이후 경량 모델 후처리 정규화를 추가해 같은 샘플의 하의/악세서리 표현을 `블루 데님 팬츠`, `블랙 안경` 형태로 표준화했습니다.
- 3-way 비교 기준 현재 성능 순위는 `gemini > ollama(gemma3:4b) > rule`이며, `ollama` 비교를 fresh 실행하려면 `--no-cache` 옵션을 사용합니다.
- 2026-04-29 하이브리드 병합 보정으로 AI 결과를 규칙 기반 fallback과 제한적으로 재조정하도록 보강했고, `codytest_2.jpg`는 `화이트 셔츠 / 블루 가디건 / 블랙 데님 팬츠 / 블랙 안경`으로 정리되었습니다.
- 2026-04-29 선택적 Gemini 보정 경로를 추가해, Ollama 결과가 모호한 카테고리에만 Gemini를 보조 호출하도록 했습니다.
- 같은 날 `codytest_2.jpg`는 `화이트 슬리브리스 탑 / 블루 가디건 / 블랙 와이드 팬츠 / 블랙 안경 / 블랙 귀걸이`, `codytest_3.png`는 `화이트 티셔츠 / 블루 가디건 / 브라운 와이드 팬츠 / 화이트 운동화` 수준으로 개선되는 것을 확인했습니다.
- 2026-04-29 가방/하의 generic 품목 정교화를 추가해 `운동화 -> 스니커즈`, `가방 -> 숄더백` 같은 보정을 적용했고, `codytest_3.png`는 `브라운 숄더백 / 화이트 스니커즈 / 브라운 팬츠` 수준까지 개선됐습니다.
- 2026-04-29 액세서리 세부명/색상 정교화를 추가해 `체인 팔찌 -> 팔찌` 정규화와 주얼리 accessory의 `unknown -> gray` 보정을 적용했고, `codytest_3.png`는 `그레이 팔찌 / 그레이 목걸이` 수준까지 개선됐습니다.
- 2026-04-29 액세서리 우선순위와 금속 톤 검색어를 정리해 주얼리 `gray/yellow` 검색어를 `실버/골드`로 노출하고, `codytest_3.png`는 `실버 목걸이 / 실버 팔찌 / 실버 반지 / 화이트 양말` 순서로 정리되는 것을 확인했습니다.

데이터셋 경로:
- `backend/data/vision_dataset/images/`
- `backend/data/vision_dataset/labels/`

## 비전 데이터셋 평가
- 현재 분석기 성능은 로컬 데이터셋 기준으로 바로 평가할 수 있습니다.
- 정답 라벨이 있는 이미지셋을 `backend/data/vision_dataset/`에 넣은 뒤 아래 명령으로 실행합니다.

```bash
cd backend
PYTHONPATH=. python3 scripts/evaluate_vision_dataset.py
```

JSON 출력:
```bash
cd backend
PYTHONPATH=. python3 scripts/evaluate_vision_dataset.py --format json
```

규칙 기반 vs AI 비교:
```bash
cd backend
PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate gemini --format text
```

Ollama 비교 예시:
```bash
cd backend
PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --format text
```

비교 스크립트 메모:
- Gemini 비교는 `backend/data/vision_dataset/cache/gemini.json`에 샘플별 응답 캐시를 남긴다.
- Ollama 비교는 `backend/data/vision_dataset/cache/ollama.json`에 샘플별 응답 캐시를 남긴다.
- 기본적으로 Gemini 무료 티어 제한을 고려해 요청 간 대기와 재시도를 적용한다.
- Ollama는 로컬 서버라 기본적으로 추가 대기 없이 실행한다.
- 2026-04-27 기준 무료 티어 일일 한도로 인해 3샘플 캐시까지만 확보되었다.

현재 로컬 데이터셋(11샘플) 기준 첫 측정값:
- 아이템 정밀도: `0.2500`
- 아이템 재현율: `0.2281`
- 샘플 완전일치율: `0.0000`

## 업로드 이미지 파일 응답
- 업로드 응답의 `image_url`은 `/images/{uploaded_image_id}/file`입니다.
- 추천 fallback은 초기 샘플 카탈로그만 사용하며, 이전 업로드에서 등록된 외부 상품 후보는 다음 업로드 기본 추천에 재사용되지 않습니다.
- 해당 URL은 업로드 원본 bytes를 `content_type`과 함께 반환합니다.
- 현재 로컬 단일 사용자 모드에서는 업로드 파일을 메모리에 보관하므로 백엔드 재시작 후 이전 업로드 파일은 사라질 수 있습니다.

## 추천 카테고리 다양화
- 추천 전체 보기에서는 네이버 쇼핑 후보를 상의/하의/아우터/신발/가방 카테고리별로 나누어 조회합니다.
- 카테고리 필터를 선택하면 해당 카테고리만 조회합니다.
- 응답의 `query`는 전체 보기에서 카테고리별 검색어를 `/`로 연결해 표시합니다.
