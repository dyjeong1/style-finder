---
id: PLAN-20260420-위시리스트정렬추가
title: 위시리스트 정렬 추가 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-위시리스트정렬추가]
  tasks: [TSK-0001-프론트위시리스트정렬구현]
tags: [frontend, wishlist]
---

## 1. 목표
- 위시리스트 목록을 프론트에서 여러 기준으로 정렬해 보여준다.

## 2. 기능 스펙
- 정렬 옵션: `latest`, `oldest`, `price_asc`, `price_desc`, `name_asc`
- API 응답 원본은 유지하고, 렌더 직전 파생된 정렬 배열을 사용한다.
- 상단 요약에 현재 정렬 값을 함께 노출한다.

## 3. 비기능 스펙
- 기존 카테고리 필터와 충돌 없이 동작해야 한다.
- 정렬 변경은 추가 API 호출 없이 즉시 반영되어야 한다.

## 4. 검증 스펙
- `npm run build`
- 정렬 옵션 변경 시 카드 순서가 즉시 바뀌는지 확인
