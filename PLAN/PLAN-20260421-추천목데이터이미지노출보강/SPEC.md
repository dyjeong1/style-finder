---
id: PLAN-20260421-추천목데이터이미지노출보강-SPEC
title: 추천 목데이터 이미지 노출 보강 스펙
status: done
priority: P1
created_at: 2026-04-21
updated_at: 2026-04-21
related:
  plan: [PLAN-20260421-추천목데이터이미지노출보강]
tags: [frontend, spec, mock-data]
---

## 1. 목적
- 목 상품 데이터의 깨진 이미지 URL을 사용자에게 노출하지 않고, 즉시 대체 썸네일을 보여준다.

## 2. 구현 범위
- `frontend/app/(main)/recommendations/page.tsx`
  - 목 이미지 URL 판별 함수 추가
  - `src`를 fallback SVG로 즉시 치환하는 처리 추가
- `frontend/app/(main)/wishlist/page.tsx`
  - 동일한 목 이미지 URL 판별 및 fallback 적용
- 문서
  - 현재 추천 소스가 실 API가 아니라 목데이터임을 README/TODO에 반영

## 3. 비범위
- 29CM/지그재그 공식 API 연동
- 실 상품 이미지 크롤링/동기화

## 4. 검증 방법
- `cd frontend && npm run build`
- 추천/위시리스트 응답 렌더링 시 이미지 `src` 확인
