---
id: TSK-0001-비전분석초기구조도입
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
AI 비전 모델을 나중에 연결할 수 있도록 데이터셋 구조, 공통 출력 포맷, 분석 인터페이스를 먼저 도입한다.

## 작업 내역
- [x] PLAN/SPEC/TASK 문서 생성
- [x] 데이터셋 폴더 및 라벨 예시 추가
- [x] 비전 분석 인터페이스 초안 구현
- [x] 테스트/루트 문서 갱신

## 산출물(Artifacts)
- 문서 경로:
  - `PLAN/PLAN-20260424-AI비전기반착장분석도입/PLAN.md`
  - `PLAN/PLAN-20260424-AI비전기반착장분석도입/SPEC.md`
- 코드 경로:
  - `backend/src/services/vision_outfit_analyzer.py`
  - `backend/src/services/store.py`
- 데이터셋 경로:
  - `backend/data/vision_dataset/README.md`
  - `backend/data/vision_dataset/labels/sample-flatlay-001.json`

## 테스트/검증
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_vision_outfit_analyzer.py backend/tests/test_outfit_query_hints.py -q`

## 완료 기준(DoD)
- [x] 데이터셋 구조 및 예시 라벨 추가
- [x] 비전 분석 인터페이스와 fallback 로직 추가
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신

## 완료 메모
- `VisionOutfitAnalyzer` 인터페이스와 `merge_detected_items` fallback 전략을 추가했다.
- 현재는 `disabled/mock` provider만 지원하며, 다음 단계에서 실제 비전 모델 provider를 연결한다.
