---
id: PLAN-20260505-AI검색어고도화-SPEC
plan_id: PLAN-20260505-AI검색어고도화
status: done
created_at: 2026-05-05
updated_at: 2026-05-05
---

## 제품 동작 기준
1. AI가 반환한 품목 query 또는 item_label 안에 패턴/소재 힌트가 있으면 검색어에 보존한다.
2. 검색어는 가능하면 `색상 + 패턴 + 소재 + 품목` 순서를 사용하고, 없는 정보만 생략한다.
3. `무지` 같은 표현은 사용자 노출용 query에서 `민무늬`로 정규화한다.
4. 기존 액세서리 전용 descriptor 규칙과 품목 정규화는 유지한다.

## 구현 대상
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트 기준
- `브라운 스트라이프 실크 셔츠`, `브라운 체크 가죽 가방`, `화이트 민무늬 실크 블라우스` 같은 query가 안정적으로 생성된다.
- 기존 `가죽`, `스웨이드`, `도트`, 액세서리 descriptor 회귀가 유지된다.
