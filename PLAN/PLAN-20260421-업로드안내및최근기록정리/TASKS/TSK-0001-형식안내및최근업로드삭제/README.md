---
id: TSK-0001-형식안내및최근업로드삭제
plan_id: PLAN-20260421-업로드안내및최근기록정리
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-21
---

## 목적
업로드 형식 안내 문구 위치를 더 자연스럽게 바꾸고 최근 업로드 기록을 직접 삭제할 수 있게 한다.

## 작업 내역
- [x] 업로드 placeholder 문구를 허용 형식 안내로 교체
- [x] 최근 업로드 카드 삭제 기능 추가
- [x] `Local Mode` 문구 비노출 상태 재확인
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/lib/api.ts`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 최근 업로드 삭제는 브라우저 저장소 기준이라 브라우저별로 기록이 독립적이다.

## 완료 기준(DoD)
- [x] placeholder에 허용 형식 문구가 보인다.
- [x] 최근 업로드 카드를 개별 삭제할 수 있다.
- [x] 헤더에 `Local Mode`가 보이지 않는다.
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
