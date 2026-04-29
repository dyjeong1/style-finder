---
id: PLAN-20260421-프론트메뉴및페이지타이틀한글화-SPEC
title: 프론트 메뉴 및 페이지 타이틀 한글화 스펙
status: done
priority: P2
created_at: 2026-04-21
updated_at: 2026-04-21
related:
  plan: [PLAN-20260421-프론트메뉴및페이지타이틀한글화]
tags: [frontend, spec, localization]
---

## 1. 목적
- 상단 메뉴와 핵심 페이지 타이틀, 상단 액션 라벨을 한국어 중심으로 맞춘다.

## 2. 구현 범위
- `frontend/components/app-shell.tsx`
  - 상단 메뉴 라벨 한글화
  - 우측 액션 버튼 한글화
- `frontend/app/layout.tsx`
  - 기본 메타데이터 한국어화
- `frontend/app/(main)/upload/page.tsx`
  - 브라우저 탭 제목 설정
  - 분석 패널 타이틀 한글화
- `frontend/app/(main)/recommendations/page.tsx`
  - 페이지 대표 타이틀, 상단 요약, 필터/버튼, 카드 액션 한글화
  - 브라우저 탭 제목 설정
- `frontend/app/(main)/wishlist/page.tsx`
  - 페이지 대표 타이틀, 상단 요약, 필터/버튼 한글화
  - 브라우저 탭 제목 설정

## 3. 비범위
- API 응답 필드명 변경
- 이미지 내 fallback SVG 텍스트 전체 한글화
- 전체 서비스 카피 전수 변경

## 4. 검증 방법
- `npm run build`
- 수동 확인: `/upload`, `/recommendations`, `/wishlist`
