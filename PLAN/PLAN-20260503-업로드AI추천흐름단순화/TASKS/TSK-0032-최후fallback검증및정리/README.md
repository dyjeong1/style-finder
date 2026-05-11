---
id: TSK-0032-최후fallback검증및정리
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-03
---

## 목적
규칙 분석기를 AI unavailable/error 시에만 쓰는 마지막 fallback 으로 제한하고, 실패 원인을 추적할 수 있게 검증/정리한다.

## 작업 내역
- [x] AI empty 와 AI unavailable/error 를 분리해 fallback 진입 조건을 명시
- [x] 응답 메타의 `analysis_source`, `query_source`, `fallback_reason` 으로 fallback 이유 추적 가능하게 정리
- [x] 회귀 테스트와 문서 정리

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/tests/test_api_e2e.py`
- `backend/tests/test_api_failures.py`
- `backend/tests/test_naver_shopping.py`
- `frontend/lib/api.ts`
- `frontend/app/(main)/recommendations/page.tsx`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_api_e2e.py tests/test_api_failures.py tests/test_naver_shopping.py -q` 통과
- `cd frontend && npm run build` 통과
- `cd frontend && npm run test:e2e -- --project=chromium --grep "업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"` 통과

## 의존성/리스크
- provider별 장애 케이스가 달라서 unavailable/error reason 값은 계속 확장될 수 있다.

## 완료 기준(DoD)
- [x] fallback 이 마지막 수단으로만 동작함
- [x] fallback 이유 추적 가능
- [x] 테스트/문서 갱신
