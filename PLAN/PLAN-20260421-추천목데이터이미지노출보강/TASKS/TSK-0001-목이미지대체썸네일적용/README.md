---
id: TSK-0001-목이미지대체썸네일적용
plan_id: PLAN-20260421-추천목데이터이미지노출보강
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-21
---

## 목적
실 API가 연결되지 않은 목데이터 환경에서도 추천/위시리스트 카드의 상품 이미지가 항상 보이도록 만든다.

## 작업 내역
- [x] 목 이미지 URL 판별 함수 추가
- [x] 추천 카드 fallback 즉시 적용
- [x] 위시리스트 카드 fallback 즉시 적용
- [x] 문서/README/TODO 반영

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/recommendations/page.tsx`, `frontend/app/(main)/wishlist/page.tsx`
- 문서/노트북: `PLAN/PLAN-20260421-추천목데이터이미지노출보강/*`

## 테스트/검증
- `cd frontend && npm run build`
- 추천/위시리스트 카드에서 썸네일 확인

## 의존성/리스크
- 선행 TASK/시스템/권한: 없음

## 완료 기준(DoD)
- [ ] 추천/위시리스트 카드에서 썸네일이 항상 보인다.
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [ ] README/TODO 갱신
