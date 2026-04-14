---
id: TSK-0001-프론트접근성개선
plan_id: PLAN-20260414-프론트접근성및E2E확장
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-14
---

## 목적
프론트 핵심 화면의 키보드 사용성, 레이블 연결, 상태 메시지 전달을 개선합니다.

## 작업 내역
- [x] 폼/컨트롤 레이블 및 설명 연결
- [x] 상태 메시지 접근성 개선
- [x] 포커스/skip link/키보드 흐름 개선

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/(auth)/login/page.tsx`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/(main)/wishlist/page.tsx`
  - `frontend/components/app-shell.tsx`
  - `frontend/app/globals.css`

## 테스트/검증
- `cd frontend && npm run build` 성공

## 완료 기준(DoD)
- [x] 주요 화면 접근성 속성 반영
- [x] 빌드 통과
- [x] README/TODO/PLAN/TASK 갱신
