---
id: TSK-0009-업로드버튼간격재조정
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
업로드 화면에서 제목 아래 간격은 유지하면서, 업로드 영역과 `이미지 분석하기` 버튼 사이 여백만 더 좁게 조정합니다.

## 작업 내역
- [x] 제목 아래 `gap`을 18px로 복원
- [x] 업로드 영역과 분석 버튼 사이 간격 축소
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
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0009-업로드버튼간격재조정/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0009-업로드버튼간격재조정/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 화면의 제목 아래 간격과 버튼 위치 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 버튼을 너무 위로 당기면 드롭존 하단 여백과 충돌할 수 있어 미세한 음수 마진만 적용해야 합니다.

## 완료 기준(DoD)
- [x] 사용자 요청 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
