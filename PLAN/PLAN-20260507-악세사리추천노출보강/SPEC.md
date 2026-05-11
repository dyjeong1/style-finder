---
id: PLAN-20260507-악세사리추천노출보강
title: 악세사리 추천 노출 보강 스펙
status: ready
priority: P1
created_at: 2026-05-07
updated_at: 2026-05-07
related:
  plan:
    - PLAN-20260507-악세사리추천노출보강
  tasks:
    - TSK-0001-악세사리카테고리노출보강
tags:
  - backend
  - recommendations
  - accessory
---

## 1. 요구사항
1. 전체 추천(`category` 미지정)에서는 감지된 카테고리와 검색 힌트가 있는 카테고리별로 최소 1개 추천 상품을 남긴다.
2. 카테고리 필터가 명시된 경우에는 기존처럼 해당 카테고리 결과만 점수순으로 자른다.
3. 각 상품의 기존 rank 값은 전체 정렬 기준을 유지한다.

## 2. 상태 관리 규칙
- 우선 보장 대상 카테고리는 `category_query_hints`가 있으면 그 키를 따르고, 없으면 `preferred_categories`를 따른다.
- 최소 노출 보장으로 선택된 상품과 일반 상위 상품을 합친 뒤, 원래 rank 순서대로 다시 정렬한다.
- 실제 후보 상품이 없는 카테고리는 억지로 빈 섹션을 만들지 않는다.

## 3. 검증 시나리오
- `top`, `bottom`, `accessory`가 감지된 업로드에서 `accessory` 후보 점수가 낮더라도 상위 limit 결과에 악세사리 상품 1개가 남는다.
- 개별 카테고리 필터 추천은 기존처럼 단순 점수순 결과를 반환한다.
