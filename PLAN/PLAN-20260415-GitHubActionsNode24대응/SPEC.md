---
id: SPEC-PLAN-20260415-GitHubActionsNode24대응
title: GitHub Actions Node 24 대응 스펙
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  plan: [PLAN-20260415-GitHubActionsNode24대응]
  tasks: [TSK-0001-워크플로우액션버전업데이트]
tags: [github-actions, node24]
---

## 1. 목적
GitHub Actions 러너의 Node 20 deprecation 경고를 해소하기 위해 사용 중인 액션 버전을 Node 24 호환 버전으로 올립니다.

## 2. 기능 스펙
- `backend-tests.yml`, `frontend-e2e.yml`의 공통 액션 버전 검토
- Node 24 호환 릴리즈로 상향
- 기존 테스트 명령 유지

## 3. 비기능 스펙
- required check 이름 유지
- GitHub-hosted runner에서 그대로 동작해야 함

## 4. 구현 스펙
- 대상 파일:
  - `.github/workflows/backend-tests.yml`
  - `.github/workflows/frontend-e2e.yml`
  - PLAN/TASK 문서

## 5. 수용 기준
- [x] Node 24 호환 액션 버전으로 갱신
- [x] 로컬 테스트 통과
