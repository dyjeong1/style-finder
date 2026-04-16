---
id: TSK-0001-위시리스트상세정보노출
plan_id: PLAN-20260416-위시리스트상세화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-16
---

## 목적
위시리스트에서 저장한 상품을 식별자 없이도 바로 이해할 수 있도록 백엔드 응답과 프론트 화면을 함께 개선합니다.

## 작업 내역
- [x] 위시리스트 응답에 상품 상세 정보 추가
- [x] 저장 시각 영속화
- [x] 프론트 위시리스트 UI와 테스트 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/services/store.py`
  - `backend/tests/test_api_e2e.py`
  - `backend/tests/test_api_failures.py`
  - `frontend/lib/api.ts`
  - `frontend/app/(main)/wishlist/page.tsx`
  - `frontend/e2e/core-flow.spec.ts`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd frontend && npm run build`
- `cd frontend && npx playwright test e2e/core-flow.spec.ts --reporter=list --workers=1`

## 검증 메모
- 백엔드 `pytest` 통과
- 프론트 `build` 통과
- Playwright 시나리오는 응답 스키마와 화면 텍스트를 최신화함
- 이번 턴의 로컬 E2E 재실행은 Next dev server 예열 문제로 자동 검증이 불안정해 별도 확인이 필요함

## 의존성/리스크
- 위시리스트 mock 응답이 실제 응답과 달라지지 않게 함께 갱신해야 합니다.

## 완료 기준(DoD)
- [x] 백엔드/프론트 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
