---
id: TSK-0012-로딩문구폭확장
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
이미지 분석 중 표시되는 보조 문구가 잘려 보이지 않도록 로딩 오버레이의 문구 폭을 확장합니다.

## 작업 내역
- [x] 로딩 오버레이 보조 문구 폭 확장
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
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0012-로딩문구폭확장/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0012-로딩문구폭확장/TODO.md`

## 테스트/검증
- in-app browser에서 분석 중 오버레이 문구 줄바꿈 상태 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 폭을 넓혀도 모바일에서 넘치지 않도록 `min()` 기반으로 제한해야 합니다.

## 완료 기준(DoD)
- [x] 사용자 요청 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
