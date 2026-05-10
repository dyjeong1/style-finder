---
id: TSK-0011-업로드버튼간격32보정
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
업로드 영역과 `이미지 분석하기` 버튼 사이 간격이 과하게 넓어 보이는 문제를 약 32px 수준으로 보정합니다.

## 작업 내역
- [x] 업로드 프레임의 과도한 최소 높이를 제거
- [x] 업로드 영역과 버튼 사이 간격을 32px 기준으로 재조정
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
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0011-업로드버튼간격32보정/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0011-업로드버튼간격32보정/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 화면의 업로드 영역과 버튼 사이 간격 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 프레임 최소 높이를 제거하면 데스크톱 레이아웃의 세로 여백 균형이 달라질 수 있으므로 실제 화면 확인이 필요합니다.

## 완료 기준(DoD)
- [x] 사용자 요청 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
