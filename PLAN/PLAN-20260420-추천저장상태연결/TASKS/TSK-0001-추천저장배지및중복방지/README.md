---
id: TSK-0001-추천저장배지및중복방지
plan_id: PLAN-20260420-추천저장상태연결
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
추천 카드에서 저장 상태를 바로 보여주고, 이미 저장된 상품의 중복 찜 시도를 막습니다.

## 작업 내역
- [x] 추천 화면에서 위시리스트 상태 조회
- [x] Saved 배지와 비활성 버튼 적용
- [x] 저장 직후 상태 즉시 반영
- [x] 빌드 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`
  - `PLAN/PLAN-20260420-추천저장상태연결/PLAN.md`
  - `PLAN/PLAN-20260420-추천저장상태연결/SPEC.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 위시리스트 조회가 지연되면 Saved 표시가 늦게 붙을 수 있습니다.
- 프론트 상태 동기화가 어긋나지 않도록 저장 직후 즉시 로컬 상태를 갱신해야 합니다.

## 완료 기준(DoD)
- [x] Saved 배지와 비활성화 상태 적용
- [x] 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서 갱신
