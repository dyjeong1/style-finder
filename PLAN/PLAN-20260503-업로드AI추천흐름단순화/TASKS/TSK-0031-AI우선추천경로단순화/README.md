---
id: TSK-0031-AI우선추천경로단순화
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-03
---

## 목적
추천 생성 경로를 "AI 분석 성공 -> 추천" 중심으로 단순화하고, 불필요한 중간 보정/상태 동기화 잔재를 줄인다.

## 작업 내역
- [x] 추천 API와 프론트가 현재 업로드의 AI 분석만 기준으로 동작하는지 재정리
- [x] 필요 없는 임의 카테고리 fallback 과 업로드 분석 보조 설명 로직을 정리
- [x] 직접 검색어는 유지하되, 추천 기준 표시는 AI 분석/규칙 fallback 기준으로 명시

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/lib/api.ts`
- `backend/tests/test_api_e2e.py`
- `frontend/e2e/core-flow.spec.ts`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_api_e2e.py tests/test_api_failures.py tests/test_naver_shopping.py -q` 통과
- `cd frontend && npm run build` 통과
- `cd frontend && npm run test:e2e -- --project=chromium --grep "업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"` 통과

## 의존성/리스크
- 직접 검색어 기능은 유지하지만, 최종 추천 기준은 항상 현재 업로드 분석 메타와 함께 보여주도록 유지해야 한다.

## 완료 기준(DoD)
- [x] AI 성공 경로가 최종 추천 기준으로 명확히 유지됨
- [x] 불필요한 보조 상태/설명 로직 정리
- [x] 테스트/문서 갱신
