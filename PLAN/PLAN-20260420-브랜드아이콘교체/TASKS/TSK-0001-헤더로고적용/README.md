---
id: TSK-0001-헤더로고적용
plan_id: PLAN-20260420-브랜드아이콘교체
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-20
---

## 목적
좌측 상단 브랜드 마크를 실제 로고 이미지로 교체해 서비스 아이덴티티를 강화한다.

## 작업 내역
- [x] 로고 이미지 정적 자산 경로 추가
- [x] 헤더 브랜드 마크를 이미지 로고로 교체
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/components/app-shell.tsx`, `frontend/app/globals.css`, `frontend/public/brand/stylefinder_logo.png`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 로고 비율이 헤더 영역과 맞지 않으면 CSS에서 미세 조정이 필요하다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
