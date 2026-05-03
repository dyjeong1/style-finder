---
id: TSK-0043-로컬스모크CI연결
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
로컬에서만 확인하던 `next build + next start` 기반 smoke 회귀를 GitHub Actions에도 연결해, 업로드 후 추천 이동과 `uploaded_image_id` 동기화 문제를 PR 단계에서 다시 잡을 수 있게 한다.

## 작업 내역
- [x] `Frontend E2E` 워크플로우에 local smoke job 추가
- [x] smoke job 아티팩트 이름 분리
- [x] 문서/README/TODO/PLAN/TASK 갱신
- [ ] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `.github/workflows/frontend-e2e.yml`
- `frontend/README.md`
- `README.md`
- `TODO.md`

## 테스트/검증
- 기존 local smoke 명령: `cd frontend && npm run test:e2e:local:smoke -- --project=chromium`
- CI에서는 `Frontend E2E / e2e-local-smoke` job으로 동일 시나리오 실행

## 의존성/리스크
- 기존 required check `Frontend E2E / e2e`는 유지하고, local smoke는 보강용 추가 job으로 연결한다.
- 워크플로우 실행 시간은 증가하지만, smoke 범위만 돌기 때문에 전체 full E2E보다 비교적 짧다.

## 결과 요약
- GitHub Actions `Frontend E2E` 워크플로우에 `e2e-local-smoke` job을 추가했다.
- 새 job은 `npm run test:e2e:local:smoke -- --project=chromium`를 사용해 `next build + next start` 기준 smoke 회귀를 실행한다.
- 기존 `e2e` job 이름은 그대로 유지해 현재 required check 정합성을 깨지 않도록 했다.

## 완료 기준(DoD)
- [x] CI에서 local smoke 회귀를 별도 job으로 실행한다.
- [x] 기존 dev 기반 E2E 체크 이름을 깨지 않는다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
