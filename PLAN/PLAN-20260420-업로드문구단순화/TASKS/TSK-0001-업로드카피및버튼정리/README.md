---
id: TSK-0001-업로드카피및버튼정리
plan_id: PLAN-20260420-업로드문구단순화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
업로드 화면의 불필요한 문구와 버튼을 줄여 첫 화면의 집중도를 높인다.

## 작업 내역
- [x] 헤더/드롭존/보조 문구 단순화
- [x] 최근 업로드 버튼 제거 및 카드 클릭형 재사용 적용
- [x] 문서 및 루트 TODO 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `frontend/README.md`, `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 버튼 제거 후에도 최근 업로드 재사용 의도가 충분히 드러나야 한다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
