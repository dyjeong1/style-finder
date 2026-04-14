---
id: SPEC-PLAN-20260414-프론트E2ECI연동
title: 프론트 E2E CI 연동 스펙
status: done
priority: P1
created_at: 2026-04-14
updated_at: 2026-04-14
related:
  plan: [PLAN-20260414-프론트E2ECI연동]
  tasks: [TSK-0001-Playwright워크플로우추가]
tags: [github-actions, playwright, ci]
---

## 1. 목적
프론트 Playwright E2E를 GitHub Actions에서 자동 실행해 품질 확인을 자동화합니다.

## 2. 기능 스펙
- `frontend/**` 변경 시 워크플로우 실행
- Node 설정 및 의존성 설치
- Playwright Chromium 설치 및 E2E 실행
- 테스트 리포트 업로드

## 3. 비기능 스펙
- 백엔드 워크플로우와 유사한 구조 유지
- 실패 시에도 아티팩트 업로드

## 4. 구현 스펙
- 경로: `.github/workflows/frontend-e2e.yml`
- 실행 명령: `npm ci`, `npx playwright install --with-deps chromium`, `npm run test:e2e`

## 5. 수용 기준
- [x] 워크플로우 파일 추가
- [x] Playwright E2E 실행 단계 반영
- [x] 문서 최신화 완료
