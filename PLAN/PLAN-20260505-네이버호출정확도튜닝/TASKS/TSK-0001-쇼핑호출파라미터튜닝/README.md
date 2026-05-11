---
id: TSK-0001-쇼핑호출파라미터튜닝
plan_id: PLAN-20260505-네이버호출정확도튜닝
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-05
---

## 목적
네이버 쇼핑 API 공식 파라미터를 이용해 추천 엔진 이전 단계의 후보 정확도를 높입니다.

## 작업 내역
- [x] 네이버 쇼핑 호출 파라미터 설정 확장
- [x] 기본 `exclude=used:rental:cbshop` 반영
- [x] `sort/filter` 설정값 반영
- [x] 테스트 및 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/core/config.py`
- `backend/src/api/routes/recommendation.py`
- `backend/src/services/naver_shopping.py`
- `backend/tests/test_naver_shopping.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_naver_shopping.py tests/test_vision_outfit_analyzer.py -q`

## 의존성/리스크
- `filter=naverpay`는 사용성보다 결제 편의 우선 옵션이므로 기본 활성화하지 않는다.

## 완료 기준(DoD)
- [x] 네이버 API 호출 파라미터가 튜닝 가능해진다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
