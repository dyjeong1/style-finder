---
id: TSK-0001-추천분석패널정리
plan_id: PLAN-20260506-추천분석패널핵심항목만노출
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-06
---

## 목적
추천 분석 패널에서 사용자 행동과 직접 연결되는 핵심 정보만 남기고 나머지 보조 설명은 제거한다.

## 작업 내역
- [x] 패널 보조 문구 제거
- [x] `검색 힌트` 제거
- [x] smoke 테스트 정리
- [x] 문서/README/TODO 반영

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/e2e/core-flow.spec.ts`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd frontend && npm run build`
- `cd frontend && npm run test:e2e:local:smoke -- --grep "@smoke 업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"`
- 인앱 브라우저 `http://127.0.0.1:3000/recommendations?uploaded_image_id=...` 확인

## 의존성/리스크
- 감지 품목 정보는 남기되 중복 정보 제거로 인한 레이아웃 깨짐은 없어야 한다.

## 완료 기준(DoD)
- [x] 패널에 `감지 카테고리`, `감지 품목`만 보인다.
- [x] smoke 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
