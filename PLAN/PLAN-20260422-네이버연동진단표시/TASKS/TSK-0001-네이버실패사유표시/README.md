---
id: TSK-0001-네이버실패사유표시
plan_id: PLAN-20260422-네이버연동진단표시
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-22
---

## 목적
네이버 쇼핑 검색 API가 실패해 샘플 데이터로 fallback될 때 원인을 추천 API와 화면에서 확인할 수 있게 한다.

## 작업 내역
- [x] 네이버 쇼핑 클라이언트에 진단 결과 타입 추가
- [x] 추천 API 응답에 fallback 사유/메시지 추가
- [x] 추천 페이지에서 fallback 안내 표시
- [x] 테스트 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/services/naver_shopping.py`
  - `backend/src/api/routes/recommendation.py`
  - `frontend/lib/api.ts`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` → 11 passed
- `cd frontend && npm run build` → 성공
- 로컬 네이버 호출 진단 결과: `fallback_reason=auth_failed`

## 의존성/리스크
- 네이버 API 키는 사용자가 로컬 `.env`에 직접 관리한다.
- 실패 메시지는 민감정보를 노출하지 않는 범위에서만 표시한다.

## 완료 기준(DoD)
- [x] 네이버 실패 사유가 추천 응답에 포함된다.
- [x] 추천 페이지에 안내 문구가 보인다.
- [x] 백엔드 테스트와 프론트 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
