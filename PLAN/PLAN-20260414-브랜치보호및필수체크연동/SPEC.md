---
id: SPEC-PLAN-20260414-브랜치보호및필수체크연동
title: 브랜치 보호 및 필수 체크 연동 스펙
status: review
priority: P1
created_at: 2026-04-14
updated_at: 2026-04-14
related:
  plan: [PLAN-20260414-브랜치보호및필수체크연동]
  tasks: [TSK-0001-보호정책스크립트준비, TSK-0002-원격브랜치보호적용]
tags: [github, protection, required-check]
---

## 1. 목적
메인 브랜치 보호 규칙과 필수 체크 구성을 저장소에 선언적으로 남기고, 원격 연결 후 즉시 적용 가능하게 준비합니다.

## 2. 기능 스펙
- 브랜치 보호 정책 JSON 작성
- GitHub API 호출 스크립트 작성
- 적용 방법/필수 체크 이름 문서화

## 3. 비기능 스펙
- 정책은 재실행 가능해야 함
- 원격 저장소와 토큰만 있으면 동일하게 적용 가능해야 함

## 4. 구현 스펙
- 정책 파일: `.github/branch-protection/main.json`
- 스크립트: `scripts/apply-branch-protection.sh`
- 문서: `docs/github-branch-protection.md`

## 5. 수용 기준
- [x] 보호 정책 파일 추가
- [x] 적용 스크립트 추가
- [x] blocker 및 후속 절차 문서화
