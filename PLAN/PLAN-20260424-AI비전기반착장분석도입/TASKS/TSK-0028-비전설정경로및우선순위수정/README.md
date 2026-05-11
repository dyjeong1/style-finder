---
id: TSK-0028-비전설정경로및우선순위수정
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-29
---

## 목적
백엔드를 어느 디렉터리에서 실행하느냐에 따라 `.env`를 놓치거나, `ollama` provider인데 stale 공통 모델명이 우선 적용되어 AI 대신 fallback 이 자주 실행되는 문제를 줄인다.

## 작업 내역
- [x] `backend/.env`를 절대경로로 읽도록 설정 경로 보강
- [x] 런타임 비전 설정에서 provider별 `*_VISION_*` 값을 공통 `VISION_*`보다 우선 적용
- [x] 관련 테스트와 문서 갱신

## 산출물(Artifacts)
- `backend/src/core/config.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_api_e2e.py tests/test_api_failures.py -q`
- `PYTHONPATH=backend python3 -c "from src.core.config import get_settings, resolve_vision_outfit_analyzer_runtime_config; print(resolve_vision_outfit_analyzer_runtime_config(get_settings()))"`

## 의존성/리스크
- Ollama 서버가 실제로 꺼져 있으면 설정이 맞아도 fallback 은 계속 발생한다.
- Gemini 보정은 quota/503 상태에 따라 일시적으로 동작하지 않을 수 있다.

## 완료 기준(DoD)
- [x] 실행 디렉터리와 무관하게 `backend/.env` 기준 설정을 읽음
- [x] `ollama` 사용 시 `OLLAMA_VISION_MODEL` 같은 provider별 설정이 런타임에서 우선됨
- [x] 관련 테스트 통과
- [x] README/TODO/PLAN 문서 갱신
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
