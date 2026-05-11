---
id: TSK-0021-비전평가정규화및품목보정
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-29
---

## 목적
AI 비전 예측 캐시를 평가할 때도 런타임과 동일한 정규화 경로를 적용하고, 실제 코디 이미지에서 자주 흔들리는 품목명을 보정합니다.

## 작업 내역
- [x] 캐시된 비전 예측 결과에 공통 정규화 적용
- [x] 스트라이프 니트/스웨터, 네이비 와이드 팬츠, 도트 미니 스커트 품목명 보정
- [x] 데이터셋 비교와 백엔드 테스트로 회귀 검증

## 산출물(Artifacts)
- `backend/scripts/compare_vision_predictors.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --dataset-root data/vision_dataset --baseline rule --candidate gemini --format text`
  - Gemini 정밀도/재현율: `0.6316`
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_vision_dataset_evaluator.py -q`

## 의존성/리스크
- 캐시된 provider 응답은 모델 원문을 보존하되, 비교/평가 시 서비스 런타임 정규화 결과로 해석합니다.

## 완료 기준(DoD)
- [x] Gemini 캐시 비교에서 정규화 반영 전보다 지표가 개선됨
- [x] 관련 테스트 통과
- [x] README/TODO/PLAN/루트 문서 갱신
- [x] TASK 완료 직후 커밋 완료
