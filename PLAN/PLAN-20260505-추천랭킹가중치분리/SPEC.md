---
id: PLAN-20260505-추천랭킹가중치분리-SPEC
plan_id: PLAN-20260505-추천랭킹가중치분리
status: done
created_at: 2026-05-05
updated_at: 2026-05-05
---

## 제품 동작 기준
1. 추천 점수는 설정 객체를 통해 `base`, `vector_similarity`, `tone`, `mood`, `silhouette`, `category`, `color`, `product_image_color`, `item_label`, `vision_similarity` 가중치를 관리한다.
2. 업로드 분석에 특정 카테고리의 `item_label`이 있으면 같은 품목명을 포함한 상품명에 추가 보너스를 준다.
3. `가방`, `팬츠`처럼 너무 일반적인 품목명은 품목명 보너스 대상에서 제외한다.
4. `vision_similarity`는 설정값으로 곱해져 추천 점수에 반영된다.

## 구현 대상
- `backend/src/core/config.py`
- `backend/src/services/store.py`
- `backend/tests/test_store_color_matching.py`
- `backend/tests/test_api_e2e.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트 기준
- 품목명 일치 보너스가 특정 품목명을 가진 상품을 더 위로 올린다.
- `vision_similarity_weight=0`일 때 비전 유사도 차이가 점수에 반영되지 않는다.
- score breakdown과 matched signals에 새 디버그 필드가 포함된다.
