---
id: TSK-0017-가방하의일반품목정교화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.6d
updated_at: 2026-04-29
---

## 목적
가방과 하의에서 `가방`, `운동화`, `바지`, `팬츠`처럼 너무 일반적인 품목명이 남는 문제를 줄이고, fallback 또는 선택적 Gemini 보정으로 더 구체적인 서비스형 품목명으로 정리한다.

## 작업 내역
- [x] bag/bottom generic 품목 보정 규칙 추가
- [x] 선택적 Gemini 보정 대상 카테고리 조정
- [x] 테스트 보강
- [x] 실샘플 재검증
- [x] README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `README.md`
- `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_3.png --provider ollama --timeout-seconds 120`

## 의존성/리스크
- 가방/하의를 과하게 보정하면 실제 모델이 맞춘 세부명을 fallback이 덮어쓸 수 있다.
- Gemini 보정 대상을 넓히면 무료 티어 quota 사용량이 늘 수 있다.

## 결과 요약
- `운동화 -> 스니커즈` 정규화를 추가해 신발 generic label을 서비스형 품목명으로 통일했다.
- bag/bottom 계열은 같은 그룹 안에서 fallback이 더 구체적이면 `가방 -> 숄더백`, `바지/팬츠 -> 더 구체적인 팬츠 계열`로 보정하도록 했다.
- 선택적 Gemini 보정 대상에 `bag`을 추가해, generic bag label이 남아 있으면 Gemini 결과로 다시 교체할 수 있게 했다.
- `codytest_3` 실검증 결과:
  - `화이트 티셔츠 / 블루 가디건 / 브라운 팬츠 / 화이트 스니커즈 / 브라운 숄더백 / 팔찌 / 목걸이 / 반지 / 화이트 양말`
- 여전히 악세서리 색상과 세부명은 흔들릴 수 있어서, 다음 단계는 accessory 후처리 정교화가 우선이다.

## 완료 기준(DoD)
- [x] 가방/하의 generic 품목 보정이 코드에 추가된다.
- [x] 관련 테스트가 통과한다.
- [x] 실샘플에서 `가방`, `운동화`, `바지` 같은 표현이 일부 더 구체화된다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
