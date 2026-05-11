---
id: TSK-0042-업로드추천스모크경로정리
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
업로드 후 추천 이동과 `uploaded_image_id` 상태 동기화처럼 가장 자주 깨질 수 있는 핵심 흐름을 별도 smoke 경로로 묶어, dev/local 양쪽에서 빠르게 재검증할 수 있게 한다.

## 작업 내역
- [x] 핵심 E2E 시나리오에 `@smoke` 태그 부여
- [x] `npm run test:e2e:smoke`, `npm run test:e2e:local:smoke` 스크립트 추가
- [x] local smoke 경로 실행 검증
- [x] README/TODO/PLAN/TASK 문서 갱신
- [ ] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/e2e/core-flow.spec.ts`
- `frontend/package.json`
- `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run test:e2e:local:smoke -- --project=chromium`

## 의존성/리스크
- smoke 태그 범위를 너무 넓히면 빠른 재검증 목적이 약해질 수 있어, 현재는 업로드 핵심 흐름과 URL 동기화 회귀만 포함한다.

## 결과 요약
- `@smoke` 태그로 업로드 핵심 흐름과 `uploaded_image_id` 동기화 회귀를 분리해 빠른 재검증 세트로 묶었다.
- `npm run test:e2e:smoke`는 dev 서버 기준, `npm run test:e2e:local:smoke`는 `next build + next start` 기준으로 같은 핵심 회귀를 확인할 수 있다.
- local smoke 실행 결과 2개 시나리오가 모두 통과했다.

## 완료 기준(DoD)
- [x] smoke 태그로 핵심 업로드/추천 흐름을 빠르게 실행할 수 있다.
- [x] local smoke 경로가 실제로 통과한다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
