---
id: TSK-0001-선택후미리보기노출
plan_id: PLAN-20260421-업로드미리보기조건부노출
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-21
---

## 목적
업로드 첫 화면에서는 미리보기를 숨기고, 파일을 선택한 뒤에만 정사각형 이미지 미리보기가 보이도록 만든다.

## 작업 내역
- [x] 파일 미선택 시 정사각형 미리보기 숨김
- [x] 파일 선택 시 정사각형 미리보기 노출
- [x] 업로드 박스 레이아웃 보정 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 파일 선택 직후 object URL 생성 타이밍에 따라 미리보기가 짧게 늦게 보일 수 있다.

## 완료 기준(DoD)
- [x] 파일 선택 전에는 미리보기 정사각형이 없다.
- [x] 파일 선택 후에는 정사각형 미리보기가 나타난다.
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
