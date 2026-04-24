---
id: SPEC-PLAN-20260423-동적업로드분석및카테고리감지
title: 동적 업로드 분석 및 카테고리 감지 스펙
status: done
priority: P0
created_at: 2026-04-23
updated_at: 2026-04-24
related:
  plan: PLAN-20260423-동적업로드분석및카테고리감지
  tasks: [TSK-0001-분석및카테고리감지개선]
tags: [backend, frontend, recommendation, image-analysis]
---

## 목표
업로드 이미지마다 실제 foreground 분석과 감지 카테고리를 반영한다.

## 백엔드 스펙
- 대표 색상 분석에서 edge 배경색과 가까운 픽셀을 제외한다.
- `UploadAnalysis`의 tone/mood/silhouette/preferred_categories를 이미지 분석 결과 기반으로 구성한다.
- `build_naver_category_queries`는 category_query_hints가 있으면 해당 카테고리만 반환한다.
- `accessory` 카테고리를 검색/추론/상품 분류에 추가한다.

## 프론트 스펙
- 추천/위시리스트 카테고리 라벨과 필터에 accessory를 추가한다.
- 업로드 분석의 preferred_categories는 한글 라벨로 표시하고 검색 힌트를 함께 노출한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd frontend && npm run build`
