---
id: TSK-0001-AI원본분석유지
plan_id: PLAN-20260510-AI원본분석고정및보조검색유지
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-10
---

## 목적
AI 감지 품목은 규칙 분석으로 다시 보정하지 않고 그대로 유지하되, 네이버 검색의 보조 query 와 후보 정렬은 그대로 남깁니다.

## 작업 내역
- [x] same-category 규칙 보정 제거
- [x] 관련 테스트 정리
- [x] 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/tests/test_ai_search_path.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_ai_search_path.py tests/test_naver_shopping.py tests/test_store_color_matching.py -q`
- `cd backend && python3 -m pytest tests/test_api_e2e.py tests/test_vision_outfit_analyzer.py tests/test_outfit_query_hints.py -q`

## 의존성/리스크
- AI 일반 품목명이 더 추상적으로 남을 수 있지만, 분석 결과 일관성을 우선합니다.
- 검색 품질 저하를 막기 위해 query variant 와 후보 재정렬은 유지합니다.

## 완료 기준(DoD)
- [x] AI 성공 시 규칙 보정이 개입하지 않는다.
- [x] fallback 경로와 검색 보강 경로가 각각 유지된다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
