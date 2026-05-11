---
id: TSK-0001-악세사리카테고리노출보강
plan_id: PLAN-20260507-악세사리추천노출보강
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-07
---

## 목적
감지된 악세사리 추천 후보가 전체 추천 상한에 밀려 섹션 자체가 사라지는 문제를 막는다.

## 작업 내역
- [x] 전체 추천 결과 제한 시 감지 카테고리 최소 노출 보장 로직 추가
- [x] 악세사리 회귀 테스트 추가
- [x] 관련 문서와 루트 README/TODO 갱신

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/tests/test_store_color_matching.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_store_color_matching.py -q`
- 현재 추천 API 응답 확인으로 악세사리 전용 결과와 전체 결과 구조 비교

## 의존성/리스크
- 현재 업로드 분석에 `accessory` 카테고리 자체가 없으면 이 보강만으로는 악세사리 섹션이 생기지 않는다.
- 전체 추천 다양성을 위해 하위 rank 상품이 상위 limit에 포함될 수 있다.

## 완료 기준(DoD)
- [x] 감지된 악세사리 카테고리가 전체 추천 limit 때문에 완전히 사라지지 않는다.
- [x] 유닛 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
