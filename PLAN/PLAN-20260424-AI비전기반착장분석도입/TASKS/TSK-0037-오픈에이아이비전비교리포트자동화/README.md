---
id: TSK-0037-오픈에이아이비전비교리포트자동화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-03
---

## 목적
OpenAI Vision 예측 결과와 정답 라벨 비교 리포트를 매번 수동 파일명으로 지정하지 않고 자동 경로로 생성할 수 있게 하며, 실제 런타임 비교에 쓰는 predictor 반환 버그도 함께 바로잡는다.

## 작업 내역
- [x] OpenAI 전용 비교 리포트 자동 생성 스크립트 추가
- [x] 리포트 파일명/저장 경로 규칙 추가
- [x] 데이터셋 유효성 검사 추가
- [x] runtime predictor 반환 버그 수정
- [x] 테스트 및 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/scripts/generate_openai_vision_report.py`
- `backend/scripts/compare_vision_predictors.py`
- `backend/tests/test_vision_dataset_evaluator.py`
- `README.md`
- `backend/README.md`
- `TODO.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/PLAN.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/SPEC.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_dataset_evaluator.py -q`
- 자동 생성 스크립트는 테스트 데이터셋 기준으로 JSON/TXT 리포트 경로를 생성하고, 빈 데이터셋에서는 `FileNotFoundError`로 즉시 실패하는지 확인

## 의존성/리스크
- 실제 OpenAI 응답 캐시가 없으면 `OPENAI_API_KEY`와 외부 호출 가능한 환경이 필요하다.
- 현재 세션에서는 실 OpenAI 호출까지 검증하지 않았으므로, 첫 실사용 시 timeout/요금/쿼터 상태는 별도 확인이 필요하다.

## 결과 요약
- `PYTHONPATH=. python3 scripts/generate_openai_vision_report.py` 한 번으로 `backend/data/vision_dataset/reports/openai/` 아래에 JSON/TXT 리포트를 함께 생성할 수 있게 했다.
- 리포트 파일명은 `openai-vs-rule-YYYYMMDD-HHMMSS[-scope].json|txt` 규칙을 따른다.
- `runtime-ollama+gemini` 같은 후보를 평가할 때 내부 predictor가 `(detected_items, source, reason)` 전체를 잘못 리스트화하던 버그를 수정해 실제 `DetectedOutfitItem[]`만 반환하도록 정리했다.

## 완료 기준(DoD)
- [x] OpenAI 비교 리포트 자동 생성 명령이 추가된다.
- [x] 리포트 경로와 파일명이 자동으로 정해진다.
- [x] 데이터셋 경로가 비어 있으면 조용히 빈 리포트를 만들지 않고 즉시 실패한다.
- [x] 관련 테스트가 통과한다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
