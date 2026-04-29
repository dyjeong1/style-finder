---
id: PLAN-20260420-브랜드아이콘교체
title: 브랜드 아이콘 교체 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-브랜드아이콘교체]
  tasks: [TSK-0001-헤더로고적용]
tags: [frontend, branding, asset]
---

## 1. 목표
- 좌측 상단 헤더 아이콘을 제공된 로고 이미지로 교체한다.

## 2. 기능 스펙
- 로고 이미지를 `frontend/public/brand/stylefinder_logo.png`에 배치한다.
- 헤더 브랜드 마크는 문자 `S` 대신 이미지 로고를 렌더링한다.
- 기존 브랜드 텍스트와 네비게이션 구조는 유지한다.

## 3. 비기능 스펙
- 헤더 높이가 과도하게 바뀌지 않도록 현재 브랜드 마크 영역 크기 안에서 조정한다.
- 빌드 오류 없이 정적 페이지 생성이 가능해야 한다.

## 4. 검증 스펙
- `cd frontend && npm run build`
- `/upload`에서 좌측 상단 로고 노출 확인
