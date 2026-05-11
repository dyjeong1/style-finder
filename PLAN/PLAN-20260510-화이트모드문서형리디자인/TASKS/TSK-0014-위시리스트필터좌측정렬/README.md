---
id: TSK-0014-위시리스트필터좌측정렬
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
위시리스트 페이지의 카테고리, 정렬, 새로고침 버튼이 서로 너무 떨어져 보이지 않도록 좌측 정렬 묶음으로 정리합니다.

## 작업 내역
- [x] 위시리스트 툴바를 좌측 정렬로 변경
- [x] 필터와 새로고침 버튼 사이 간격 축소
- [x] `/wishlist` 화면 재검증
- [x] 문서 갱신 및 커밋

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `.sisyphus/plans/PLAN-20260510-화이트모드문서형리디자인.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/PLAN.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/SPEC.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0014-위시리스트필터좌측정렬/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0014-위시리스트필터좌측정렬/TODO.md`

## 테스트/검증
- in-app browser에서 `/wishlist` 툴바 정렬 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 모바일에서 줄바꿈될 때도 좌측 정렬이 자연스럽게 유지되는지 확인이 필요합니다.

## 완료 기준(DoD)
- [x] 사용자 요청 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
