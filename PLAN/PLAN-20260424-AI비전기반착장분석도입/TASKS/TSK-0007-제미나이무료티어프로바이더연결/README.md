---
id: TSK-0007-제미나이무료티어프로바이더연결
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-27
---

## 목적
개인 비상업 프로젝트에서도 비용 부담 없이 이미지별 착장 분석 실험을 이어갈 수 있도록 Gemini 무료 티어 provider를 비전 분석 흐름에 연결한다.

## 작업 내역
- [x] `VisionOutfitAnalyzer`에 `gemini` provider 구현
- [x] `GEMINI_API_KEY`, `GEMINI_VISION_*` 환경변수 별칭 지원 추가
- [x] Gemini 요청/응답 파싱 테스트 추가
- [x] README/TODO/PLAN 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/core/config.py`
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/.env.example`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 의존성/리스크
- 실제 Gemini 호출은 `GEMINI_API_KEY`가 필요하다.
- 무료 티어는 quota 제한이 있으므로 대량 평가 전에 호출량 제어가 필요하다.
- Gemini 호출 실패 시에도 규칙 기반 fallback을 유지한다.

## 완료 기준(DoD)
- [x] Gemini Vision provider 코드가 연결된다.
- [x] `GEMINI_*` 환경변수가 정상 인식된다.
- [x] 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서가 갱신된다.

## 완료 메모
- Gemini `generateContent` 기반 이미지 입력과 JSON 응답 파싱을 추가했다.
- OpenAI provider는 유지하되, 개인 비상업 프로젝트의 기본 권장 경로를 Gemini 무료 티어로 문서화했다.
