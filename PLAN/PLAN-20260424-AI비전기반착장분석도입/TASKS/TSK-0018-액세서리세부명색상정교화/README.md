---
id: TSK-0018-액세서리세부명색상정교화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-29
---

## 목적
액세서리에서 `팔찌`, `목걸이`, `반지` 같은 주얼리 품목은 유지하되, 색상이 비어 있거나 generic하게 남는 문제를 줄여 더 자연스러운 서비스형 검색어로 정리한다.

## 작업 내역
- [x] 액세서리 세부명 정규화 규칙 추가
- [x] 주얼리 accessory 색상 기본값 보정
- [x] 테스트 보강
- [x] 실샘플 재검증
- [x] README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `README.md`
- `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd backend && PYTHONPATH=. python3 - <<'PY' ... codytest_3 ... PY`

## 의존성/리스크
- 작은 액세서리는 실제 색상이 잘 안 보일 수 있어, 과도한 색상 보정은 오탐으로 이어질 수 있다.
- `그레이`를 실버 대용으로 쓰는 현재 색상 체계 한계를 문서에 남겨야 한다.

## 결과 요약
- 액세서리 정규화 규칙에 `팔찌`, `반지`, `체인 팔찌`를 추가했다.
- 주얼리 accessory(`목걸이`, `귀걸이`, `팔찌`, `반지`)가 `unknown` 또는 `neutral` 색상으로 들어오면 기본적으로 `gray`로 보정하도록 했다.
- `실버`, `골드`, `메탈` 같은 텍스트가 있으면 각각 `gray`, `yellow`로 우선 추론하도록 보강했다.
- `codytest_3` 실검증 결과:
  - `화이트 셔츠 / 블루 가디건 / 브라운 와이드 팬츠 / 화이트 스니커즈 / 브라운 숄더백 / 그레이 팔찌 / 그레이 목걸이 / 화이트 양말`
- 아직 `반지`의 유지 여부나 `양말` 노출 우선순위는 추가 조정 여지가 있어, 다음 단계에서 accessory 우선순위를 더 정리하는 편이 좋다.

## 완료 기준(DoD)
- [x] 액세서리 세부명/색상 정규화가 코드에 추가된다.
- [x] 관련 테스트가 통과한다.
- [x] 실샘플에서 `팔찌`, `목걸이`, `반지` 표현이 더 자연스럽게 정리된다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
