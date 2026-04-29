---
id: TSK-0024-비전우선분석전환
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-29
---

## 목적
업로드 착장 분석에서 규칙 기반 결과를 기본 뼈대로 섞지 않고, AI 비전 결과를 우선 사용하도록 전환한다. 규칙 분석기는 비전 provider가 비활성화되었거나 응답이 비어 있을 때만 최후 fallback으로 사용한다.

## 작업 내역
- [x] 업로드 분석 흐름을 AI 우선, 규칙 fallback-only 구조로 수정
- [x] 선택적 Gemini 보정이 AI 결과 기준으로 동작하도록 조정
- [x] 테스트와 문서를 새 정책 기준으로 갱신

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/README.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/PLAN.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/SPEC.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_api_e2e.py -q`

## 의존성/리스크
- Ollama 1차 결과가 일부 카테고리를 놓치는 경우, 규칙 결과 대신 선택적 Gemini 보정에 더 의존하게 된다.
- 규칙 기반 품목 보정 로직을 제거하지는 않으므로, 추후 미사용 유틸 정리가 필요할 수 있다.

## 완료 기준(DoD)
- [x] AI 결과가 존재할 때 규칙 기반 품목이 최종 detected_items에 자동 주입되지 않음
- [x] AI 결과가 비어 있을 때만 규칙 기반 fallback이 동작함
- [x] 관련 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
