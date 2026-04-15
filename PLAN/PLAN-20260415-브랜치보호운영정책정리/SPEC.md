---
id: SPEC-PLAN-20260415-브랜치보호운영정책정리
title: 브랜치 보호 운영 정책 정리 스펙
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  plan: [PLAN-20260415-브랜치보호운영정책정리]
  tasks: [TSK-0001-솔로운영병합정책조정]
tags: [github, branch-protection]
---

## 1. 목적
단독 운영 저장소에 맞게 브랜치 보호 정책을 조정해 PR 머지 블로커를 제거합니다.

## 2. 기능 스펙
- `.github/branch-protection/main.json`의 리뷰 승인 수 조정
- `docs/github-branch-protection.md`에 solo 운영 기준 반영
- README/TODO와 PLAN/TASK 문서 동기화

## 3. 비기능 스펙
- required check 이름은 유지
- direct push 차단, 선형 히스토리 유지

## 4. 구현 스펙
- 대상 파일:
  - `.github/branch-protection/main.json`
  - `docs/github-branch-protection.md`
  - PLAN/TASK 문서

## 5. 수용 기준
- [x] solo 운영 기준 정책 반영
- [x] 문서 갱신 완료
