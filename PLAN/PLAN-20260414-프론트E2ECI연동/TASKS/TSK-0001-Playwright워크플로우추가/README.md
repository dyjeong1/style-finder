---
id: TSK-0001-Playwright워크플로우추가
plan_id: PLAN-20260414-프론트E2ECI연동
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-14
---

## 목적
프론트 Playwright E2E를 GitHub Actions에 연결합니다.

## 작업 내역
- [x] 워크플로우 YAML 추가
- [x] Playwright 브라우저 설치/실행 단계 반영
- [x] 아티팩트 업로드 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `.github/workflows/frontend-e2e.yml`
  - `README.md`
  - `TODO.md`

## 테스트/검증
- `cd frontend && npm run test:e2e` 성공

## 완료 기준(DoD)
- [x] 워크플로우 파일 추가
- [x] 테스트 실행 단계 및 아티팩트 업로드 정의
- [x] README/TODO/PLAN/TASK 갱신
