---
id: TSK-0012-올라마경량기본모델전환
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.4d
updated_at: 2026-04-29
---

## 목적
로컬 개발 기본 경로를 `qwen2.5vl:7b`에서 더 가벼운 `gemma3:4b`로 전환해, 맥북 환경에서도 실제 업로드 분석과 반복 테스트를 현실적으로 수행할 수 있게 한다.

## 작업 내역
- [x] Ollama 기본 권장 모델을 `gemma3:4b`로 변경
- [x] 로컬 `.env`를 가벼운 모델 기준으로 정리
- [x] 모델 pull 및 단일 이미지 실응답 검증
- [x] 문서/루트 README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/.env.example`
- `backend/.env`
- `backend/src/core/config.py`
- `backend/README.md`
- `README.md`
- `TODO.md`

## 테스트/검증
- `ollama pull gemma3:4b`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --sample-ids codytest_2 --format text --timeout-seconds 120 --max-retries 0`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 결과 요약
- `gemma3:4b`를 로컬 기본 권장 모델로 전환했다.
- `codytest_2.jpg` 실응답에서 `화이트 셔츠`, `회색 가디건`, `청바지 팬츠`, `검정 선글라스`를 추출하는 것을 확인했다.
- 비교 스크립트 단일 샘플 실행도 timeout 없이 완료됐다.
- 다만 `codytest_2` 기준 품목명 정확도는 아직 규칙 기반보다 낮아, 이후 후처리/정규화 튜닝이 필요하다.

## 의존성/리스크
- `gemma3:4b`는 속도와 안정성은 좋아졌지만 품목 세분화 정확도는 `qwen2.5vl:7b`보다 낮을 수 있다.
- 비교 스크립트 전체 데이터셋 평가는 샘플 수가 늘수록 시간이 길어질 수 있어 캐시 활용이 중요하다.

## 완료 기준(DoD)
- [x] Ollama 기본 권장 모델이 `gemma3:4b`로 바뀐다.
- [x] 로컬 `.env`가 Ollama 경량 모델 기준으로 정리된다.
- [x] 최소 1개 샘플에서 실제 응답을 확인한다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
