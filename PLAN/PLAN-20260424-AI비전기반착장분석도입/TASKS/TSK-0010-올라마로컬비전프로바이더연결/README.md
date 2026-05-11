---
id: TSK-0010-올라마로컬비전프로바이더연결
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-27
---

## 목적
개인 비상업 프로젝트에서 클라우드 quota와 비용 제약 없이 이미지별 착장 분석을 반복 실험할 수 있도록 Ollama 기반 로컬 비전 provider를 연결한다.

## 작업 내역
- [x] `VisionOutfitAnalyzer`에 `ollama` provider 구현
- [x] `OLLAMA_VISION_*` 및 `OLLAMA_API_BASE_URL` 환경변수 호환 추가
- [x] 비교 스크립트에서 `ollama` 후보 지원 추가
- [x] 테스트/문서/루트 README/TODO/PLAN 갱신
- [x] 로컬 Ollama 설치 여부 확인 및 fallback 동작 검증
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/core/config.py`
- `backend/src/services/store.py`
- `backend/scripts/compare_vision_predictors.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --format text`

## 의존성/리스크
- 로컬 Ollama가 설치되지 않았거나 모델이 pull되지 않았다면 실호출 검증은 문서화까지만 가능하다.
- `qwen2.5vl:7b`는 로컬 메모리 자원을 사용하므로 사용자 장비 상태에 따라 응답 지연이 있을 수 있다.

## 완료 기준(DoD)
- [x] Ollama Vision provider 코드가 연결된다.
- [x] `OLLAMA_VISION_*` 이름이 설정에 반영된다.
- [x] 비교 스크립트에서 `ollama`를 baseline/candidate로 사용할 수 있다.
- [x] 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서가 갱신된다.

## 완료 메모
- 2026-04-27 기준 현재 작업 머신에는 Ollama가 설치되어 있지 않아 실모델 응답까지는 확인하지 못했다.
- 대신 `compare_vision_predictors.py --candidate ollama --max-retries 0` 실행 시 연결 거부를 짧게 보고하고 규칙 기반 fallback으로 종료되는 흐름을 검증했다.
- 기본 권장 모델은 `qwen2.5vl:7b`로 설정했다.
