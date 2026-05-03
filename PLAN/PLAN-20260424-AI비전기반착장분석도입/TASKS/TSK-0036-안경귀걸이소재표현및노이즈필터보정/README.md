---
id: TSK-0036-안경귀걸이소재표현및노이즈필터보정
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-03
---

## 목적
안경/귀걸이 accessory query에서 소재·형태 descriptor를 더 자연스럽게 남기고, AI 보정 단계에서 `칼라` 같은 unsupported accessory 라벨이나 단일 추가 jewelry 오탐이 결과를 어지럽히는 문제를 줄인다.

## 작업 내역
- [x] 안경/귀걸이 descriptor 보존 규칙 추가
- [x] accessory 색상 보정 조건 정밀화
- [x] unsupported accessory 라벨 필터 추가
- [x] Gemini 보정의 단일 추가 jewelry 오탐 억제
- [x] 테스트/문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `README.md`
- `backend/README.md`
- `TODO.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/PLAN.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/SPEC.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_outfit_query_hints.py -q`
- 캐시 기반 런타임 확인:
  - `codytest_2`: `블루 가디건 / 네이비 와이드 데님 팬츠 / 블랙 안경`
  - `codytest_3`: `실버 목걸이 / 실버 팔찌 / 실버 반지` 유지
  - `codytest_6`: `화이트 양말`만 유지되고 unsupported/단일 jewelry 오탐 제거

## 의존성/리스크
- 단일 추가 jewelry 보정을 보수적으로 막았기 때문에, 실제로 귀걸이 1개만 더 보이는 이미지에서는 재현율이 일부 줄 수 있다.
- `메탈`은 색상 fallback 용도로는 더 이상 무조건 실버 처리하지 않고, explicit 색상이 없을 때만 사용하도록 조정했다.

## 결과 요약
- `블랙 메탈 안경테`는 `블랙 메탈 안경`, `진주 귀걸이`는 `화이트 진주 귀걸이`처럼 query에서 더 자연스러운 descriptor를 유지한다.
- accessory 라벨이 지원 family로 정규화되지 않으면 결과에서 제거해 `화이트 칼라` 같은 노이즈를 걸러낸다.
- Gemini 보정이 accessory 1개만 새로 덧붙이는 경우는 기본적으로 억제하고, `목걸이/팔찌/반지`처럼 세트로 나타나는 jewelry 추가는 유지한다.

## 완료 기준(DoD)
- [x] 안경/귀걸이 descriptor가 query에 반영된다.
- [x] unsupported accessory 라벨이 결과에서 제거된다.
- [x] 단일 추가 jewelry 보정 오탐이 줄어든다.
- [x] 관련 테스트가 통과한다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
