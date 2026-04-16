---
id: SPEC-PLAN-20260416-위시리스트상세화
title: 위시리스트 상세화 스펙
status: doing
priority: P1
created_at: 2026-04-16
updated_at: 2026-04-16
related:
  plan: [PLAN-20260416-위시리스트상세화]
  tasks: [TSK-0001-위시리스트상세정보노출]
tags: [wishlist, local-dev]
---

## 1. 목적
위시리스트를 단순 식별자 목록이 아니라 다시 보고 바로 활용할 수 있는 상품 목록으로 개선합니다.

## 2. 기능 스펙
- `GET /wishlist` 응답에 `product_name`, `price`, `source`, `category`, `product_url`, `image_url`를 포함합니다.
- 위시리스트 `created_at`은 최초 저장 시각을 유지합니다.
- 프론트 위시리스트 페이지에 상품 핵심 정보와 외부 링크를 노출합니다.

## 3. 비기능 스펙
- 기존 찜 추가/삭제 흐름과 API 경로는 유지합니다.
- 단일 사용자 로컬 모드와 충돌하지 않아야 합니다.

## 4. 구현 스펙
- 백엔드 인메모리 위시리스트 저장 구조를 `product_id -> created_at` 형태로 변경
- 프론트 타입과 UI를 확장된 응답에 맞게 갱신
- Playwright 및 백엔드 테스트에서 위시리스트 상세 필드를 검증

## 5. 수용 기준
- [ ] 위시리스트 목록에서 상세 상품 정보를 확인 가능
- [ ] 저장 시각이 재조회 후에도 유지됨
- [ ] 테스트/빌드 통과
