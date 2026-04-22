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

## 업로드 이미지 파일 응답
- 업로드 응답의 `image_url`은 `/images/{uploaded_image_id}/file`입니다.
- 해당 URL은 업로드 원본 bytes를 `content_type`과 함께 반환합니다.
- 현재 로컬 단일 사용자 모드에서는 업로드 파일을 메모리에 보관하므로 백엔드 재시작 후 이전 업로드 파일은 사라질 수 있습니다.
