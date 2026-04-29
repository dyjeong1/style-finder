---
id: TSK-0006-오픈에이아이비전프로바이더연결
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-27
---

## 목적
사용자가 `.env`에 입력한 `OPENAI_API_KEY`를 이용해 실제 OpenAI Vision provider를 업로드 분석 흐름에 연결하고, 기존 규칙 기반 분석이 안전한 fallback으로 계속 동작하도록 정리한다.

## 작업 내역
- [x] `VisionOutfitAnalyzer`에 `openai` provider 구현
- [x] `OPENAI_API_KEY`, `OPENAI_VISION_*` 환경변수 별칭 지원 추가
- [x] 다중 악세서리 결과를 `detected_items`에 유지하도록 병합 로직 보강
- [x] 테스트/README/TODO/PLAN 문서 갱신
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
- `cd backend && python3 scripts/evaluate_vision_dataset.py --format text`

## 의존성/리스크
- 실제 OpenAI 호출은 API 키와 Billing 상태에 영향을 받는다.
- OpenAI 응답 실패 시에도 서비스가 멈추지 않도록 규칙 기반 fallback을 유지한다.

## 완료 기준(DoD)
- [x] OpenAI Vision provider 코드가 연결된다.
- [x] 사용자가 이미 입력한 `OPENAI_VISION_*` 이름이 그대로 동작한다.
- [x] 기존 테스트와 신규 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서가 갱신된다.

## 완료 메모
- OpenAI `Responses API` 기반 이미지 입력과 `json_schema` 응답 파싱을 추가했다.
- OpenAI 결과는 `detected_items`에 여러 품목을 유지하고, 카테고리 검색 힌트는 첫 번째 품목 기준으로 사용한다.
- OpenAI 호출 실패 시에는 업로드 분석이 자동으로 규칙 기반으로 fallback 된다.
