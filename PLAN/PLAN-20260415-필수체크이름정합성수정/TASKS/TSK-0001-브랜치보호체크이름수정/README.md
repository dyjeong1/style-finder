---
id: TSK-0001-브랜치보호체크이름수정
plan_id: PLAN-20260415-필수체크이름정합성수정
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-15
---

## 목적
PR 성공 체크와 브랜치 보호 required check 이름을 일치시켜 머지 대기 상태를 해소합니다.

## 작업 내역
- [x] 현재 pending required check 이름 분석
- [x] 정책 파일 exact check name 수정
- [x] 운영 문서 반영

## 산출물(Artifacts)
- `.github/branch-protection/main.json`
- `docs/github-branch-protection.md`
- PLAN/TASK 문서

## 테스트/검증
- PR 화면의 성공 체크 이름 기준 정합성 검토
- 재적용 명령 문서화

## 의존성/리스크
- 실제 해소 확인을 위해 GitHub 브랜치 보호 재적용 필요

## 완료 기준(DoD)
- [x] required check 이름 정합성 수정
- [x] 운영 문서 반영
- [ ] TASK 완료 직후 커밋 완료
