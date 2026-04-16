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
