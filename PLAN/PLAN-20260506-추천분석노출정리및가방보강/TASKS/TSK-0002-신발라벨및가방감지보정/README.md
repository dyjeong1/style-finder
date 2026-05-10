---
id: TSK-0002-신발라벨및가방감지보정
plan_id: PLAN-20260506-추천분석노출정리및가방보강
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-10
---

## 목적
추천 분석 패널에서 `바레즈`처럼 이해하기 어려운 신발명이 보이지 않도록 정규화하고, 좌측에 든 가방을 놓치는 전신 코디에서 `bag` 감지를 다시 보강합니다.

## 작업 내역
- [x] 실제 주석 업로드 이미지/응답 확인
- [x] 비표준 신발 라벨 정규화 규칙 추가
- [x] 좌측 가방 heuristic 보강
- [x] 회귀 테스트 검증
- [x] README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/services/image_analysis.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/tests/test_outfit_query_hints.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && python3 -m pytest tests/test_outfit_query_hints.py -q`
- `cd backend && python3 -m pytest tests/test_api_e2e.py -q`

## 의존성/리스크
- 신발 라벨을 과하게 치환하면 실제 다른 신발 품목 의미를 좁혀버릴 수 있습니다.
- 가방 heuristic을 넓히면 좌우 배경 오브젝트를 가방으로 오탐할 위험이 있어, 전신 코디 회귀 테스트로 경계를 고정해야 합니다.

## 완료 기준(DoD)
- [x] `바레즈` 같은 비표준 신발 라벨이 서비스형 표현으로 정리된다.
- [x] 좌측에 든 가방이 있는 전신 코디에서 `bag` query hint가 복원된다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
