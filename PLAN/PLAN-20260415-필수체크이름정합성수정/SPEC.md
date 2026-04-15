---
id: SPEC-PLAN-20260415-필수체크이름정합성수정
title: 필수 체크 이름 정합성 수정 스펙
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  plan: [PLAN-20260415-필수체크이름정합성수정]
  tasks: [TSK-0001-브랜치보호체크이름수정]
tags: [github, required-check]
---

## 1. 목적
브랜치 보호 정책이 기다리는 required check 이름을 실제 `pull_request` 체크 이름과 일치시킵니다.

## 2. 기능 스펙
- `.github/branch-protection/main.json`의 required check context 수정
- `docs/github-branch-protection.md`에 exact check name 기준 반영
- README/TODO와 PLAN/TASK 문서 동기화

## 3. 비기능 스펙
- solo 운영 기준 리뷰 수 `0` 유지
- direct push 차단과 linear history 유지

## 4. 구현 스펙
- 대상 파일:
  - `.github/branch-protection/main.json`
  - `docs/github-branch-protection.md`
  - PLAN/TASK 문서

## 5. 수용 기준
- [x] exact check name 기준 정책 반영
- [x] 재적용 절차 문서화
