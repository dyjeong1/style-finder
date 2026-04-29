---
id: TSK-0025-런타임평가정렬
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-29
---

## 목적
데이터셋 비교 스크립트가 실제 업로드 런타임과 같은 AI-first 분석 흐름을 직접 재현하도록 정렬한다. 이제 단일 provider 점수뿐 아니라 `ollama -> 선택적 gemini 보정 -> rule fallback` 경로를 같은 기준으로 측정할 수 있어야 한다.

## 작업 내역
- [x] 런타임 분석 helper를 재사용 가능한 형태로 추출
- [x] 비교 스크립트에 `runtime-<provider>` 형식 predictor 지원 추가
- [x] 테스트와 문서에 실제 런타임 평가 예시 반영

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/scripts/compare_vision_predictors.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/tests/test_vision_dataset_evaluator.py`
- `backend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_vision_dataset_evaluator.py -q`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --dataset-root data/vision_dataset --baseline rule --candidate runtime-ollama+gemini --format json`

## 의존성/리스크
- 캐시된 provider 결과를 사용하므로, fresh 측정값과는 차이가 있을 수 있다.
- 런타임 경로가 store helper를 재사용하게 되면서, 추후 helper 시그니처 변경 시 스크립트도 함께 관리해야 한다.

## 완료 기준(DoD)
- [x] 비교 스크립트가 런타임 AI-first 경로를 직접 평가할 수 있음
- [x] 테스트 통과
- [x] README/TODO/PLAN 문서 갱신
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
