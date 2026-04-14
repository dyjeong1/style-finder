---
id: PLAN-20260414-프론트보안업그레이드
title: 프론트 보안 업그레이드
status: done
priority: P1
created_at: 2026-04-14
updated_at: 2026-04-14
related:
  tasks: [TSK-0001-Next패치업그레이드]
tags: [frontend, security, dependency, nextjs]
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 프론트 MVP 구축 이후 실행 환경 검증을 진행하며 Next.js 보안 경고가 확인되었습니다.
- 현재 성능/운영 이슈: `next@14.2.5`는 보안 취약점이 보고된 버전으로, 패치 릴리스 적용이 필요합니다.

## 2. 목표/가설
- 1차 지표(Primary): 프론트 의존성 보안 경고 해소 및 빌드 재검증
- 2차 지표(Secondary): 현재 App Router 기반 구조를 유지하면서 회귀 없이 안전 버전 적용
- 가설: 취약점이 해소되는 최소 안전 버전으로 업그레이드하면 리스크를 낮추면서 보안 경고를 정리할 수 있습니다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - `next` 버전 패치 업그레이드
  - lockfile 재생성
  - `npm install`, `npm run build`, `npm audit` 기반 검증
- 제외 범위:
  - Next.js 메이저 버전 전환
  - 기능 UI 변경

## 4. 일정/마일스톤
- M1(보안 권고 확인): 2026-04-14
- M2(패치 업그레이드 적용): 2026-04-14
- M3(빌드/감사 검증): 2026-04-14

## 5. 리스크 & 가정
- 시스템/리소스 제약: 외부 패키지 레지스트리 및 Google Fonts 네트워크 접근이 필요합니다.
- 호환성 가정: React 18.3.1과 Next 15.5.15는 호환됩니다.

## 6. 검증/수용 기준(DoD)
- [x] `next`가 보안 패치 버전으로 상향됨
- [x] `npm install` 및 `npm run build` 성공
- [x] 문서(README/TODO/PLAN/TASK) 최신화

## 7. 변경 이력
- 2026-04-14: PLAN 생성
- 2026-04-14: `next@15.5.15` 업그레이드, `npm audit`/`npm run build` 검증 완료
