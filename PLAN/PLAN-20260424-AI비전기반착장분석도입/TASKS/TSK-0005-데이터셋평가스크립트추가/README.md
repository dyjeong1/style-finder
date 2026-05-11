---
id: TSK-0005-데이터셋평가스크립트추가
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
비전 데이터셋의 정답 라벨과 현재 착장 분석기 예측을 비교하는 평가 스크립트를 추가한다.

## 작업 내역
- [x] 데이터셋 평가 로직 구현
- [x] CLI 스크립트 추가
- [x] 테스트/문서 갱신
- [x] 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_dataset_evaluator.py`
- `backend/scripts/evaluate_vision_dataset.py`
- `backend/tests/test_vision_dataset_evaluator.py`

## 테스트/검증
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_vision_dataset_evaluator.py backend/tests/test_outfit_query_hints.py -q`
- `cd backend && PYTHONPATH=. python3 scripts/evaluate_vision_dataset.py`

## 완료 기준(DoD)
- [x] 데이터셋 평가 로직 추가
- [x] 평가 스크립트 추가
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신

## 완료 메모
- 현재 데이터셋 11샘플 기준으로 아이템 정밀도 0.2500, 재현율 0.2281, 샘플 완전일치율 0.0000을 확인했다.
- 복수 악세서리, 실사 전신샷, 레이어드 의상에서 오차가 커서 실제 AI 비전 provider 연결 우선순위가 높다는 근거를 확보했다.
