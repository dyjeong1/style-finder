# GitHub 브랜치 보호 적용 가이드

## 목적
- `main` 브랜치에 보호 규칙을 적용하고, 백엔드/프론트 테스트를 필수 체크로 연결합니다.

## 필수 체크 이름
- `Backend Tests / test`
- `Frontend E2E / e2e`

## 준비물
- GitHub 원격 저장소 slug 예: `owner/repo`
- `repo` 권한이 있는 `GITHUB_TOKEN` 또는 `GH_TOKEN`

## 적용 파일
- 정책 파일: `.github/branch-protection/main.json`
- 적용 스크립트: `scripts/apply-branch-protection.sh`

## 적용 명령
```bash
export GITHUB_TOKEN=<your-token>
scripts/apply-branch-protection.sh owner/repo main
```

## 현재 blocker
- 로컬 저장소에 `git remote`가 없습니다.
- `gh` CLI가 설치되어 있지 않습니다.
- 원격 저장소 slug와 인증 토큰이 확인되지 않았습니다.

## 적용 후 확인할 항목
- `main` 브랜치 direct push 제한 여부
- PR 기준 required check 2종 연결 여부
- 실패한 워크플로우에서 merge 차단 여부
