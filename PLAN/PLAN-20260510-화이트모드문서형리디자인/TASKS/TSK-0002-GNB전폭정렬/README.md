---
id: TSK-0002-GNB전폭정렬
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-05-10
---

## 목적
브라우저에서 상단 GNB가 본문 컨테이너 폭과 함께 묶여 보여 화면 전체 가로폭과 어긋나 보이는 문제를 보정합니다.

## 작업 내역
- [x] 브라우저에서 GNB 잘림/폭 어긋남 현상 확인
- [x] 헤더 전폭 구조와 본문 컨테이너 폭 제약 분리
- [x] 브라우저 재검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `.sisyphus/plans/PLAN-20260510-화이트모드문서형리디자인.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/PLAN.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/SPEC.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0002-GNB전폭정렬/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0002-GNB전폭정렬/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 상단 GNB 시각 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 상단 헤더와 본문 컨테이너 폭을 분리하면 다른 브레이크포인트에서 패딩 균형이 어색해질 수 있어 브라우저 확인이 필요합니다.

## 완료 기준(DoD)
- [x] GNB가 화면 전폭 기준으로 자연스럽게 보임
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
