---
id: TSK-0002-원격브랜치보호적용
plan_id: PLAN-20260414-브랜치보호및필수체크연동
owner: codex
status: blocked
estimate: 0.5d
updated_at: 2026-04-14
---

## 목적
원격 GitHub 저장소의 `main` 브랜치에 보호 규칙과 필수 체크를 적용합니다.

## 작업 내역
- [ ] 원격 저장소 slug 확인
- [ ] GitHub 인증 토큰 또는 `gh` 환경 확인
- [ ] 보호 규칙 실제 적용

## 의존성/리스크
- 현재 blocker:
  - 로컬 저장소에 `git remote`가 없음
  - `gh` 명령이 설치되어 있지 않음
  - GitHub 인증 정보가 없음

## 완료 기준(DoD)
- [ ] 원격 저장소 `main` 브랜치에 보호 규칙 적용 완료
- [ ] required check 연결 확인
