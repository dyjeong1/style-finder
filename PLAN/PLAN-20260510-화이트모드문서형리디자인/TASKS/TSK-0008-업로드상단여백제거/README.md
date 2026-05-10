---
id: TSK-0008-업로드상단여백제거
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-05-10
---

## 목적
업로드 카드에서 `이미지로 상품 찾기` 제목 아래 여백이 과하게 넓어 보이는 문제를 제거합니다.

## 작업 내역
- [x] 업로드 프레임 그리드 정렬을 상단 기준으로 보정
- [x] 제목과 드롭존 사이 간격 축소
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
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0008-업로드상단여백제거/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0008-업로드상단여백제거/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 화면의 제목 아래 여백 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 그리드 정렬 방식이 바뀌므로 미리보기 상태에서도 상단 정렬이 자연스러운지 함께 봐야 합니다.

## 완료 기준(DoD)
- [x] 사용자 피드백 1건 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
