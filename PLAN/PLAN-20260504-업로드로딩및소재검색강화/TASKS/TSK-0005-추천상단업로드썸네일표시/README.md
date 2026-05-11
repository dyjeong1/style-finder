---
id: TSK-0005-추천상단업로드썸네일표시
plan_id: PLAN-20260504-업로드로딩및소재검색강화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
추천 화면 상단에 업로드한 원본 이미지를 작은 정사각형 썸네일로 함께 보여줘 어떤 이미지 기준 추천인지 바로 알 수 있게 합니다.

## 작업 내역
- [x] 추천 상단 업로드 썸네일 UI 추가
- [x] 업로드 이미지 URL 연결
- [x] 테스트/문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/lib/api.ts`
- `frontend/app/globals.css`

## 테스트/검증
- `cd frontend && npm run test:e2e:local -- --project=chromium -g '@smoke 업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다|업로드 분석 중 버튼 상태와 진행 시간을 보여준다'`

## 의존성/리스크
- 업로드 이미지가 만료되거나 없는 경우에도 화면이 깨지지 않게 fallback 이 필요합니다.

## 완료 기준(DoD)
- [x] 추천 상단에 업로드 썸네일이 표시된다.
- [x] 업로드 이미지가 없을 때도 레이아웃이 안정적이다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
