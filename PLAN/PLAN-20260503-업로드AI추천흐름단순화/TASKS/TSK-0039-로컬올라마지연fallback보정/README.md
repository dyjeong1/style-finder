---
id: TSK-0039-로컬올라마지연fallback보정
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-03
---

## 목적
로컬 `Ollama` 서버가 꺼져 있거나 연결되지 않을 때 업로드 분석이 긴 timeout 동안 붙잡혀 `이미지 분석 중...` 상태로 멈춰 보이는 문제를 줄이고, 즉시 규칙 기반 fallback 으로 넘어가게 한다.

## 작업 내역
- [x] `Ollama` loopback 주소에 대한 빠른 reachability probe 추가
- [x] provider 연결 실패/timeout 시 fallback_reason을 더 구체적으로 정리
- [x] 로컬 `Ollama` 미실행 상황 회귀 테스트 추가
- [x] README/TODO/PLAN/TASK 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/README.md`
- `README.md`
- `TODO.md`
- `PLAN/PLAN-20260503-업로드AI추천흐름단순화/PLAN.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- 로컬 `Ollama` 미실행 가정에서 `provider_unreachable` fallback_reason으로 규칙 분석이 바로 사용되는지 단위 테스트로 검증

## 의존성/리스크
- 이번 보정은 loopback(`127.0.0.1`, `localhost`, `::1`) 기반 로컬 provider에만 빠른 연결 확인을 적용한다.
- 실제 `Ollama` 서버가 떠 있어도 모델 응답 자체가 오래 걸리면 provider timeout 기준 fallback 이 동작할 수 있다.

## 결과 요약
- 이제 로컬 `Ollama` 주소가 아예 닫혀 있으면 업로드 분석이 긴 `OLLAMA_VISION_TIMEOUT_SECONDS`를 다 기다리지 않고 즉시 규칙 fallback 으로 전환된다.
- `provider_unreachable`, `provider_timeout`, `provider_http_error`처럼 provider 실패 사유가 더 구체적으로 남아 런타임 원인 파악이 쉬워졌다.
- 사용자 체감상 업로드 버튼이 오래 `이미지 분석 중...` 상태에 묶이는 증상을 크게 줄이는 방향으로 정리됐다.

## 완료 기준(DoD)
- [x] 로컬 `Ollama` 미실행 시 업로드 분석이 빠르게 fallback 된다.
- [x] provider 실패 사유가 더 구체적으로 기록된다.
- [x] 회귀 테스트가 추가된다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
