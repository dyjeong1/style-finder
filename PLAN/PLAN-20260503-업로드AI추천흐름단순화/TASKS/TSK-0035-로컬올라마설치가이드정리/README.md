---
id: TSK-0035-로컬올라마설치가이드정리
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-03
---

## 목적
사용자가 로컬에서 Ollama를 설치하고 `gemma3:4b`를 pull한 뒤 이 저장소의 `ollama` provider를 바로 점검할 수 있도록 단일 가이드를 정리한다.

## 작업 내역
- [x] 기존 README와 backend README에 흩어진 Ollama 메모 수집
- [x] 설치, 모델 pull, 서버 실행, `.env` 설정, 점검 명령을 한 문서로 정리
- [x] 루트 README와 backend README에서 새 가이드로 진입할 수 있게 연결

## 산출물(Artifacts)
- `docs/ollama-local-setup.md`
- `README.md`
- `backend/README.md`
- `TODO.md`
- `PLAN/PLAN-20260503-업로드AI추천흐름단순화/PLAN.md`

## 테스트/검증
- 문서 교차 검토로 명령 순서와 경로가 현재 저장소 구조와 맞는지 확인

## 의존성/리스크
- 사용자의 macOS 환경, Homebrew 설치 여부, Ollama 데스크톱 앱 상태에 따라 실제 설치 단계는 조금 달라질 수 있다.
- 모델 다운로드 시간과 성능은 로컬 장비 상태에 따라 차이가 크다.

## 완료 기준(DoD)
- [x] 사용자가 설치부터 점검까지 한 문서에서 따라갈 수 있음
- [x] `gemma3:4b` pull과 `.env` 설정 예시가 포함됨
- [x] 루트 README와 backend README에서 새 가이드로 진입 가능
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서 갱신
