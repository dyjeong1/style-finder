---
id: SPEC-PLAN-20260423-신발검색어추론확장
title: 신발 검색어 추론 확장 스펙
status: done
priority: P1
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-신발검색어추론확장
  tasks: [TSK-0001-신발품목키워드확장]
tags: [backend, recommendation, naver]
---

## 목표
신발 하위 품목명이 포함된 직접 검색어를 신발 카테고리로 추론한다.

## 백엔드 스펙
- `CATEGORY_KEYWORDS["shoes"]`에 메리제인, 구두, 슬리퍼, 플랫, 힐, 펌프스, 뮬 등 대표 품목을 추가한다.
- `build_custom_naver_category_queries("블랙 메리제인")`은 `[("shoes", "블랙 메리제인 신발")]` 또는 동등한 신발 단일 쿼리를 반환한다.
- 기존 제품군 없는 검색어는 전체 카테고리 쿼리를 유지한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 성공
