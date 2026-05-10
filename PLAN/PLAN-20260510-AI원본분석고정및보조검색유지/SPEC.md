---
id: PLAN-20260510-AI원본분석고정및보조검색유지-SPEC
plan_id: PLAN-20260510-AI원본분석고정및보조검색유지
title: AI 원본 분석 고정 및 보조 검색 유지 스펙
status: ready
priority: P1
created_at: 2026-05-10
updated_at: 2026-05-10
---

## 1. 요구사항
1. AI가 정상 응답한 경우 `detected_items`와 `category_query_hints`는 규칙 분석으로 다시 보정하지 않는다.
2. AI 실패 시 최후 fallback 으로서의 규칙 분석 경로는 유지한다.
3. 네이버 쇼핑 보조 query 1개 추가와 후보 재정렬은 유지한다.

## 2. 상태 관리 규칙
- AI 분석 성공 경로와 규칙 fallback 경로를 다시 섞지 않는다.
- same-category 품목명 교체 테스트는 제거한다.
- 검색 품질 개선 범위는 유지 문서에 명시한다.

## 3. 검증 시나리오
- AI 성공 시 `resolve_detected_items`는 AI 결과만 반환한다.
- AI 실패 시에는 기존처럼 규칙 fallback 이 동작한다.
- 네이버 query variant 테스트는 계속 통과한다.
