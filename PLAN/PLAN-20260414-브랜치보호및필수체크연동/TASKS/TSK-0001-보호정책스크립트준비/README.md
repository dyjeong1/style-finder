---
id: TSK-0001-보호정책스크립트준비
plan_id: PLAN-20260414-브랜치보호및필수체크연동
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-14
---

## 목적
브랜치 보호 정책 파일, 적용 스크립트, 운영 문서를 작성합니다.

## 작업 내역
- [x] 보호 정책 JSON 작성
- [x] 적용 스크립트 작성
- [x] 적용 절차 문서화

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `.github/branch-protection/main.json`
  - `scripts/apply-branch-protection.sh`
  - `docs/github-branch-protection.md`

## 테스트/검증
- 정적 검증:
  - 정책 JSON에 required check 2종 정의 확인
  - 스크립트 인자/토큰/파일 검증 로직 확인
  - 원격 적용 blocker 문서화 확인
  - `bash -n scripts/apply-branch-protection.sh` 통과
  - `node` 기반 JSON 파싱 검증 통과

## 완료 기준(DoD)
- [x] 보호 정책 JSON 작성
- [x] 적용 스크립트 작성
- [x] README/TODO/PLAN/TASK 갱신
