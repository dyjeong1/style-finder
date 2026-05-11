---
id: TSK-0006-업로드폰트재보정
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
업로드 카드의 안내 문구와 분석 버튼 문구가 실제 화면에서 과하게 크게 보이는 문제를 다시 보정합니다.

## 작업 내역
- [x] 업로드 안내 문구 체감 크기 축소
- [x] 업로드 분석 버튼 문구 체감 크기 축소
- [x] 브라우저 재검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `.sisyphus/plans/PLAN-20260510-화이트모드문서형리디자인.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/PLAN.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/SPEC.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0006-업로드폰트재보정/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0006-업로드폰트재보정/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 화면의 안내 문구와 버튼 크기 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 디자인 툴의 `pt` 표기와 웹 CSS의 `pt` 체감이 달라 실제 화면에서 더 크게 보일 수 있습니다.

## 완료 기준(DoD)
- [x] 주석 2건 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
