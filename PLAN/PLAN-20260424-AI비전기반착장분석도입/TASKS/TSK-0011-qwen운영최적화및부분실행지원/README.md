---
id: TSK-0011-qwen운영최적화및부분실행지원
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-28
---

## 목적
`qwen2.5vl:7b`를 메인 로컬 비전 모델로 유지하면서도 맥북 환경에서 과도한 타임아웃과 전체 배치 부담 없이 반복 실험할 수 있도록 timeout, 캐시, 부분 실행, 단일 업로드 검증 경로를 정리한다.

## 작업 내역
- [x] Ollama provider 기본 timeout/설정 해석을 무거운 모델 기준으로 보강
- [x] 데이터셋 비교 스크립트에 샘플 부분 실행 옵션 추가
- [x] 단일 이미지 업로드 분석 확인용 CLI 추가
- [x] qwen 단일 샘플 실응답 시도 및 로컬 지연 특성 확인
- [x] 테스트/문서/루트 README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/core/config.py`
- `backend/src/services/vision_dataset_evaluator.py`
- `backend/scripts/compare_vision_predictors.py`
- `backend/scripts/check_upload_analysis.py`
- `backend/tests/`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --sample-ids codytest_2 --format text`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg`

## 의존성/리스크
- 로컬 Ollama 모델 응답 속도는 장비 상태에 따라 달라질 수 있다.
- 전체 10장 비교는 여전히 시간이 오래 걸릴 수 있으므로 부분 실행과 캐시를 적극 활용한다.

## 완료 기준(DoD)
- [x] qwen 기준 기본 timeout이 개선된다.
- [x] 샘플 단위 부분 실행이 가능해진다.
- [x] 단일 업로드 분석 결과를 CLI로 확인할 수 있다.
- [x] 실제 qwen 단일 샘플 호출을 시도하고 로컬 지연 특성을 확인한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서가 갱신된다.

## 완료 메모
- `resolve_vision_outfit_analyzer_runtime_config()`가 provider별 timeout/max-image 기본값을 분리해 해석하도록 보강했다.
- `compare_vision_predictors.py`에 `--sample-ids`, `--offset`, `--limit`, `--timeout-seconds` 옵션을 추가해 전체 10장을 한 번에 돌리지 않아도 되게 했다.
- `check_upload_analysis.py`로 단일 이미지 업로드 분석 결과를 직접 확인할 수 있게 했다.
- `codytest_2` 기준 `qwen2.5vl:7b` 단일 호출은 180초에서도 결과가 매우 늦어, 현재 맥북 환경에서는 더 가벼운 모델 전환이 합리적이라는 결론을 확인했다.
