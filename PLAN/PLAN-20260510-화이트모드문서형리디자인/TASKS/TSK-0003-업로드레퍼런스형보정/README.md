---
id: TSK-0003-업로드레퍼런스형보정
plan_id: PLAN-20260510-화이트모드문서형리디자인
owner: Codex
status: done
estimate: 0.3d
updated_at: 2026-05-10
---

## 목적
업로드 메인 카드를 참고 이미지와 유사한 구성으로 보정해 중앙 타이틀, 점선 업로드 영역, 큰 액션 버튼 중심의 인상을 강화합니다.

## 작업 내역
- [x] 참고 이미지 기준 업로드 카드 구조 재정리
- [x] 상단 중앙 타이틀, 카메라 아이콘, 점선 드롭존 스타일 반영
- [x] `허용 이미지: PNG, JPG, JPEG, WEBP` 문구 유지
- [x] 브라우저 재검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `.sisyphus/plans/PLAN-20260510-화이트모드문서형리디자인.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/PLAN.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/SPEC.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0003-업로드레퍼런스형보정/README.md`
  - `PLAN/PLAN-20260510-화이트모드문서형리디자인/TASKS/TSK-0003-업로드레퍼런스형보정/TODO.md`

## 테스트/검증
- in-app browser에서 `/upload` 메인 카드 시각 확인
- `cd frontend && npm run build`

## 의존성/리스크
- 업로드 카드 카피와 레이아웃을 참고 이미지 쪽으로 맞추면서도 실제 기능 오해가 없도록 버튼 의미는 기존 흐름을 유지해야 합니다.

## 완료 기준(DoD)
- [x] 업로드 카드가 참고 이미지에 가까운 시각 구조를 가짐
- [x] 허용 이미지 문구 유지
- [x] 브라우저 재검증 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 및 TASK 문서 갱신
