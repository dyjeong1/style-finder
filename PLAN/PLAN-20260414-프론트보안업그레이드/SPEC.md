---
id: SPEC-PLAN-20260414-프론트보안업그레이드
title: 프론트 보안 업그레이드 스펙
status: done
priority: P1
created_at: 2026-04-14
updated_at: 2026-04-14
related:
  plan: [PLAN-20260414-프론트보안업그레이드]
  tasks: [TSK-0001-Next패치업그레이드]
tags: [security, nextjs, dependency]
---

## 1. 목적
보안 경고가 있는 Next.js 버전을 패치 릴리스로 업그레이드해 프론트 실행 환경을 안정화합니다.

## 2. 기능 스펙
- `next` 의존성 버전 상향
- lockfile 최신화
- 설치/빌드/감사 결과 확인

## 3. 비기능 스펙
- 기존 App Router 구조 유지
- React 및 타입 패키지와의 호환성 유지

## 4. 구현 스펙
- 경로: `frontend/package.json`, `frontend/package-lock.json`
- 검증: `npm install`, `npm run build`, `npm audit`

## 5. 수용 기준
- [x] 패치 권고 버전 적용
- [x] 프론트 빌드 성공
- [x] 문서 최신화 완료
