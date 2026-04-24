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

## AI 비전 기반 착장 분석기 (초기 구조)
- 현재 업로드 분석은 기본적으로 규칙 기반으로 동작합니다.
- 여기에 AI 비전 모델을 붙일 수 있도록 `vision_outfit_analyzer` 인터페이스가 추가되었습니다.
- 지금 단계에서는 `disabled`와 `mock` provider만 지원하며, 실제 모델 연결은 다음 PLAN/TASK에서 이어집니다.
- 비전 결과가 일부만 있으면 해당 카테고리만 우선 적용하고, 나머지는 규칙 기반 결과로 fallback 합니다.

주요 설정:
- `VISION_OUTFIT_ANALYZER_ENABLED`
- `VISION_OUTFIT_ANALYZER_PROVIDER`
- `VISION_OUTFIT_ANALYZER_MODEL_NAME`
- `VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES`

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

현재 로컬 데이터셋(11샘플) 기준 첫 측정값:
- 아이템 정밀도: `0.2500`
- 아이템 재현율: `0.2281`
- 샘플 완전일치율: `0.0000`

## 업로드 이미지 파일 응답
- 업로드 응답의 `image_url`은 `/images/{uploaded_image_id}/file`입니다.
- 해당 URL은 업로드 원본 bytes를 `content_type`과 함께 반환합니다.
- 현재 로컬 단일 사용자 모드에서는 업로드 파일을 메모리에 보관하므로 백엔드 재시작 후 이전 업로드 파일은 사라질 수 있습니다.

## 추천 카테고리 다양화
- 추천 전체 보기에서는 네이버 쇼핑 후보를 상의/하의/아우터/신발/가방 카테고리별로 나누어 조회합니다.
- 카테고리 필터를 선택하면 해당 카테고리만 조회합니다.
- 응답의 `query`는 전체 보기에서 카테고리별 검색어를 `/`로 연결해 표시합니다.
