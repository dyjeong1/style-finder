---
id: TSK-0004-업로드진행시간노출
plan_id: PLAN-20260504-업로드로딩및소재검색강화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
업로드 버튼 내부 스피너를 제거하고, 버튼 아래에 실시간 진행 시간을 보여줘 사용자가 분석 진행 길이를 바로 알 수 있게 합니다.

## 작업 내역
- [x] 버튼 내부 스피너 제거
- [x] 버튼 아래 진행 시간 표시 추가
- [x] 테스트/문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/globals.css`
- `frontend/e2e/core-flow.spec.ts`

## 테스트/검증
- `cd frontend && npm run test:e2e:local -- --project=chromium -g '업로드 분석 중 버튼 상태와 진행 시간을 보여준다'`

## 의존성/리스크
- 실제 남은 시간은 예측할 수 없으므로, 사용자를 오도하지 않게 진행 시간 기준으로 보여줘야 합니다.

## 완료 기준(DoD)
- [x] 버튼 내부 스피너가 제거된다.
- [x] 업로드 진행 시간이 실시간으로 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
