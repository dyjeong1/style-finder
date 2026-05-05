---
id: PLAN-20260505-브랜드로고검색어반영-SPEC
plan_id: PLAN-20260505-브랜드로고검색어반영
status: done
created_at: 2026-05-05
updated_at: 2026-05-05
---

## 제품 동작 기준
1. AI가 로고나 브랜드 텍스트를 명확히 읽을 수 있을 때만 `brand`를 반환하고 query에 반영한다.
2. 검색어는 가능하면 `브랜드 + 색상 + 패턴 + 소재 + 품목` 순서를 사용한다.
3. 브랜드가 보이지 않거나 불명확하면 기존처럼 브랜드 없이 query를 만든다.
4. 기존 소재/패턴 descriptor 회귀는 유지한다.

## 구현 대상
- `backend/src/services/image_analysis.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/tests/test_api_e2e.py`

## 테스트 기준
- `뉴발란스 그레이 스니커즈`, `아디다스 블랙 트랙 자켓` 같은 query가 안정적으로 생성된다.
- 기존 `브라운 체크 가죽 가방`, `화이트 레이스 쉬폰 블라우스` 회귀가 유지된다.
