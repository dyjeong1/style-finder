---
id: TSK-0002-최근업로드재사용UI복원
plan_id: PLAN-20260504-최근업로드이미지재사용복원
owner: codex
status: ready
estimate: 0.5d
updated_at: 2026-05-04
---

## 목적
저장된 업로드 이미지를 `/upload` 화면에서 다시 선택 없이 재사용할 수 있도록 최근 업로드 목록 UI와 재분석 흐름을 복원한다.

## 작업 내역
- [ ] 최근 업로드 목록 렌더링 추가
- [ ] 카드 클릭 시 저장된 이미지 재업로드 연결
- [ ] 카드 삭제/빈 상태/에러 처리 추가
- [ ] E2E 검증 및 문서 반영

## 산출물(Artifacts)
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/globals.css`
- `frontend/e2e/core-flow.spec.ts`

## 테스트/검증
- `/upload`에서 최근 업로드 카드가 렌더링되는지 확인
- 카드 클릭 시 추천 페이지로 이동하는지 Playwright로 검증

## 의존성/리스크
- 카드 클릭 시 새 분석을 다시 수행하므로 업로드 API 가용성에 의존한다.

## 완료 기준(DoD)
- [ ] 최근 업로드 목록이 다시 보인다.
- [ ] 최근 업로드 재분석이 동작한다.
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
