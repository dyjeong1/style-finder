---
id: TSK-0001-안정실행스크립트추가
plan_id: PLAN-20260420-프론트로컬실행안정화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
로컬에서 프론트를 확인할 때 `next dev`의 캐시/HMR 오류를 피하고, 항상 안정적인 방식으로 앱을 실행할 수 있게 한다.

## 작업 내역
- [x] `frontend/package.json`에 안정 실행 스크립트 추가
- [x] 프론트/루트 README 실행 안내 갱신
- [x] 루트 TODO 및 PLAN/TASK 문서 반영
- [x] `build` 후 핵심 페이지 응답 검증

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/package.json`
- 문서/노트북: `README.md`, `frontend/README.md`, `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`
- `cd frontend && npm run local`
- `/upload`, `/recommendations`, `/wishlist` 200 응답 확인

## 의존성/리스크
- 로컬 Node/npm 환경이 준비되어 있어야 한다.
- 백엔드가 필요한 기능은 별도 서버가 켜져 있어야 한다.

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과
- [x] 코드 리뷰 승인/병합
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
