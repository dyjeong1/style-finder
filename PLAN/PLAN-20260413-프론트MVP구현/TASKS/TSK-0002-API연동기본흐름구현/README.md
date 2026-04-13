---
id: TSK-0002-API연동기본흐름구현
plan_id: PLAN-20260413-프론트MVP구현
owner: codex
status: done
estimate: 1d
updated_at: 2026-04-13
---

## 목적
프론트에서 백엔드 API를 호출하는 기본 흐름을 구현합니다.

## 작업 내역
- [x] 로그인 API 연동
- [x] 업로드/추천 API 연동
- [x] 찜 CRUD API 연동

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/lib/api.ts`
  - `frontend/app/(auth)/login/page.tsx`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/(main)/wishlist/page.tsx`
  - `frontend/app/globals.css`

## 테스트/검증
- 정적 검증:
  - API 경로/파라미터가 백엔드 라우터(`backend/src/api/routes/*`)와 일치하는지 확인
  - 로그인 토큰 저장(localStorage) → 업로드 ID 저장 → 추천 조회/찜 CRUD 흐름 코드 점검
- 실행 검증:
  - Node/npm 미설치 환경으로 `npm run dev` 실행 검증은 미수행

## 완료 기준(DoD)
- [x] 로그인/업로드/추천/찜 API 호출 흐름이 구현됨
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서 갱신
