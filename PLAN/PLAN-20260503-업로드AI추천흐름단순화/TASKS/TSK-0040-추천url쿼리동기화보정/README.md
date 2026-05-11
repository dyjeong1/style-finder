---
id: TSK-0040-추천url쿼리동기화보정
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
추천 페이지가 production build 환경에서 `uploaded_image_id` query를 놓쳐 `업로드된 이미지가 없습니다` 상태로 잘못 빠지는 문제를 보정한다.

## 작업 내역
- [x] 추천 페이지의 URL query 읽기 경로 점검
- [x] `useSearchParams()` 결과가 늦거나 비어 있어도 `window.location.search`로 보완하도록 수정
- [x] 프론트 재빌드 후 추천 URL 직접 접근 검증
- [x] README/TODO/PLAN/TASK 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/README.md`
- `README.md`
- `TODO.md`
- `PLAN/PLAN-20260503-업로드AI추천흐름단순화/PLAN.md`

## 테스트/검증
- `cd frontend && npm run local`
- 브라우저에서 `http://127.0.0.1:3000/recommendations?uploaded_image_id=<id>` 직접 진입
- 수정 전: `업로드된 이미지가 없습니다. /upload에서 이미지를 먼저 올려주세요.`
- 수정 후: 같은 URL에서 검색어/업로드 분석/추천 상품 목록이 정상 렌더됨

## 의존성/리스크
- 이번 보정은 query 동기화 안정화에 집중한 대응이며, 업로드 단계 자체의 네트워크 실패와는 별도다.
- 이후 브라우저별 query hydration 차이가 다시 보이면 server component prop 전달 방식으로 한 번 더 단순화할 수 있다.

## 결과 요약
- 추천 페이지는 이제 `useSearchParams()` 값이 늦게 들어오거나 비어 있는 경우에도 현재 브라우저 URL에서 `uploaded_image_id`를 다시 읽어 현재 업로드 기준 상태를 복구한다.
- production build에서 직접 추천 URL을 열었을 때도 더 이상 초기 null 상태에 고정되지 않고, 실제 추천 로딩과 결과 렌더로 이어진다.

## 완료 기준(DoD)
- [x] 추천 페이지가 `uploaded_image_id`를 더 안정적으로 읽는다.
- [x] production build에서 직접 추천 URL 진입 시 결과가 렌더된다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
