---
id: TSK-0003-스피너가시성보정
plan_id: PLAN-20260504-업로드로딩및소재검색강화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
업로드 요청이 빨라도 스피너가 실제로 보이도록 렌더 타이밍과 최소 노출 시간을 보정합니다.

## 작업 내역
- [x] 업로드 상태 즉시 렌더 보장
- [x] 스피너 최소 노출 시간 추가
- [x] 회귀 테스트/문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/app/(main)/upload/page.tsx`
- `frontend/e2e/core-flow.spec.ts`

## 테스트/검증
- `cd frontend && npm run test:e2e -- --project=chromium -g '업로드 분석 중 스피너와 진행 안내를 보여준다'`

## 의존성/리스크
- 최소 노출 시간을 너무 길게 잡으면 업로드가 끝났어도 느리게 느껴질 수 있어 짧고 안정적인 값으로 제한해야 합니다.

## 완료 기준(DoD)
- [x] 빠른 응답에서도 스피너가 체감 가능하게 노출된다.
- [x] 회귀 테스트가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
