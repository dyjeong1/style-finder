---
id: TSK-0001-AI프롬프트와검색정확도보강
plan_id: PLAN-20260510-AI프롬프트및네이버검색정확도고도화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-10
---

## 목적
AI가 더 정확한 쇼핑용 품목명과 query 를 처음부터 생성하게 만들고, 감지 품목/검색어를 바탕으로 네이버 쇼핑 검색 품질을 더 높입니다.

## 작업 내역
- [x] AI 프롬프트 강화
- [x] 감지 item 중심 보조 query 생성 보강
- [x] 네이버 후보 정렬 penalty 보강
- [x] 최종 추천 exact match 세분화
- [x] 테스트 및 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/services/naver_shopping.py`
- `backend/src/services/store.py`
- `backend/tests/test_naver_shopping.py`
- `backend/tests/test_store_color_matching.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_naver_shopping.py tests/test_store_color_matching.py -q`
- `cd backend && python3 -m pytest tests/test_ai_search_path.py tests/test_naver_shopping.py tests/test_store_color_matching.py tests/test_api_e2e.py tests/test_vision_outfit_analyzer.py tests/test_outfit_query_hints.py -q`

## 의존성/리스크
- prompt 강화만으로 모든 품목 ambiguity 가 해결되지는 않으므로 query variant/재정렬과 함께 봐야 합니다.
- mismatch penalty 가 지나치게 세면 recall 이 줄 수 있으므로 검색 후보 제거가 아니라 정렬 위주로 적용합니다.

## 완료 기준(DoD)
- [x] AI가 더 쇼핑 친화적인 품목명/query 를 유도받는다.
- [x] 감지 item 기반 보조 query 가 생성된다.
- [x] 네이버 후보와 최종 랭킹이 brand/family/intent 정합성을 더 반영한다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
