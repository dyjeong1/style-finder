---
id: TSK-0001-워크플로우액션버전업데이트
plan_id: PLAN-20260415-GitHubActionsNode24대응
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-15
---

## 목적
GitHub Actions 워크플로우에서 Node 20 deprecation warning을 유발하는 액션 버전을 Node 24 호환 버전으로 갱신합니다.

## 작업 내역
- [x] 공식 릴리즈 기준 업그레이드 대상 액션 확인
- [x] 백엔드/프론트 워크플로우 액션 버전 상향
- [x] 로컬 테스트 및 문서 반영

## 산출물(Artifacts)
- `.github/workflows/backend-tests.yml`
- `.github/workflows/frontend-e2e.yml`
- PLAN/TASK 문서

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd frontend && npm run test:e2e`

## 의존성/리스크
- 액션 메이저 업그레이드에 따른 입력 파라미터 호환성 확인 필요

## 완료 기준(DoD)
- [x] 공식 릴리즈 기준으로 안전한 액션 버전 상향
- [x] 테스트 재검증
- [ ] TASK 완료 직후 커밋 완료
