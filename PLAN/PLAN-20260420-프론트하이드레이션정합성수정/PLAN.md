---
id: PLAN-20260420-프론트하이드레이션정합성수정
title: 프론트 하이드레이션 정합성 수정
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  tasks: [TSK-0001-추천페이지로컬상태동기화]
tags: [frontend, hydration, nextjs]
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 추천/위시리스트 흐름 자체는 동작하지만, 브라우저에서 페이지 이동 시 React hydration mismatch 오류가 보였습니다.
- 현재 성능/운영 이슈: SSR 결과와 클라이언트 첫 렌더가 달라 추천 화면과 연관 라우트에서 경고/복구 렌더가 발생했습니다.

## 2. 목표/가설
- 1차 지표(Primary): 추천/위시리스트 이동 시 hydration 오류 제거
- 2차 지표(Secondary): 추천 화면 초기 렌더 안정화
- 가설: `localStorage` 기반 상태를 초기 렌더가 아니라 mount 이후 동기화하면 SSR/CSR 정합성이 맞춰집니다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - 추천 페이지의 로컬 상태 초기화 방식 수정
  - 문서/빌드 검증
- 제외 범위:
  - API 변경
  - 위시리스트 기능 확장

## 4. 일정/마일스톤
- M1(PLAN/SPEC 작성): 2026-04-20
- M2(프론트 수정): 2026-04-20
- M3(빌드/문서 정리): 2026-04-20

## 5. 리스크 & 가정
- 가정: 문제의 핵심은 `localStorage`를 렌더 시점에 읽는 부분입니다.
- 리스크: 로컬 상태를 늦게 읽게 되면 첫 렌더 메시지가 잠깐 보일 수 있어 빈 상태 처리 문구를 자연스럽게 유지해야 합니다.

## 6. 검증/수용 기준(DoD)
- [x] 추천/위시리스트 이동 시 hydration 오류가 재현되지 않음
- [x] 프론트 빌드 통과
- [x] README/TODO/PLAN/TASK 문서 갱신

## 7. 변경 이력
- 2026-04-20: PLAN 생성
- 2026-04-20: 추천 페이지 localStorage 동기화 시점을 mount 이후로 조정해 hydration mismatch 수정 완료
