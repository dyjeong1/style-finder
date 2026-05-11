---
id: TSK-0001-추천섹션요약바구현
plan_id: PLAN-20260423-추천카테고리바로가기
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
추천 전체 보기에서 카테고리 섹션으로 빠르게 이동할 수 있는 요약 바를 구현한다.

## 작업 내역
- [x] 카테고리 섹션 앵커 ID 함수 추가
- [x] 카테고리 요약/바로가기 바 렌더링 추가
- [x] 요약 바 스타일 추가
- [x] 문서와 검증 결과 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build` 성공

## 의존성/리스크
- 기존 섹션 렌더링과 상품 카드 동작을 유지한다.
- 앵커 링크는 현재 페이지 내 이동으로만 동작한다.

## 완료 기준(DoD)
- [x] 카테고리 요약 바가 표시된다.
- [x] 요약 항목 클릭 시 카테고리 섹션으로 이동한다.
- [x] 프론트 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
