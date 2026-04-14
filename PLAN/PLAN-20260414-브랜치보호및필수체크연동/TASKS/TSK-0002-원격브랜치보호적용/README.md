---
id: TSK-0002-원격브랜치보호적용
plan_id: PLAN-20260414-브랜치보호및필수체크연동
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-15
---

## 목적
원격 GitHub 저장소의 `main` 브랜치에 보호 규칙과 필수 체크를 적용합니다.

## 작업 내역
- [x] 원격 저장소 slug 확인
- [x] GitHub 인증 토큰 또는 `gh` 환경 확인
- [x] 보호 규칙 실제 적용

## 의존성/리스크
- 적용 조건:
  - GitHub 원격 저장소 `dyjeong1/style-finder` 연결
  - 브랜치 보호 API 호출 권한이 있는 토큰 준비

## 산출물(Artifacts)
- 적용 대상:
  - 원격 저장소 `dyjeong1/style-finder`
  - 브랜치 `main`
- 보호 규칙:
  - required check `Backend Tests / test`
  - required check `Frontend E2E / e2e`

## 완료 기준(DoD)
- [x] 원격 저장소 `main` 브랜치에 보호 규칙 적용 완료
- [x] required check 연결 확인
