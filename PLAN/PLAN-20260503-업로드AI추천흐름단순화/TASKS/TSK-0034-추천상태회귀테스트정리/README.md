---
id: TSK-0034-추천상태회귀테스트정리
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-03
---

## 목적
추천 페이지에서 `uploaded_image_id`가 바뀔 때 이전 검색어/필터/분석 요약이 남지 않는지, 느린 이전 응답이 새 업로드 결과를 덮지 않는지를 회귀 테스트로 고정한다.

## 작업 내역
- [x] 기존 Playwright 핵심 흐름 테스트를 현재 UI 기준으로 정리
- [x] 업로드 전환 시 검색어/필터/분석 요약 초기화 시나리오 추가
- [x] 느린 이전 추천 응답 덮어쓰기 방지 시나리오 추가
- [x] 문서/검증 반영

## 산출물(Artifacts)
- `frontend/e2e/core-flow.spec.ts`
- `README.md`
- `TODO.md`
- `PLAN/PLAN-20260503-업로드AI추천흐름단순화/PLAN.md`
- `PLAN/PLAN-20260503-업로드AI추천흐름단순화/TASKS/TSK-0034-추천상태회귀테스트정리/*`

## 테스트/검증
- `cd frontend && npm run test:e2e -- --project=chromium`

## 의존성/리스크
- Playwright mock 응답이 현재 API 응답 구조와 맞지 않으면 UI 회귀가 아닌 테스트 자체가 깨질 수 있어, mock payload를 현재 업로드 분석 메타 기준으로 함께 유지해야 한다.

## 완료 기준(DoD)
- [x] 업로드 화면 최신 UI 기준으로 핵심 흐름 E2E가 통과함
- [x] 새 `uploaded_image_id` 전환 시 추천 상태 초기화 회귀가 고정됨
- [x] 느린 이전 응답 덮어쓰기 방지 회귀가 고정됨
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서 갱신
