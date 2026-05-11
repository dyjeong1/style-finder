---
id: TSK-0001-프리텐다드및핵심화면리디자인
plan_id: PLAN-20260417-프론트비주얼리프레시
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
Pretendard를 적용하고 업로드/추천/위시리스트 핵심 화면의 헤더, 카드, 배경 위계를 정리해 더 서비스다운 인상을 만듭니다.

## 작업 내역
- [x] Pretendard 전역 적용
- [x] 공통 레이아웃/네비게이션 스타일 개선
- [x] 업로드/추천/위시리스트 화면 리디자인
- [x] 빌드 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/layout.tsx`
  - `frontend/app/globals.css`
  - `frontend/components/app-shell.tsx`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/(main)/wishlist/page.tsx`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`
  - `PLAN/PLAN-20260417-프론트비주얼리프레시/PLAN.md`
  - `PLAN/PLAN-20260417-프론트비주얼리프레시/SPEC.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 외부 CDN 기반 Pretendard를 사용하므로 네트워크 차단 환경에서는 시스템 폴백 글꼴로 내려갑니다.
- 시각 변화 폭이 있어 모바일 레이아웃을 함께 점검했습니다.

## 완료 기준(DoD)
- [x] Pretendard와 시각 리프레시 반영
- [x] 프론트 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서 갱신
