---
id: TSK-0002-위시리스트카드UI강화
plan_id: PLAN-20260416-위시리스트상세화
owner: Codex
status: doing
estimate: 0.5d
updated_at: 2026-04-16
---

## 목적
위시리스트를 텍스트 목록이 아니라 썸네일과 핵심 메타데이터가 함께 보이는 카드 형태로 강화합니다.

## 작업 내역
- [x] 위시리스트 카드 썸네일 표시
- [x] 이미지 실패 시 대체 썸네일 처리
- [x] 스타일 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/(main)/wishlist/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 목 상품 이미지 URL이 실제 이미지가 아닐 수 있어 대체 썸네일이 필요합니다.

## 완료 기준(DoD)
- [x] 카드형 위시리스트 UI 반영
- [x] 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
