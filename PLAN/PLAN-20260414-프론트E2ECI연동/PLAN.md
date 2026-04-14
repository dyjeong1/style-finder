---
id: PLAN-20260414-프론트E2ECI연동
title: 프론트 E2E CI 연동
status: done
priority: P1
created_at: 2026-04-14
updated_at: 2026-04-14
related:
  tasks: [TSK-0001-Playwright워크플로우추가]
tags: [frontend, ci, e2e, playwright, github-actions]
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 프론트 Playwright E2E가 로컬에서 준비되어, 이제 변경 시 자동 검증이 가능해야 합니다.
- 현재 성능/운영 이슈: 브라우저 E2E가 CI에 연결되지 않아 회귀를 수동으로만 확인하고 있습니다.

## 2. 목표/가설
- 1차 지표(Primary): 프론트 변경 시 Playwright E2E가 GitHub Actions에서 자동 실행
- 2차 지표(Secondary): 실패 시 보고서와 테스트 아티팩트를 확인 가능
- 가설: CI 연동으로 프론트 회귀를 조기에 감지할 수 있습니다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - 프론트 E2E GitHub Actions 워크플로우 추가
  - Playwright 리포트/테스트 아티팩트 업로드
  - 실행 문서 갱신
- 제외 범위:
  - 브랜치 보호 규칙 직접 설정
  - 외부 서비스 배포 연동

## 4. 일정/마일스톤
- M1(워크플로우 정의): 2026-04-14
- M2(로컬/구성 검증): 2026-04-14
- M3(문서 최신화): 2026-04-14

## 5. 리스크 & 가정
- 시스템/리소스 제약: Playwright 브라우저 설치 시간이 CI에서 추가됩니다.
- 테스트 가정: 현재 E2E는 API mock 기반으로 브라우저에서 안정적으로 재현됩니다.

## 6. 검증/수용 기준(DoD)
- [x] 프론트 CI 워크플로우가 추가됨
- [x] Playwright 테스트 실행/아티팩트 업로드 단계가 정의됨
- [x] README/TODO/PLAN/TASK 문서 최신화

## 7. 변경 이력
- 2026-04-14: PLAN 생성
- 2026-04-14: TSK-0001 Playwright CI 워크플로우 추가 및 로컬 검증 완료
