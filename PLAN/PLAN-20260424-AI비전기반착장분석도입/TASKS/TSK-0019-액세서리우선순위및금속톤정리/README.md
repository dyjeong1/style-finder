---
id: TSK-0019-액세서리우선순위및금속톤정리
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-29
---

## 목적
액세서리 결과에서 양말/반지 같은 보조 품목이 너무 앞에 노출되지 않게 우선순위를 정리하고, 주얼리 계열은 `그레이/옐로우` 대신 `실버/골드` 검색어를 사용해 더 자연스럽게 만든다.

## 작업 내역
- [x] 액세서리 우선순위 정렬 규칙 추가
- [x] 주얼리 실버/골드 검색어 보정
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
- `cd backend && PYTHONPATH=. python3 - <<'PY' ... codytest_3 ... PY`

## 의존성/리스크
- 주얼리 검색어를 `실버/골드`로 바꾸면 기존 색상 enum(`gray/yellow`)과 표현 차이가 생기므로, 내부 저장값과 노출값을 명확히 구분해야 한다.

## 결과 요약
- 액세서리 쿼리에서 `목걸이`, `귀걸이`, `팔찌`, `반지`는 `gray -> 실버`, `yellow -> 골드` 표현으로 바꿨다.
- 액세서리 표시 순서는 `안경 -> 목걸이 -> 귀걸이 -> 팔찌 -> ... -> 반지 -> 양말`로 정리해 양말/반지가 보조 품목처럼 뒤로 가도록 조정했다.
- `codytest_3` 실검증 결과:
  - `화이트 프릴 민소매 / 블루 털 카디건 / 브라운 와이드 팬츠 / 화이트 스니커즈 / 브라운 숄더백 / 실버 목걸이 / 실버 팔찌 / 실버 반지 / 화이트 양말`
- 실샘플에서 Gemini가 잠시 `503 high demand`를 반환한 경우도 있었지만, 재시도 후 정상 결과를 확인했다.

## 완료 기준(DoD)
- [x] 액세서리 우선순위 정렬이 코드에 추가된다.
- [x] 주얼리 검색어가 `실버/골드` 표현으로 정리된다.
- [x] 관련 테스트가 통과한다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
