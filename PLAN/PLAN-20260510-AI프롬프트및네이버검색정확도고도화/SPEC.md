---
id: PLAN-20260510-AI프롬프트및네이버검색정확도고도화-SPEC
plan_id: PLAN-20260510-AI프롬프트및네이버검색정확도고도화
title: AI 프롬프트 및 네이버 검색 정확도 고도화 스펙
status: ready
priority: P1
created_at: 2026-05-10
updated_at: 2026-05-10
---

## 1. 요구사항
1. AI 프롬프트는 `가방`, `신발` 같은 일반 표현보다 쇼핑몰 상품명에 바로 쓰일 세부 품목명을 우선 유도해야 한다.
2. 네이버 보조 query 는 감지 item 의 `brand`, `color`, `item_label`, `intent`를 우선 사용해 원본 query보다 더 짧고 핵심적인 형태로 만든다.
3. 네이버 후보 정렬은 category 일치 외에도 family, brand, intent 일치 여부를 더 강하게 반영해야 한다.
4. 최종 추천 랭킹은 exact 품목명 일치 상품 중에서도 brand/intent/descriptors 가 더 맞는 상품을 더 높게 둘 수 있어야 한다.

## 2. 상태 관리 규칙
- AI 분석 성공 경로는 그대로 유지하고, 규칙 보정은 다시 섞지 않는다.
- 보조 query 는 카테고리당 최대 1개만 유지한다.
- mismatch penalty 는 후보 제거보다 정렬 우선으로 적용한다.

## 3. 검증 시나리오
- `남색 롱슬리브 티셔츠`와 감지 item `티셔츠`가 있으면 보조 query 로 `네이비 긴팔 티셔츠`가 생성된다.
- `뉴발란스 블랙 메리제인 슈즈` query 에서 `나이키 블랙 로퍼`보다 `뉴발란스 블랙 메리제인 슈즈`가 앞선다.
- 같은 `메리제인 슈즈` 매치라도 brand 가 맞는 상품이 더 높은 exact match bonus 를 받는다.
