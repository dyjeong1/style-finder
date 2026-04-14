---
id: TSK-0002-PlaywrightE2E구현
plan_id: PLAN-20260414-프론트접근성및E2E확장
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-14
---

## 목적
Playwright 기반으로 프론트 핵심 흐름 E2E 테스트를 도입합니다.

## 작업 내역
- [x] Playwright 의존성/설정 추가
- [x] 핵심 사용자 흐름 테스트 작성
- [x] 테스트 실행 및 문서화

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/package.json`
  - `frontend/package-lock.json`
  - `frontend/playwright.config.ts`
  - `frontend/e2e/core-flow.spec.ts`
  - `.gitignore`

## 테스트/검증
- `cd frontend && npx playwright install chromium` 성공
- `cd frontend && npm run test:e2e` 성공

## 완료 기준(DoD)
- [x] Playwright 의존성/설정 반영
- [x] 핵심 흐름 테스트 구현
- [x] README/TODO/PLAN/TASK 갱신
