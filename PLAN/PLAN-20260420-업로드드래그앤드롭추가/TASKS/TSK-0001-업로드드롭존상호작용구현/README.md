---
id: TSK-0001-업로드드롭존상호작용구현
plan_id: PLAN-20260420-업로드드래그앤드롭추가
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
업로드 드롭존이 실제 드래그앤드롭 파일 선택을 지원하도록 만들어 업로드 흐름을 더 직관적으로 만든다.

## 작업 내역
- [x] 드래그앤드롭 이벤트 처리 추가
- [x] 드롭존 활성 스타일 추가
- [x] 문서 및 루트 TODO 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `frontend/README.md`, `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 브라우저별 drag event bubbling 차이로 활성 상태 해제가 꼬이지 않도록 주의한다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
