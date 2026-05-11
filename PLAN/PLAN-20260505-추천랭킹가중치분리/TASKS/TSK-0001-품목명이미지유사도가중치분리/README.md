---
id: TSK-0001-품목명이미지유사도가중치분리
plan_id: PLAN-20260505-추천랭킹가중치분리
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-05
---

## 목적
추천 점수식에서 품목명 일치와 비전 이미지 유사도의 영향도를 분리해 이후 튜닝 작업을 빠르게 만들고, 랭킹 판단 근거를 더 명확히 노출합니다.

## 작업 내역
- [x] 추천 점수 설정 객체 도입
- [x] 품목명 일치 보너스 추가
- [x] 비전 이미지 유사도 가중치 설정 분리
- [x] 회귀 테스트 및 API 디버그 필드 갱신
- [x] 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/core/config.py`
- `backend/src/services/store.py`
- `backend/tests/test_store_color_matching.py`
- `backend/tests/test_api_e2e.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_store_color_matching.py tests/test_api_e2e.py tests/test_vision_outfit_analyzer.py -q`

## 의존성/리스크
- 품목명 보너스는 업로드 분석의 `item_label` 품질에 의존하므로, generic 품목명 보너스는 제한해야 합니다.

## 완료 기준(DoD)
- [x] 품목명 일치 보너스가 동작한다.
- [x] 비전 유사도 가중치가 설정값으로 분리된다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
