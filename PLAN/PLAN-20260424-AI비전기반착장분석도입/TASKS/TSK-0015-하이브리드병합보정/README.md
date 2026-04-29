---
id: TSK-0015-하이브리드병합보정
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.6d
updated_at: 2026-04-29
---

## 목적
AI 비전 결과와 규칙 기반 결과를 같은 카테고리 안에서 비교해, 색상/세부 품목이 더 신뢰할 만한 쪽으로 보정하는 하이브리드 병합 로직을 추가한다.

## 작업 내역
- [x] 기존 병합 로직 분석
- [x] 카테고리별 보정 규칙 추가
- [x] 테스트 보강
- [x] 실샘플 재검증 및 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `README.md`
- `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_3.png --provider ollama --timeout-seconds 120`

## 결과 요약
- `merge_detected_items`가 같은 품목 계열일 때 fallback 결과를 재활용하도록 보강했다.
- `top`으로 잘못 들어온 `가디건`을 fallback의 `outer`와 맞춰 재배치하는 규칙을 추가했다.
- `bottom`에서 `데님 팬츠`와 `와이드 데님 팬츠`처럼 같은 계열의 세부명 차이는 specificity가 더 높은 fallback으로 보정한다.
- `codytest_2` 실검증 결과는 `화이트 셔츠 / 블루 가디건 / 블랙 데님 팬츠 / 블랙 안경`으로 정리되었다.
- `codytest_3`는 fallback 자체가 `브라운 가디건 / 브라운 바지 / 화이트 양말` 방향으로 흔들려, 다음 단계에서는 fallback 분석 품질을 직접 개선해야 한다.

## 의존성/리스크
- 규칙 기반을 너무 강하게 우선하면 AI 모델 고유의 장점이 사라질 수 있다.
- 보정은 같은 품목 계열일 때만 제한적으로 적용해야 한다.

## 완료 기준(DoD)
- [x] 하이브리드 병합 보정이 코드에 추가된다.
- [x] 관련 테스트가 통과한다.
- [x] 실샘플에서 일부 색상/품목 정합성이 개선된다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
