---
id: TSK-0001-추천프리뷰조건부노출
plan_id: PLAN-20260506-추천빈업로드프리뷰숨김
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-06
---

## 목적
추천 페이지에서 업로드가 없는 빈 상태와 업로드 분석 완료 상태를 더 명확히 구분하기 위해, 상단 업로드 프리뷰와 확대 모달을 조건부로 노출한다.

## 작업 내역
- [x] 추천 상단 프리뷰 버튼 조건부 렌더링 추가
- [x] 확대 모달 조건부 렌더링 정렬
- [x] 업로드 전/후 프리뷰 노출 회귀 테스트 보강
- [x] 문서/README/TODO 반영

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/e2e/core-flow.spec.ts`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd frontend && npm run build`
- `cd frontend && npm run test:e2e:local:smoke -- --grep "@smoke 업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"`
- 인앱 브라우저 `http://127.0.0.1:3000/recommendations`에서 업로드 전 프리뷰 카드 미노출 확인

## 의존성/리스크
- 추천 프리뷰 복원 로직과 충돌 없이 렌더링 조건만 조정해야 한다.
- 분석 응답 로딩 중 프리뷰가 숨겨지는 동작은 의도된 UX로 유지한다.

## 완료 기준(DoD)
- [x] 업로드 이미지가 없을 때 프리뷰 버튼이 보이지 않는다.
- [x] 업로드 분석 완료 후 프리뷰 버튼이 다시 보인다.
- [x] 확대 모달이 기존 동작을 유지한다.
- [x] 유닛/통합 또는 E2E 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
