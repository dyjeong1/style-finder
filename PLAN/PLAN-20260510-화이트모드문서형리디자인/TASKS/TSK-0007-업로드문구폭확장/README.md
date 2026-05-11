---
id: TSK-0007-업로드문구폭확장
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
업로드 안내 문구 영역의 가로 폭이 너무 좁아 줄바꿈이 과하게 생기는 문제를 보정합니다.

## 작업 내역
- [x] 업로드 안내 `span`의 가로 폭을 300px 기준으로 확장
- [x] `/upload` 화면 재검증
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
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0007-업로드문구폭확장/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0007-업로드문구폭확장/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 화면의 안내 문구 줄바꿈 상태 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 폭을 고정값에 가깝게 넓히되 모바일에서 넘치지 않도록 `min()` 처리해야 합니다.

## 완료 기준(DoD)
- [x] 주석 1건 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
