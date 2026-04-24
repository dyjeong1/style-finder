---
id: SPEC-PLAN-20260424-카테고리오탐억제및아우터정교화
title: 카테고리 오탐 억제 및 아우터 정교화 스펙
status: done
priority: P0
created_at: 2026-04-24
updated_at: 2026-04-24
related:
  plan: PLAN-20260424-카테고리오탐억제및아우터정교화
  tasks: [TSK-0001-오탐필터링및가디건정교화]
tags: [recommendation, naver, image-analysis]
---

## 목표
없는 카테고리와 잘못된 품목 결과를 더 강하게 걸러낸다.

## 백엔드 스펙
- 신발/가방은 더 엄격한 컴포넌트 기준을 만족할 때만 카테고리로 채택한다.
- 아우터 라벨은 높이/폭/색상 특성을 사용해 가디건 쪽으로 더 정교하게 추론한다.
- 네이버 검색 결과는 category hint/query 품목 키워드와 실제 상품 제목/카테고리가 맞을 때만 유지한다.

## 검증
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_naver_shopping.py -q`
- `cd frontend && npm run build`
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_naver_shopping.py backend/tests/test_api_e2e.py backend/tests/test_api_failures.py -q`
