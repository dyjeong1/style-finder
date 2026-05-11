---
id: TSK-0001-헤더리셋버튼제거
plan_id: PLAN-20260421-헤더업로드초기화제거
owner: Codex
status: done
estimate: 0.3d
updated_at: 2026-04-21
---

## 목적
헤더의 `업로드 초기화` 버튼을 제거해 상단 영역을 메뉴 중심으로 단순화한다.

## 작업 내역
- [x] 헤더 버튼 제거
- [x] 불필요한 import/handler 정리
- [x] 문서 반영

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/components/app-shell.tsx`
- 문서/노트북: `PLAN/PLAN-20260421-헤더업로드초기화제거/*`

## 테스트/검증
- `cd frontend && npm run build`
- `/upload`, `/recommendations`, `/wishlist` 헤더 수동 확인

## 의존성/리스크
- 선행 TASK/시스템/권한: 없음

## 완료 기준(DoD)
- [x] 헤더에서 버튼이 사라진다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
