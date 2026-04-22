---
id: SPEC-PLAN-20260422-네이버연동진단표시
title: 네이버 연동 진단 표시 스펙
status: done
priority: P1
created_at: 2026-04-22
updated_at: 2026-04-22
related:
  plan: PLAN-20260422-네이버연동진단표시
  tasks: [TSK-0001-네이버실패사유표시]
tags: [naver, recommendation, diagnostics]
---

## 목표
네이버 쇼핑 검색 API 호출 실패 시 기존 샘플 추천 fallback을 유지하면서, 사용자가 원인을 알 수 있도록 API 응답과 프론트 화면에 진단 메시지를 제공한다.

## 백엔드 스펙
- `NaverShoppingClient.search(...)`는 상품 목록과 실패 사유를 함께 반환한다.
- 기존 `search_products(...)`는 호환성을 위해 상품 목록만 반환한다.
- 추천 API 응답 필드:
  - `source`: `naver_shopping` 또는 `mock`
  - `query`: 네이버 검색어
  - `fallback_reason`: 실패 사유 코드 또는 `null`
  - `fallback_message`: 사용자 안내 문구 또는 `null`

## 프론트 스펙
- 추천 페이지가 `fallback_message`를 받으면 데이터 소스 안내 아래에 경고 문구로 표시한다.
- 상품 목록은 기존 fallback 결과를 그대로 렌더링한다.

## 검증
- 네이버 키 미설정/인증 실패 상황에서도 추천 API가 200을 반환하고 샘플 데이터가 표시된다.
- 테스트와 빌드가 통과한다.
