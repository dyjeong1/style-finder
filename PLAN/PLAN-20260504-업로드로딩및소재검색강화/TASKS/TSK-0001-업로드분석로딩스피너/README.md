---
id: TSK-0001-업로드분석로딩스피너
plan_id: PLAN-20260504-업로드로딩및소재검색강화
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-04
---

## 목적
업로드 분석이 길어질 때도 사용자가 진행 중임을 바로 알 수 있도록 스피너와 진행 안내를 추가합니다.

## 작업 내역
- [x] 업로드 중 스피너 UI 추가
- [x] 진행 안내 문구 추가
- [x] 관련 테스트/문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/globals.css`
- `frontend/e2e/core-flow.spec.ts`

## 테스트/검증
- `cd frontend && npm run test:e2e -- --project=chromium -g '업로드 분석이 지연되면 스피너와 진행 안내를 보여준다'`

## 의존성/리스크
- 업로드 완료 직후 추천 페이지로 이동하므로, 스피너는 요청 중에만 자연스럽게 보여야 합니다.

## 완료 기준(DoD)
- [x] 업로드 분석 중 진행 상태가 명확하게 노출된다.
- [x] 테스트가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
