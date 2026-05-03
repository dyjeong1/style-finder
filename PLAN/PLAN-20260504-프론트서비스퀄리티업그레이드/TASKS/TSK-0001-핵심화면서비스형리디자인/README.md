---
id: TSK-0001-핵심화면서비스형리디자인
plan_id: PLAN-20260504-프론트서비스퀄리티업그레이드
owner: Codex
status: done
estimate: 1d
updated_at: 2026-05-04
---

## 목적
업로드, 추천, 위시리스트 핵심 화면을 실제 서비스 중인 스타일 커머스처럼 보이도록 전역 스타일과 정보 구조를 함께 재설계합니다.

## 작업 내역
- [x] 공통 앱 셸과 전역 스타일 시스템 재정비
- [x] 업로드 화면을 포스터형 진입 구조로 재디자인
- [x] 추천 화면을 큐레이션형 탐색 구조로 재디자인
- [x] 위시리스트 화면을 저장 컬렉션 보드형으로 재디자인
- [x] 빌드 검증 및 문서 반영

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/components/app-shell.tsx`
  - `frontend/app/globals.css`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/(main)/wishlist/page.tsx`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`
  - `PLAN/PLAN-20260504-프론트서비스퀄리티업그레이드/PLAN.md`
  - `PLAN/PLAN-20260504-프론트서비스퀄리티업그레이드/SPEC.md`

## 테스트/검증
- `cd frontend && npm run build`
- 확인 메모: Playwright 기반 스크린샷으로 실제 브라우저 시각 검증까지 시도했으나, 현재 실행 환경의 headless Chromium 권한 제한으로 캡처는 실패했습니다.

## 의존성/리스크
- 스타일 변경 폭이 넓어 모바일 레이아웃과 긴 상품명 줄바꿈 확인이 필요합니다.
- 실제 상품 이미지 품질 편차가 커도 카드 구조가 무너지지 않아야 합니다.

## 완료 기준(DoD)
- [x] 핵심 3개 화면 서비스형 리디자인 반영
- [x] 프론트 빌드 통과
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 갱신
