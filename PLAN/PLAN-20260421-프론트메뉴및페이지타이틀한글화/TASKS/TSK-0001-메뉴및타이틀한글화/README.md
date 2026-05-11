---
id: TSK-0001-메뉴및타이틀한글화
plan_id: PLAN-20260421-프론트메뉴및페이지타이틀한글화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-21
---

## 목적
상단 메뉴와 페이지 대표 타이틀, 자주 보이는 상단 라벨을 한글로 통일해 프론트 경험을 자연스럽게 만든다.

## 작업 내역
- [x] 상단 메뉴 라벨 한글화
- [x] 업로드/추천/위시리스트 대표 타이틀 한글화
- [x] 브라우저 탭 제목 한국어화
- [x] 상단 요약/필터/주요 버튼 문구 한글화

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/components/app-shell.tsx`, `frontend/app/layout.tsx`, `frontend/app/(main)/*/page.tsx`
- 문서/노트북: `PLAN/PLAN-20260421-프론트메뉴및페이지타이틀한글화/*`

## 테스트/검증
- `cd frontend && npm run build`
- `/upload`, `/recommendations`, `/wishlist` 수동 확인

## 의존성/리스크
- 선행 TASK/시스템/권한: 없음

## 완료 기준(DoD)
- [ ] 유닛/통합 테스트 통과
- [ ] 코드 리뷰 승인/병합
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [ ] README/TODO 갱신
