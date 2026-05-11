---
id: TSK-0004-업로드세부타이포보정
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-05-10
---

## 목적
업로드 화면과 최근 업로드 카드의 세부 타이포그래피, 문구, 간격을 브라우저 주석 기준으로 미세 보정합니다.

## 작업 내역
- [x] 업로드 제목 크기를 최근 업로드 제목과 같은 계열로 축소
- [x] 업로드 안내 문구를 2줄 구성으로 정리
- [x] 제목과 업로드 영역 사이 간격 축소
- [x] 브랜드 보조 문구를 `이미지 기반 상품 추천`으로 변경
- [x] 최근 업로드 파일명 색상 보정 및 보조 문구 제거

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/components/app-shell.tsx`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `.sisyphus/plans/PLAN-20260510-화이트모드문서형리디자인.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/PLAN.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/SPEC.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0004-업로드세부타이포보정/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0004-업로드세부타이포보정/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 상단 카드와 최근 업로드 카드 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 주석 기반 미세 보정이라 작은 폰트/간격 차이가 다른 브레이크포인트에서 다시 달라 보일 수 있어 브라우저 재확인이 필요합니다.

## 완료 기준(DoD)
- [x] 주석 6건 반영 완료
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
