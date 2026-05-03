---
id: TSK-0041-프로덕션스타트회귀검증경로추가
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
dev 서버에서 통과하던 추천 회귀 테스트를 `next build + next start` 기반 production-start 경로에서도 재사용할 수 있게 해, 실제 사용자 실행 방식과 테스트 환경 사이의 틈을 줄인다.

## 작업 내역
- [x] Playwright webServer를 dev/local 모드로 전환할 수 있게 설정 확장
- [x] `npm run test:e2e:local` 스크립트 추가
- [x] production-start 경로에서 핵심 추천 회귀 테스트 실행
- [x] E2E mock API base를 `127.0.0.1:8000` 기준으로 정리
- [x] README/TODO/PLAN/TASK 문서 갱신
- [ ] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/package.json`
- `frontend/playwright.config.ts`
- `frontend/e2e/core-flow.spec.ts`
- `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run test:e2e:local -- --project=chromium -g "추천 페이지는 uploaded_image_id가 바뀌면 이전 검색어와 필터, 분석 요약을 초기화한다"`

## 의존성/리스크
- `npm run local`은 build를 포함하므로 dev 모드보다 테스트 시작 시간이 더 길다.
- 기존 3000 포트 서버가 떠 있으면 `reuseExistingServer` 설정에 따라 그 서버를 재사용할 수 있다.

## 결과 요약
- Playwright는 이제 기본 dev 서버뿐 아니라 `next build + next start` 기반 local 모드에서도 같은 테스트 세트를 실행할 수 있다.
- `frontend/e2e/core-flow.spec.ts`의 mock API base도 실제 프론트 기본값과 맞춰 `http://127.0.0.1:8000`으로 정리했다.
- local 모드에서 `추천 페이지는 uploaded_image_id가 바뀌면 이전 검색어와 필터, 분석 요약을 초기화한다` 테스트가 실제로 통과했다.

## 완료 기준(DoD)
- [x] production-start 경로에서도 Playwright를 실행할 수 있다.
- [x] 핵심 추천 회귀 테스트가 local 모드에서 확인된다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
