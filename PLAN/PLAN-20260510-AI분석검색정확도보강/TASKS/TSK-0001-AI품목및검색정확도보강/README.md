---
id: TSK-0001-AI품목및검색정확도보강
plan_id: PLAN-20260510-AI분석검색정확도보강
owner: codex
status: done
estimate: 0.6d
updated_at: 2026-05-10
---

## 목적
AI 감지 품목이 지나치게 일반적일 때 같은 카테고리 안에서만 세부 품목명을 보정하고, 네이버 검색/후보 정렬/추천 랭킹까지 AI query 의도를 더 강하게 반영합니다.

## 작업 내역
- [x] same-category 규칙 품목 보정 추가
- [x] 네이버 query variant 생성 추가
- [x] 네이버 후보 재정렬 로직 보강
- [x] 추천 랭킹의 품목군/디스크립터 정합성 보너스 보강
- [x] 테스트 및 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/recommendation_intent.py`
- `backend/src/services/store.py`
- `backend/src/services/naver_shopping.py`
- `backend/src/api/routes/recommendation.py`
- `backend/tests/test_ai_search_path.py`
- `backend/tests/test_naver_shopping.py`
- `backend/tests/test_store_color_matching.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_ai_search_path.py tests/test_naver_shopping.py tests/test_store_color_matching.py -q`
- `cd backend && python3 -m pytest tests/test_api_e2e.py tests/test_vision_outfit_analyzer.py tests/test_outfit_query_hints.py -q`

## 의존성/리스크
- 품목군/디스크립터 매칭을 과하게 넓히면 다른 카테고리 상품까지 끌어올릴 수 있으므로, 같은 카테고리 기준과 제한된 alias 사전을 함께 유지해야 합니다.
- 보조 query 가 너무 많아지면 외부 API 호출 수가 늘어나므로 최대 1개 variant 만 유지합니다.

## 완료 기준(DoD)
- [x] 일반 품목명이 제한적으로 세부 품목명으로 보정된다.
- [x] 네이버 검색이 보조 query 와 재정렬을 사용한다.
- [x] 추천 랭킹이 품목군/디스크립터 정합성을 반영한다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
