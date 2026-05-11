---
id: TSK-0001-추천이미지오버레이정리
plan_id: PLAN-20260506-추천업로드이미지상단오버레이정리
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-06
---

## 목적
추천 기준 이미지 확대 보기를 화면 전체 dimmed 모달 대신 상단 오버레이 카드로 바꾸고, 이미지 우측 상단 `X` 닫기 버튼을 제공한다.

## 작업 내역
- [x] 확대 보기 레이아웃을 상단 오버레이 카드로 변경
- [x] 우측 상단 `X` 닫기 버튼 추가
- [x] 열기/닫기 회귀 테스트 보강
- [x] 문서/README/TODO 반영

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/app/globals.css`
- `frontend/e2e/core-flow.spec.ts`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd frontend && npm run build`
- `cd frontend && npm run test:e2e:local:smoke -- --grep "@smoke 업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"`
- 인앱 브라우저 `http://127.0.0.1:3000/recommendations?uploaded_image_id=...`에서 썸네일 클릭 후 상단 오버레이와 `X` 버튼 확인

## 의존성/리스크
- 오버레이가 추천 화면 헤더/필터 위에 자연스럽게 뜨되 하단 레이아웃을 과도하게 막지 않아야 한다.
- 접근성 이름은 `X` 아이콘만 보이더라도 스크린리더용 라벨을 유지해야 한다.

## 완료 기준(DoD)
- [x] 확대 보기가 dimmed 없는 상단 오버레이 카드로 보인다.
- [x] `X` 버튼으로 닫을 수 있다.
- [x] 유닛/통합 또는 E2E 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
