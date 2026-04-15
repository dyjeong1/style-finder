---
id: PLAN-20260415-GitHubActionsNode24대응
title: GitHub Actions Node 24 대응
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  tasks: [TSK-0001-워크플로우액션버전업데이트]
tags: [github-actions, node24, maintenance, ci]
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 현재 CI는 정상 동작하지만, GitHub Actions 러너에서 Node.js 20 기반 액션이 곧 기본 지원 대상에서 제외될 예정입니다.
- 현재 성능/운영 이슈: `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4` 등 구버전 액션 사용으로 deprecation warning이 발생하고 있습니다.

## 2. 목표/가설
- 1차 지표(Primary): CI 워크플로우에서 Node 24 호환 액션 버전 사용
- 2차 지표(Secondary): 기존 테스트 동작과 required check 이름 유지
- 가설: 액션 메이저 버전을 Node 24 호환 릴리즈로 갱신하면 경고를 줄이면서 기존 CI 흐름을 유지할 수 있습니다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - GitHub Actions 워크플로우 액션 버전 상향
  - 관련 PLAN/TASK 및 루트 문서 갱신
  - 로컬 테스트 재검증
- 제외 범위:
  - 테스트 로직 자체 변경
  - 배포 파이프라인 추가

## 4. 일정/마일스톤
- M1(PLAN 작성): 2026-04-15
- M2(액션 버전 상향): 2026-04-15
- M3(검증 및 문서화): 2026-04-15

## 5. 리스크 & 가정
- 시스템/리소스 제약: 액션 메이저 업그레이드 시 입력 파라미터/기본값 차이가 있을 수 있습니다.
- 운영 가정: required check 이름은 유지되어야 하므로 workflow `name`과 job ID는 변경하지 않습니다.

## 6. 검증/수용 기준(DoD)
- [x] 워크플로우 액션 버전이 Node 24 호환 릴리즈로 갱신됨
- [x] 로컬 테스트 재검증 완료
- [x] 문서/PLAN/TASK/README/TODO 갱신

## 7. 변경 이력
- 2026-04-15: PLAN 생성
- 2026-04-15: `checkout/setup-python/setup-node/upload-artifact` 액션 버전 상향 및 로컬 테스트 재검증 완료
