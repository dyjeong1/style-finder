---
id: TSK-0002-최근업로드재사용UI복원
plan_id: PLAN-20260504-최근업로드이미지재사용복원
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-04
---

## 목적
저장된 업로드 이미지를 `/upload` 화면에서 다시 선택 없이 재사용할 수 있도록 최근 업로드 목록 UI와 재분석 흐름을 복원한다.

## 작업 내역
- [x] 최근 업로드 목록 렌더링 추가
- [x] 카드 클릭 시 저장된 이미지 재업로드 연결
- [x] 카드 삭제/빈 상태/에러 처리 추가
- [x] E2E 검증 및 문서 반영

## 산출물(Artifacts)
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/globals.css`
- `frontend/e2e/core-flow.spec.ts`

## 테스트/검증
- `cd frontend && npm run test:e2e:local -- --project=chromium -g '최근 업로드 이미지를 다시 눌러 새 분석을 시작할 수 있다|업로드 분석 중 버튼 상태와 진행 시간을 보여준다'` 통과
- `/upload`에서 최근 업로드 카드 렌더링 및 카드 클릭 재분석 흐름 확인

## 의존성/리스크
- 카드 클릭 시 새 분석을 다시 수행하므로 업로드 API 가용성에 의존한다.

## 완료 기준(DoD)
- [x] 최근 업로드 목록이 다시 보인다.
- [x] 최근 업로드 재분석이 동작한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
