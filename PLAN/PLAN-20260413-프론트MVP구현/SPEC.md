---
id: SPEC-PLAN-20260413-프론트MVP구현
title: 프론트 MVP 구현 스펙
status: review
priority: P1
created_at: 2026-04-13
updated_at: 2026-04-13
related:
  plan: [PLAN-20260413-프론트MVP구현]
  tasks: [TSK-0001-프론트스캐폴딩및핵심라우팅, TSK-0002-API연동기본흐름구현, TSK-0003-UI고도화및상태처리]
tags: [nextjs, app-router, ui]
---

## 1. 목적
스타일매치의 핵심 사용자 흐름을 프론트에서 실제로 조작/확인 가능한 MVP 인터페이스로 제공합니다.

## 2. 기능 스펙
- 로그인 화면
- 이미지 업로드 화면
- 추천 목록 화면
- 찜 목록 화면

## 3. 비기능 스펙
- 반응형 레이아웃(모바일/데스크톱)
- 공통 테마 변수 및 일관된 컴포넌트 스타일

## 4. 구현 스펙
- 경로: `frontend/app/*`
- 공통 컴포넌트: `frontend/components/*`
- API 유틸: `frontend/lib/api.ts`

## 5. 수용 기준
- [x] Next.js 프로젝트 골격 완성
- [x] 핵심 라우트 페이지 렌더링 구조 확인
- [ ] 문서 최신화 완료
