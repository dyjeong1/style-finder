---
id: TSK-0009-규칙기반대제미나이비교리포트
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.4d
updated_at: 2026-04-27
---

## 목적
규칙 기반 분석기와 Gemini 비전 분석기를 같은 데이터셋에서 비교할 수 있는 스크립트를 만들고, 무료 티어 quota 제약을 고려한 캐시/재시도 구조를 추가한다.

## 작업 내역
- [x] 비교용 평가/포맷 함수 추가
- [x] `compare_vision_predictors.py` 스크립트 추가
- [x] Gemini 호출 캐시, 요청 간 대기, 재시도 로직 추가
- [x] 테스트 추가 및 백엔드 전체 테스트 통과
- [x] 문서/루트 README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_dataset_evaluator.py`
- `backend/scripts/compare_vision_predictors.py`
- `backend/tests/test_vision_dataset_evaluator.py`
- `backend/data/vision_dataset/cache/gemini.json`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_dataset_evaluator.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate gemini --format text`

## 의존성/리스크
- Gemini 무료 티어는 분당/일일 quota 제한이 있어 전체 데이터셋 비교가 하루에 한 번에 끝나지 않을 수 있다.
- 현재 스크립트는 캐시를 남기므로, quota가 리셋된 뒤 재실행하면 남은 샘플만 이어서 채운다.

## 완료 기준(DoD)
- [x] 규칙 기반 vs Gemini 비교 스크립트가 추가된다.
- [x] 무료 티어 제한을 고려한 캐시/재시도 구조가 추가된다.
- [x] 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서가 갱신된다.

## 완료 메모
- 2026-04-27 첫 실행에서 Gemini 무료 티어 일일 quota 한도로 전체 10장을 모두 채우지는 못했고, 3샘플 캐시까지 확보했다.
- 캐시 기준 부분 비교 결과는 개선 샘플 6개, 악화 샘플 5개로 집계되었다.
