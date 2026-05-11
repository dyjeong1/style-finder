---
id: TSK-0001-프론트위시리스트정렬구현
plan_id: PLAN-20260420-위시리스트정렬추가
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
위시리스트를 최신 저장 순서 외에도 가격/이름 기준으로 정렬할 수 있게 한다.

## 작업 내역
- [x] 정렬 상태와 옵션 UI 추가
- [x] 파생 정렬 배열 렌더링 적용
- [x] 문서 및 루트 TODO 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/wishlist/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `frontend/README.md`, `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 가격/저장 시각이 비정상 데이터일 경우 정렬 결과가 기대와 다를 수 있다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
