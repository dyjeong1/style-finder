---
id: SPEC-PLAN-20260504-프론트원복
title: 프론트 원복 스펙
status: done
priority: P1
created_at: 2026-05-04
updated_at: 2026-05-04
related:
  plan: [PLAN-20260504-프론트원복]
  tasks: [TSK-0001-최근프론트변경원복]
tags: [frontend, rollback]
---

## 1. 목적
최근 적용한 프론트 리디자인/고급화 변경을 제거하고, 사용자가 익숙한 이전 UI 상태로 빠르게 복귀합니다.

## 2. 구현 스펙
- `frontend/app/globals.css`, `frontend/components/app-shell.tsx`, 주요 메인 페이지 3개를 `0cd7e00` 기준 상태로 복원합니다.
- 최근 추가한 `PLAN-20260504-프론트서비스퀄리티업그레이드`, `PLAN-20260504-프론트디자인고급화` 문서는 제거합니다.
- 원복 작업을 기록하는 새 PLAN/TASK 문서를 추가합니다.

## 3. 비기능 스펙
- 기존 업로드/추천/위시리스트 동작은 유지합니다.
- 빌드가 깨지지 않아야 하며, 로컬 브라우저에서 바로 확인 가능해야 합니다.

## 4. 수용 기준
- [x] 최근 프론트 리디자인/고급화 커밋 효과가 사라짐
- [x] `cd frontend && npm run build` 통과
- [x] 실행 중인 프론트 서버가 원복된 화면을 서빙함
