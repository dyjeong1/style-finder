---
id: TSK-0003-업로드안내문구조정
plan_id: PLAN-20260420-업로드영역통합UX개선
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-04-20
---

## 목적
업로드 안내 문구를 더 자연스러운 표현으로 다듬어 첫 화면 톤을 정리한다.

## 작업 내역
- [x] 업로드 안내 문구를 요청 문안으로 교체
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`
- 문서/노트북: `README.md`, `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 문구만 변경하며 레이아웃과 동작은 유지한다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
