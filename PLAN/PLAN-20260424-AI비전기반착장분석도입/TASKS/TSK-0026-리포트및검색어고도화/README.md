---
id: TSK-0026-리포트및검색어고도화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-04-29
---

## 목적
런타임 AI-first 평가 결과를 샘플 단위 리포트 파일로 남길 수 있게 하고, 업로드 분석 결과의 검색어를 색상+품목 수준에서 재질/패턴/실루엣이 살아 있는 형태로 고도화한다.

## 작업 내역
- [x] 비교 스크립트에 샘플별 상세 리포트 파일 출력 추가
- [x] `build_item_query`에 재질/패턴/실루엣 descriptor 반영
- [x] 테스트와 문서 갱신

## 산출물(Artifacts)
- `backend/scripts/compare_vision_predictors.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_dataset_evaluator.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_vision_dataset_evaluator.py tests/test_naver_shopping.py -q`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --dataset-root data/vision_dataset --baseline rule --candidate runtime-ollama+gemini --format json --report-file /tmp/runtime-report.json`

## 의존성/리스크
- descriptor를 과하게 붙이면 검색어가 지나치게 길어질 수 있어, 품목별로 핵심 키워드만 제한해야 한다.
- 리포트 파일은 캐시 기준 분석 결과에 의존하므로 fresh 실행과 수치가 다를 수 있다.

## 완료 기준(DoD)
- [x] 비교 스크립트가 샘플별 baseline/candidate 상세를 파일로 저장할 수 있음
- [x] 세부 검색어가 재질/패턴 descriptor를 보존함
- [x] 테스트 통과
- [x] README/TODO/PLAN 문서 갱신
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
