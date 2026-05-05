---
id: PLAN-20260505-네이버호출정확도튜닝-SPEC
plan_id: PLAN-20260505-네이버호출정확도튜닝
status: done
created_at: 2026-05-05
updated_at: 2026-05-05
---

## 제품 동작 기준
1. 네이버 쇼핑 API 호출은 기본적으로 `sort=sim`을 사용한다.
2. 기본 `exclude`는 `used:rental:cbshop`로 적용해 중고/렌탈/해외직구 후보를 줄인다.
3. `filter=naverpay`는 필요 시 설정값으로만 활성화한다.
4. 관련 설정값은 환경변수로 조정할 수 있다.

## 구현 대상
- `backend/src/core/config.py`
- `backend/src/api/routes/recommendation.py`
- `backend/src/services/naver_shopping.py`
- `backend/tests/test_naver_shopping.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트 기준
- 네이버 요청 URL에 `sort`, `filter`, `exclude`가 반영된다.
- 잘못된 sort 값은 `sim`으로 fallback 된다.
- 설정값 환경변수가 정상 파싱된다.
