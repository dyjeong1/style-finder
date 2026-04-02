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

## 개발용 로그인 계정
- email: `admin@stylematch.com`
- password: `stylematch1234`

## 구현된 주요 엔드포인트
- `POST /auth/login`
- `POST /images/upload` (Bearer 필요)
- `GET /recommendations` (Bearer 필요)
- `GET /wishlist` (Bearer 필요)
- `POST /wishlist` (Bearer 필요)
- `DELETE /wishlist/{product_id}` (Bearer 필요)
