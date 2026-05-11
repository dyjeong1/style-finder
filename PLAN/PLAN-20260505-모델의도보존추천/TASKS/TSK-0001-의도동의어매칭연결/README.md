---
id: TSK-0001-의도동의어매칭연결
plan_id: PLAN-20260505-모델의도보존추천
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-05
---

## 목적
모델이 반환한 query/item_label의 의도를 후보 필터와 랭킹 점수 계산에서 같은 의미로 읽어 추천 결과까지 보존합니다.

## 작업 내역
- [x] 공통 intent keyword 동의어 레이어 추가
- [x] 네이버 후보 필터에 semantic keyword 적용
- [x] 추천 랭킹 보너스를 intent keyword 기반으로 확장
- [x] 테스트 및 디버그 필드 갱신
- [x] 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/recommendation_intent.py`
- `backend/src/services/naver_shopping.py`
- `backend/src/services/store.py`
- `backend/tests/test_naver_shopping.py`
- `backend/tests/test_store_color_matching.py`
- `backend/tests/test_api_e2e.py`

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_naver_shopping.py tests/test_store_color_matching.py tests/test_api_e2e.py -q`

## 의존성/리스크
- intent 동의어 사전은 좁고 보수적으로 유지해야 잘못된 후보 확대를 막을 수 있습니다.

## 완료 기준(DoD)
- [x] 모델 의도 동의어가 후보 필터와 랭킹에 반영된다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
