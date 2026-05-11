---
id: TSK-0013-필터셀렉트UI통일
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
추천/위시리스트 등 필터 영역의 `select` UI를 가격 입력창과 동일한 스타일 톤으로 통일합니다.

## 작업 내역
- [x] 브라우저 기본 `select` 렌더링 제거
- [x] 공통 필터 박스 스타일과 맞는 커스텀 화살표 적용
- [x] `/recommendations`, `/wishlist` 기준 재검증
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
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0013-필터셀렉트UI통일/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0013-필터셀렉트UI통일/TODO.md`

## 테스트/검증
- in-app browser에서 `/recommendations`, `/wishlist` 필터 셀렉트 UI 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 전역 `select` 스타일을 바꾸므로 다른 페이지의 셀렉트도 동일 룩으로 바뀝니다.

## 완료 기준(DoD)
- [x] 사용자 요청 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
