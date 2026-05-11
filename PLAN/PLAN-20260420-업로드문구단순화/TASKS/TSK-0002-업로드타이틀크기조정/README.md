---
id: TSK-0002-업로드타이틀크기조정
plan_id: PLAN-20260420-업로드문구단순화
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-20
---

## 목적
업로드 화면 메인 타이틀의 시각적 비중을 낮춰 전체 레이아웃 균형을 맞춘다.

## 작업 내역
- [x] 업로드 타이틀 폰트 크기 조정
- [x] 모바일 타이틀 크기 함께 조정
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 타이틀 크기만 줄이고 업로드 레이아웃 구조는 유지한다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
