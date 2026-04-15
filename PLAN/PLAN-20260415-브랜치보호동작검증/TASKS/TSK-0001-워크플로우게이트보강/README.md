---
id: TSK-0001-워크플로우게이트보강
plan_id: PLAN-20260415-브랜치보호동작검증
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-15
---

## 목적
required check가 문서-only PR에서도 누락되지 않도록 GitHub Actions 트리거 조건을 보강합니다.

## 작업 내역
- [x] 현재 브랜치 보호와 워크플로우 조건 충돌 여부 점검
- [x] required check 대상 워크플로우 트리거 보강
- [x] 로컬 검증 및 문서 반영

## 산출물(Artifacts)
- `.github/workflows/backend-tests.yml`
- `.github/workflows/frontend-e2e.yml`
- PLAN/TASK 문서

## 테스트/검증
- 워크플로우 YAML 구조 검토
- 기존 로컬 백엔드/프론트 테스트 재실행
  - `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 통과
  - `cd frontend && npm run test:e2e` 통과

## 의존성/리스크
- 모든 PR에서 테스트가 실행되어 CI 비용이 증가할 수 있음

## 완료 기준(DoD)
- [x] docs-only PR에서도 required check 상태가 생성되도록 설정
- [x] 관련 문서 갱신
- [ ] TASK 완료 직후 커밋 완료
