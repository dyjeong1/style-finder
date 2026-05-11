---
id: PLAN-20260421-헤더업로드초기화제거-SPEC
title: 헤더 업로드 초기화 버튼 제거 스펙
status: done
priority: P2
created_at: 2026-04-21
updated_at: 2026-04-21
related:
  plan: [PLAN-20260421-헤더업로드초기화제거]
tags: [frontend, spec, header]
---

## 1. 목적
- 헤더에서 맥락 없는 전역 초기화 버튼을 제거해 내비게이션 중심 구조로 정리한다.

## 2. 구현 범위
- `frontend/components/app-shell.tsx`
  - `업로드 초기화` 버튼 제거
  - 불필요해진 import와 핸들러 제거
- 문서
  - README/TODO 및 PLAN/TASK 문서 정리

## 3. 비범위
- 업로드 localStorage 초기화 유틸 삭제
- 업로드 페이지 내부 액션 재배치

## 4. 검증 방법
- `cd frontend && npm run build`
- 헤더 메뉴 수동 확인
