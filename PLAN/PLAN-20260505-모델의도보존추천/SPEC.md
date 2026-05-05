---
id: PLAN-20260505-모델의도보존추천-SPEC
plan_id: PLAN-20260505-모델의도보존추천
status: done
created_at: 2026-05-05
updated_at: 2026-05-05
---

## 제품 동작 기준
1. 모델 query/item_label에서 추출한 의도 keyword는 추천 후보 필터와 랭킹 보너스 양쪽에 동일하게 사용한다.
2. `롱슬리브`와 `긴팔`, `숏슬리브`와 `반팔`, `슬리브리스`와 `민소매`는 같은 의미로 본다.
3. 후보 필터는 semantic keyword가 있을 때 그 의도가 상품 제목/카테고리에도 반영된 경우만 통과시킨다.
4. 추천 응답 `matched_signals`에는 `target_intent_keywords`를 포함한다.

## 구현 대상
- `backend/src/services/recommendation_intent.py`
- `backend/src/services/naver_shopping.py`
- `backend/src/services/store.py`
- `backend/tests/test_naver_shopping.py`
- `backend/tests/test_store_color_matching.py`
- `backend/tests/test_api_e2e.py`

## 테스트 기준
- `남색 롱슬리브 티셔츠` query가 `네이비 긴팔 티셔츠`를 통과시킨다.
- 같은 query에서 `네이비 반팔 티셔츠`는 통과하지 않는다.
- 랭킹 보너스가 `긴팔` synonym 매칭에 반영된다.
