---
id: TSK-0005-새로고침아이콘및폰트보정
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-05-10
---

## 목적
업로드 카드의 안내 문구/버튼 폰트를 보정하고, 추천/위시리스트의 `새로고침` 버튼을 아이콘 형태로 단순화합니다.

## 작업 내역
- [x] 업로드 안내 문구 폰트 크기 18pt 기준 유지/보정
- [x] 업로드 분석 버튼 문구 폰트 크기 20pt로 조정
- [x] 추천/위시리스트의 `새로고침` 텍스트 버튼을 아이콘 버튼으로 교체
- [x] 브라우저 재검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/(main)/wishlist/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `.sisyphus/plans/PLAN-20260510-화이트모드문서형리디자인.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/PLAN.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/SPEC.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0005-새로고침아이콘및폰트보정/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0005-새로고침아이콘및폰트보정/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload`, `/recommendations`, `/wishlist` 버튼 표현 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 아이콘 버튼으로 바꿀 때 텍스트가 사라지므로 `aria-label`로 접근성을 유지해야 합니다.

## 완료 기준(DoD)
- [x] 주석 4건 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
