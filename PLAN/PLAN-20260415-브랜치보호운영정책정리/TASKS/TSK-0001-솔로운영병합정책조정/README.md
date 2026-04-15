---
id: TSK-0001-솔로운영병합정책조정
plan_id: PLAN-20260415-브랜치보호운영정책정리
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-15
---

## 목적
혼자 운영하는 저장소에서도 PR 기반 머지가 가능하도록 브랜치 보호 정책을 조정합니다.

## 작업 내역
- [x] 현재 브랜치 보호 병목 확인
- [x] 승인 수 정책 조정
- [x] 운영 문서 및 루트 문서 반영

## 산출물(Artifacts)
- `.github/branch-protection/main.json`
- `docs/github-branch-protection.md`
- PLAN/TASK 문서

## 테스트/검증
- 정책 JSON 구조 확인
- 변경 후 적용 명령 재정리

## 의존성/리스크
- 실제 GitHub 반영에는 관리자 권한 토큰 필요

## 완료 기준(DoD)
- [x] 솔로 운영 기준 정책 반영
- [x] 운영 문서 반영
- [ ] TASK 완료 직후 커밋 완료
