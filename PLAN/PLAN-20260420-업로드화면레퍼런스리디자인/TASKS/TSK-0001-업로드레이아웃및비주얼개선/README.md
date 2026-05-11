---
id: TSK-0001-업로드레이아웃및비주얼개선
plan_id: PLAN-20260420-업로드화면레퍼런스리디자인
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
업로드 페이지의 첫인상을 레퍼런스에 가깝게 개선하고, 업로드 행동과 최근 이력의 가독성을 높인다.

## 작업 내역
- [x] 업로드 페이지 레이아웃 재구성
- [x] 인트로 패널/드롭존/최근 업로드 카드 스타일 개선
- [x] 문서 및 루트 TODO 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `frontend/README.md`, `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 최근 업로드 수가 많아도 카드 높이가 과도하게 깨지지 않도록 주의한다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
