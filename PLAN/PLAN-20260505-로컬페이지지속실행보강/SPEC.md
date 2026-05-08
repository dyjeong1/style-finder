---
id: PLAN-20260505-로컬페이지지속실행보강-SPEC
plan_id: PLAN-20260505-로컬페이지지속실행보강
status: done
created_at: 2026-05-05
updated_at: 2026-05-08
---

## 제품 동작 기준
1. `scripts/start-local-stack.sh`는 백엔드 `8000`과 프론트 `3000`을 함께 띄운다.
2. 이미 실행 중인 프로세스가 있으면 중복 실행 대신 기존 프로세스를 재사용한다.
3. `scripts/status-local-stack.sh`는 현재 실행 여부와 PID, 로그 경로를 보여준다.
4. `scripts/stop-local-stack.sh`는 두 프로세스를 안전하게 종료한다.
5. `/images/{upload_id}/file` 응답은 원본 파일명이 한글이어도 브라우저에서 안전하게 열린다.

## 구현 대상
- `scripts/start-local-stack.sh`
- `scripts/status-local-stack.sh`
- `scripts/stop-local-stack.sh`
- `.gitignore`
- `backend/src/api/routes/upload.py`
- `backend/tests/test_api_e2e.py`
- `README.md`
- `frontend/README.md`

## 테스트 기준
- 시작 스크립트 실행 후 `curl -s http://127.0.0.1:8000/health`가 성공한다.
- 시작 스크립트 실행 후 `curl -I -s http://127.0.0.1:3000/upload`가 성공한다.
- 상태/중지 스크립트가 기대 메시지를 반환한다.
- 한글 파일명으로 업로드한 뒤 `GET /images/{upload_id}/file`이 200과 안전한 `Content-Disposition` 헤더를 반환한다.
