---
id: TSK-0002-로컬페이지기동복구
plan_id: PLAN-20260505-로컬페이지지속실행보강
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-08
---

## 목적
누락된 로컬 실행 스크립트와 PLAN 문서를 복구하고, 업로드 이미지 원본 파일명이 한글일 때도 페이지가 깨지지 않도록 업로드 파일 응답을 안전화합니다.

## 작업 내역
- [x] 삭제된 로컬 실행 스크립트 3종 복구
- [x] 삭제된 PLAN/SPEC/.sisyphus PLAN 문서 복구
- [x] `.local-runtime/` 재무시 처리
- [x] 업로드 이미지 `Content-Disposition` 헤더 안전화
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- `scripts/start-local-stack.sh`
- `scripts/status-local-stack.sh`
- `scripts/stop-local-stack.sh`
- `.gitignore`
- `backend/src/api/routes/upload.py`
- `backend/tests/test_api_e2e.py`
- `PLAN/PLAN-20260505-로컬페이지지속실행보강/PLAN.md`
- `PLAN/PLAN-20260505-로컬페이지지속실행보강/SPEC.md`
- `PLAN/PLAN-20260505-로컬페이지지속실행보강/TASKS/TSK-0002-로컬페이지기동복구/*`
- `.sisyphus/plans/PLAN-20260505-로컬페이지지속실행보강.md`
- `README.md`
- `TODO.md`

## 테스트/검증
- `./scripts/start-local-stack.sh`
- `curl -s http://127.0.0.1:8000/health`
- `curl -I -s http://127.0.0.1:3000/upload`
- `cd backend && pytest tests/test_api_e2e.py`
- `./scripts/status-local-stack.sh`
- `./scripts/stop-local-stack.sh`

## 의존성/리스크
- 프론트는 Node/npm, 백엔드는 Python 실행 환경에 의존합니다.
- 브라우저 업로드 원본 파일명이 비 ASCII 문자를 포함하면 응답 헤더 인코딩을 별도 처리해야 합니다.

## 완료 기준(DoD)
- [x] 로컬 시작/상태/중지 스크립트가 다시 동작한다.
- [x] 페이지가 실제로 열린다.
- [x] 한글 파일명 업로드 이미지 응답이 500 없이 반환된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서 갱신
