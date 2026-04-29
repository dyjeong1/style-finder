---
id: TSK-0001-업로드선택미리보기통합
plan_id: PLAN-20260420-업로드영역통합UX개선
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
업로드 선택, 이미지 미리보기, 삭제 흐름을 하나의 영역으로 묶어 더 자연스러운 업로드 경험을 만든다.

## 작업 내역
- [x] 업로드 영역과 미리보기 영역 통합
- [x] 정사각형 미리보기 및 삭제 버튼 추가
- [x] 분석 버튼 활성/비활성 흐름 정리
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 삭제 버튼 클릭 시 파일 선택창이 다시 열리지 않도록 이벤트 처리 주의가 필요하다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
