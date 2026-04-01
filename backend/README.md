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
