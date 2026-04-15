---
id: TSK-0003-프론트E2E목응답동기화
plan_id: PLAN-20260415-업로드이미지분석고도화
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-15
---

## 목적
Playwright E2E의 mock API 응답을 최신 업로드/추천 스키마에 맞춰 동기화합니다.

## 작업 내역
- [x] 실패 원인 확인
- [x] mock 응답 필드 보강
- [x] `npm run test:e2e` 재검증 및 문서 반영

## 산출물(Artifacts)
- `frontend/e2e/core-flow.spec.ts`
- PLAN/TASK 문서

## 테스트/검증
- `cd frontend && npm run test:e2e`

## 의존성/리스크
- E2E는 프론트 API mock 구조 변경 시 지속적으로 동기화가 필요합니다.

## 완료 기준(DoD)
- [x] 최신 API 스키마 기반 mock 응답 반영
- [x] E2E 통과
- [ ] TASK 완료 직후 커밋 완료
