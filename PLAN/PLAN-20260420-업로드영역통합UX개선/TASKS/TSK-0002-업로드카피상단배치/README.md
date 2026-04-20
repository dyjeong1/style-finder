---
id: TSK-0002-업로드카피상단배치
plan_id: PLAN-20260420-업로드영역통합UX개선
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-20
---

## 목적
통합 업로드 박스 안에서 안내 카피를 상단에, 정사각형 이미지 영역을 하단에 배치해 읽는 순서를 더 자연스럽게 만든다.

## 작업 내역
- [x] 업로드 카피/안내 문구를 상단으로 이동
- [x] 정사각형 미리보기 영역을 하단으로 재배치
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 텍스트/버튼/미리보기 순서가 바뀌어도 삭제 버튼과 업로드 클릭 동작은 그대로 유지되어야 한다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
