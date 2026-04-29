---
id: SPEC-PLAN-20260422-추천카테고리다양화
title: 추천 카테고리 다양화 스펙
status: done
priority: P1
created_at: 2026-04-22
updated_at: 2026-04-22
related:
  plan: PLAN-20260422-추천카테고리다양화
  tasks: [TSK-0001-네이버카테고리분산조회]
tags: [recommendation, naver, category]
---

## 목표
추천 페이지의 전체 보기에서 단일 제품군 쏠림을 줄이고, 카테고리별 후보를 함께 가져온다.

## 백엔드 스펙
- 전체 추천(`category=None`)일 때 검색 카테고리 순서는 `top`, `bottom`, `outer`, `shoes`, `bag`이다.
- 각 카테고리마다 `build_naver_query(analysis, category)`로 검색어를 생성한다.
- 전체 추천의 카테고리별 조회 수는 `ceil(limit / 5)` 이상, 최소 3개로 한다.
- 상품 ID 기준으로 중복을 제거한다.
- 특정 카테고리 필터가 있으면 기존처럼 해당 카테고리 하나만 조회한다.

## 응답 스펙
- `source`: 네이버 후보가 있으면 `naver_shopping`, 없으면 `mock`
- `query`: 단일 검색이면 단일 검색어, 전체 검색이면 카테고리별 검색어를 ` / `로 연결한 문자열
- fallback 관련 필드는 기존 동작 유지

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` → 12 passed
- `cd frontend && npm run build` → 성공
