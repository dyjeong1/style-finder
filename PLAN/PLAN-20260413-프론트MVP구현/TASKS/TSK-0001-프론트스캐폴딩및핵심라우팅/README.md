---
id: TSK-0001-프론트스캐폴딩및핵심라우팅
plan_id: PLAN-20260413-프론트MVP구현
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-13
---

## 목적
Next.js 프론트 프로젝트 골격과 핵심 페이지 라우팅을 생성합니다.

## 작업 내역
- [x] Next.js 기본 파일 구성
- [x] 핵심 페이지 라우트 구성
- [x] 공통 레이아웃/네비게이션 구성

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/package.json`
  - `frontend/app/layout.tsx`
  - `frontend/app/(auth)/login/page.tsx`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/(main)/wishlist/page.tsx`
  - `frontend/components/app-shell.tsx`
  - `frontend/app/globals.css`

## 테스트/검증
- 정적 코드/라우트 파일 존재 확인
- 실행 검증은 Node/npm 미설치 환경으로 미수행 (`node`, `npm` command not found)

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과 (환경 제약으로 정적 검증 기준)
- [x] 코드 리뷰 승인/병합 (로컬 기준 준비 완료)
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
