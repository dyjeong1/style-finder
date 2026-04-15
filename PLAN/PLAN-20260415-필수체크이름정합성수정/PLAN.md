---
id: PLAN-20260415-필수체크이름정합성수정
title: 필수 체크 이름 정합성 수정
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  tasks: [TSK-0001-브랜치보호체크이름수정]
tags: [github, branch-protection, required-check]
---

## 1. 배경/문제 정의
- 비즈니스 맥락: PR의 백엔드/프론트 체크는 모두 성공했지만, 브랜치 보호 화면에서는 required check 2개가 계속 `Expected` 상태로 남아 있습니다.
- 현재 성능/운영 이슈: 브랜치 보호 정책이 기대하는 체크 이름과 GitHub Actions가 실제 보고하는 체크 이름 사이에 정합성 차이가 있어 머지가 차단됩니다.

## 2. 목표/가설
- 1차 지표(Primary): 브랜치 보호 정책의 required check 이름을 실제 PR 체크 이름과 일치시킴
- 2차 지표(Secondary): PR에서 더 이상 `Expected — Waiting for status to be reported`가 남지 않게 함
- 가설: `pull_request` 기준의 실제 체크 이름으로 정책을 재설정하면 pending required check가 해소됩니다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - 브랜치 보호 정책 JSON 수정
  - 운영 가이드와 루트 문서 갱신
  - 재적용 절차 문서화
- 제외 범위:
  - 워크플로우 로직 자체 변경
  - 신규 테스트 추가

## 4. 일정/마일스톤
- M1(PLAN 작성): 2026-04-15
- M2(정책 수정): 2026-04-15
- M3(문서 정리): 2026-04-15

## 5. 리스크 & 가정
- 시스템/리소스 제약: 정책 재적용 후 PR 페이지 새로고침 또는 체크 재실행이 필요할 수 있습니다.
- 운영 가정: 머지 게이트에는 `pull_request` 기준 체크만 요구하면 충분합니다.

## 6. 검증/수용 기준(DoD)
- [x] 정책 파일이 실제 PR 체크 이름 기준으로 수정됨
- [x] 문서/README/TODO가 최신화됨
- [x] 재적용 절차가 정리됨

## 7. 변경 이력
- 2026-04-15: PLAN 생성
- 2026-04-15: required check 이름을 `pull_request` exact name 기준으로 조정
