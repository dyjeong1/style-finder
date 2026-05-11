---
id: TSK-0002-프론트인증제거및흐름단순화
plan_id: PLAN-20260416-단일사용자모드전환
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-16
---

## 목적
프론트에서 로그인/로그아웃 UI와 토큰 저장을 제거하고, 업로드부터 추천/찜까지 바로 이어지는 단순한 로컬 사용 흐름을 만듭니다.

## 작업 내역
- [x] 토큰 저장/로그인 의존 제거
- [x] 네비게이션과 `/login` 처리 단순화
- [x] Playwright 시나리오와 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/lib/api.ts`
  - `frontend/app/(auth)/login/page.tsx`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/(main)/wishlist/page.tsx`
  - `frontend/components/app-shell.tsx`
  - `frontend/e2e/core-flow.spec.ts`
  - `frontend/playwright.config.ts`
- 문서:
  - `frontend/README.md`
  - `README.md`
  - `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`
- `cd frontend && npm run test:e2e`

## 의존성/리스크
- 백엔드 단일 사용자 모드가 먼저 반영되어야 합니다.

## 완료 기준(DoD)
- [x] 프론트 빌드/E2E 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
