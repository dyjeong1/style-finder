---
id: TSK-0001-글로벌폰트단위pt정리
plan_id: PLAN-20260420-프론트폰트단위pt전환
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
프론트 전역 폰트 단위를 `pt` 기준으로 맞추고 업로드 타이틀을 `36pt`로 조정한다.

## 작업 내역
- [x] 전역 `font-size` 선언을 `pt` 단위로 정리
- [x] 업로드 타이틀 `36pt` 반영
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 단위 전환으로 인해 일부 화면의 시각 균형이 달라질 수 있어 빌드 후 실제 페이지 확인이 필요하다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
