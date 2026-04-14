---
id: SPEC-PLAN-20260414-프론트접근성및E2E확장
title: 프론트 접근성 및 E2E 확장 스펙
status: done
priority: P1
created_at: 2026-04-14
updated_at: 2026-04-14
related:
  plan: [PLAN-20260414-프론트접근성및E2E확장]
  tasks: [TSK-0001-프론트접근성개선, TSK-0002-PlaywrightE2E구현]
tags: [frontend, accessibility, playwright]
---

## 1. 목적
프론트 사용자 경험을 접근성 측면에서 개선하고, 핵심 흐름을 브라우저 수준에서 자동 검증합니다.

## 2. 기능 스펙
- 상태 메시지/레이블/키보드 흐름 보강
- Playwright 테스트 구성 추가
- 로그인→업로드→추천→찜 흐름 테스트 추가

## 3. 비기능 스펙
- 모바일/데스크톱 공통 포커스 가시성 유지
- 테스트는 재현 가능하도록 API mock 기반 사용

## 4. 구현 스펙
- 경로: `frontend/app/*`, `frontend/components/*`, `frontend/e2e/*`
- 테스트 도구: `@playwright/test`

## 5. 수용 기준
- [x] 접근성 개선 반영
- [x] Playwright E2E 통과
- [x] 문서 최신화 완료
