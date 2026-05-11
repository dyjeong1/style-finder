---
id: SPEC-PLAN-20260423-직접검색어카테고리추론
title: 직접 검색어 카테고리 추론 스펙
status: done
priority: P1
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-직접검색어카테고리추론
  tasks: [TSK-0001-검색어제품군추론구현]
tags: [backend, recommendation, naver]
---

## 목표
직접 검색어에 제품군 키워드가 포함되어 있으면 해당 카테고리로만 네이버 쇼핑 후보를 조회한다.

## 백엔드 스펙
- 직접 검색어에서 상의/하의/아우터/신발/가방 계열 키워드를 감지한다.
- 감지된 제품군이 있으면 `build_custom_naver_category_queries`는 해당 카테고리 쿼리만 반환한다.
- 감지된 제품군이 없으면 기존처럼 전체 카테고리 쿼리를 반환한다.
- 개별 카테고리 필터가 명시된 경우에는 기존 필터를 우선한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 성공
