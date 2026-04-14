# GitHub 브랜치 보호 적용 가이드

## 목적
- `main` 브랜치에 보호 규칙을 적용하고, 백엔드/프론트 테스트를 필수 체크로 연결합니다.
- 현재 저장소는 solo 운영 기준으로 `승인 0개 + required check 유지` 정책을 사용합니다.

## 필수 체크 이름
- `Backend Tests / test`
- `Frontend E2E / e2e`

## 준비물
- GitHub 원격 저장소 slug 예: `owner/repo`
- 브랜치 보호 변경 권한이 있는 `GITHUB_TOKEN` 또는 `GH_TOKEN`

## 적용 파일
- 정책 파일: `.github/branch-protection/main.json`
- 적용 스크립트: `scripts/apply-branch-protection.sh`

## 적용 명령
```bash
export GITHUB_TOKEN=<your-token>
scripts/apply-branch-protection.sh owner/repo main
```

## 현재 정책 요약
- required check:
  - `Backend Tests / test`
  - `Frontend E2E / e2e`
- direct push: 차단
- linear history: 활성화
- required conversation resolution: 활성화
- required approving review count: `0`

## solo 운영 적용 메모
- 자기 PR은 스스로 승인할 수 없으므로, 단독 운영 저장소에서는 승인 수를 `0`으로 두는 것이 현실적입니다.
- 대신 required check 2종과 대화 해결 조건은 유지해 품질 게이트를 확보합니다.
- 협업 저장소로 전환되면 `required_approving_review_count`를 다시 `1` 이상으로 올리는 것을 권장합니다.

## 적용 후 확인할 항목
- `main` 브랜치 direct push 제한 여부
- PR 기준 required check 2종 연결 여부
- 실패한 워크플로우에서 merge 차단 여부
- 승인 없이도 PR merge 버튼이 활성화되는지 여부
