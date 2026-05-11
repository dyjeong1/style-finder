---
id: TSK-0016-선택적제미나이보정
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.8d
updated_at: 2026-04-29
---

## 목적
로컬 Ollama 분석 결과 중 상의/아우터 레이어드, 색상 충돌, generic 품목명이 나타나는 경우에만 Gemini를 보조 분석기로 호출해 오인식을 선택적으로 보정한다.

## 작업 내역
- [x] 선택적 Gemini 보정 트리거 정의
- [x] 보조 분석기 주입 및 병합 로직 구현
- [x] 테스트 보강
- [x] 실샘플 재검증
- [x] README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/core/config.py`
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `README.md`
- `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_3.png --provider ollama --timeout-seconds 120`

## 의존성/리스크
- Gemini 무료 티어 quota에 따라 보조 보정 호출이 제한될 수 있다.
- 너무 넓게 호출하면 로컬 무료 경로의 장점이 줄어들 수 있으므로, ambiguous category에만 적용해야 한다.

## 결과 요약
- 기본 경로는 `Ollama + gemma3:4b`를 유지하고, `top/outer` 레이어드가 동시에 보이거나 fallback과 색상/품목명이 충돌하는 경우에만 Gemini를 추가 호출한다.
- 선택 보정 대상 카테고리는 `top`, `outer`, `bottom`, `accessory`로 제한했다.
- Gemini 보정이 있으면 해당 카테고리만 교체하고, `shoes`, `bag` 등 나머지 카테고리는 기존 Ollama/규칙 기반 결과를 유지한다.
- `codytest_2` 실검증 결과:
  - `화이트 슬리브리스 탑 / 블루 가디건 / 블랙 와이드 팬츠 / 블랙 안경 / 블랙 귀걸이`
- `codytest_3` 실검증 결과:
  - `화이트 티셔츠 / 블루 가디건 / 브라운 와이드 팬츠 / 화이트 운동화 / 브라운 가방 / 그레이 체인 팔찌 / 화이트 양말`
- `codytest_3`처럼 가방/하의 세부명은 아직 완벽하지 않아서, 다음 단계는 fallback 분석 자체 개선이 우선이다.

## 완료 기준(DoD)
- [x] Ollama 1차 분석 후 필요한 카테고리에만 Gemini 보조 보정이 적용된다.
- [x] 관련 테스트가 통과한다.
- [x] 실샘플에서 상의/아우터/악세서리 정합성이 일부 개선된다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
