---
id: SPEC-PLAN-20260420-프론트하이드레이션정합성수정
title: 프론트 하이드레이션 정합성 수정 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-프론트하이드레이션정합성수정]
  tasks: [TSK-0001-추천페이지로컬상태동기화]
tags: [frontend, hydration, nextjs]
---

## 1. 목적
추천 페이지가 SSR과 클라이언트 렌더 간 같은 초기 DOM을 유지하게 만들어 hydration 오류를 제거합니다.

## 2. 기능 스펙
- `uploadedImageId`, `uploadedImageAnalysis`는 렌더 시점의 `useMemo` 대신 mount 이후 `useEffect`에서 읽습니다.
- 추천 데이터 조회는 로컬 상태 동기화가 끝난 뒤 실행합니다.
- 분석 패널은 클라이언트 동기화 후에만 표시되도록 정리합니다.

## 3. 비기능 스펙
- 기존 추천 기능과 필터/저장 흐름은 유지합니다.
- 빌드 오류 없이 동작해야 합니다.

## 4. 구현 스펙
- `frontend/app/(main)/recommendations/page.tsx` 상태 초기화/이펙트 순서 조정
- 문서 갱신

## 5. 수용 기준
- [x] hydration 오류 비재현
- [x] `cd frontend && npm run build` 통과
