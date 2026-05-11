---
id: TSK-0001-업로드이미지실제응답
plan_id: PLAN-20260422-업로드이미지서빙보강
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-22
---

## 목적
최근 업로드 카드가 실제 업로드 이미지를 표시할 수 있도록 백엔드 이미지 응답 API와 프론트 URL 정규화를 추가한다.

## 작업 내역
- [x] 업로드 원본 bytes 저장
- [x] `GET /images/{upload_id}/file` 라우트 추가
- [x] 업로드 응답 이미지 URL을 실제 라우트로 변경
- [x] 프론트 이미지 URL 정규화 함수 추가
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/store.py`
  - `backend/src/api/routes/upload.py`
  - `backend/tests/test_api_e2e.py`
  - `frontend/lib/api.ts`
  - `frontend/app/(main)/upload/page.tsx`
- 문서:
  - `README.md`
  - `TODO.md`
  - `backend/README.md`
  - `frontend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` → 11 passed
- `cd frontend && npm run build` → 성공

## 의존성/리스크
- 백엔드 재시작 후 메모리 업로드 파일은 사라진다.
- 기존 최근 업로드 기록은 새 이미지 URL이 없어서 새 업로드부터 개선된다.

## 완료 기준(DoD)
- [x] 업로드 이미지 URL이 실제로 응답된다.
- [x] 최근 업로드 카드가 실제 이미지 URL 또는 생성 썸네일을 표시한다.
- [x] 테스트/빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
