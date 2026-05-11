---
id: SPEC-PLAN-20260420-추천저장상태연결
title: 추천 저장 상태 연결 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-추천저장상태연결]
  tasks: [TSK-0001-추천저장배지및중복방지]
tags: [frontend, wishlist, recommendation]
---

## 1. 목적
추천 결과에서 이미 저장된 상품을 즉시 식별하게 만들어, 위시리스트와 추천 화면이 자연스럽게 연결되도록 합니다.

## 2. 기능 스펙
- 추천 화면 로드 시 위시리스트를 함께 조회해 저장된 `product_id`를 식별합니다.
- 저장된 상품 카드에는 `Saved` 배지를 표시합니다.
- 저장된 상품의 `Add to Wishlist` 버튼은 비활성화하고 저장 상태 문구를 보여줍니다.
- 새로 찜한 상품은 즉시 저장 상태로 반영합니다.

## 3. 비기능 스펙
- 기존 추천 API 및 위시리스트 API는 유지합니다.
- 모바일 카드 레이아웃을 유지해야 합니다.
- 빌드 오류 없이 동작해야 합니다.

## 4. 구현 스펙
- `frontend/app/(main)/recommendations/page.tsx`에서 위시리스트 조회 상태를 함께 관리
- `frontend/app/globals.css`에 Saved 배지/비활성 버튼 스타일 추가
- 루트/프론트 문서에 연결 상태 개선 내용 반영

## 5. 수용 기준
- [x] Saved 배지와 비활성 버튼 반영
- [x] 저장 직후 카드 상태 즉시 반영
- [x] `cd frontend && npm run build` 통과
