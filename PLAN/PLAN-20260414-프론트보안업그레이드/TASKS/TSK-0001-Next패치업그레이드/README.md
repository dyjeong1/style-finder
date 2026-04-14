---
id: TSK-0001-Next패치업그레이드
plan_id: PLAN-20260414-프론트보안업그레이드
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-14
---

## 목적
보안 권고에 맞춰 Next.js를 취약점이 해소되는 최소 안전 버전으로 업그레이드합니다.

## 작업 내역
- [x] Next.js 권고 패치 버전 확인
- [x] 패키지/lockfile 업데이트
- [x] 설치/빌드/감사 검증

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/package.json`
  - `frontend/package-lock.json`
  - `frontend/next-env.d.ts`

## 테스트/검증
- `cd frontend && npm install` 성공
- `cd frontend && npm run build` 성공
- `cd frontend && npm audit` 성공 (`0 vulnerabilities`)

## 완료 기준(DoD)
- [x] 보안 패치 버전 반영
- [x] 빌드 통과
- [x] README/TODO/PLAN/TASK 갱신
