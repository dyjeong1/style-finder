---
id: TSK-0001-오탐필터링및가디건정교화
plan_id: PLAN-20260424-카테고리오탐억제및아우터정교화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
없는 신발/가방 오탐을 줄이고, 가디건/점퍼/자켓 품목 추론과 검색 결과 적합도를 높인다.

## 작업 내역
- [x] 신발/가방 감지 기준 강화
- [x] 아우터 품목 추론 정교화
- [x] 상의/아우터 컴포넌트 분리 보정
- [x] 네이버 relevance 필터 추가
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/tests/test_outfit_query_hints.py`
  - `backend/tests/test_naver_shopping.py`

## 테스트/검증
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_naver_shopping.py -q`
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_naver_shopping.py backend/tests/test_api_e2e.py backend/tests/test_api_failures.py -q`

## 완료 기준(DoD)
- [x] 없는 신발/가방 오탐 감소
- [x] 가디건 relevance 개선
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] 문서 갱신
