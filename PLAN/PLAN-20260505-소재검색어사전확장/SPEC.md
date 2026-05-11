---
id: PLAN-20260505-소재검색어사전확장-SPEC
plan_id: PLAN-20260505-소재검색어사전확장
status: done
created_at: 2026-05-05
updated_at: 2026-05-05
---

## 제품 동작 기준
1. AI가 반환한 query 또는 item_label 안에 `쉬폰`, `레이스`, `트위드` 같은 소재 힌트가 있으면 검색어에 보존한다.
2. 검색어는 기존 원칙대로 가능하면 `색상 + 패턴 + 소재 + 품목` 순서를 유지한다.
3. `레이스`처럼 패턴/소재 경계가 있는 표현도 사용자 검색어에서 자연스럽게 남아야 한다.
4. 기존 `가죽`, `실크`, `스웨이드` 등 descriptor 회귀는 유지한다.

## 구현 대상
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트 기준
- `화이트 레이스 쉬폰 블라우스`, `브라운 트위드 자켓` 같은 query가 안정적으로 생성된다.
- 기존 `브라운 체크 가죽 가방`, `화이트 민무늬 실크 블라우스` 회귀가 유지된다.
