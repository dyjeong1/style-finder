---
id: TSK-0001-추천스타일칩비노출
plan_id: PLAN-20260506-추천분석스타일칩숨김
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-06
---

## 목적
추천 분석 패널에서 사용자에게 꼭 필요하지 않은 내부 스타일 요약 칩과 설명을 숨긴다.

## 작업 내역
- [x] 스타일 칩 비노출
- [x] 도출 설명 문구 비노출
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
- 사용자용 정보와 내부 계산용 정보를 구분하되, 추천 기능 회귀는 없어야 한다.

## 완료 기준(DoD)
- [x] 스타일 칩과 설명 문구가 화면에 보이지 않는다.
- [x] 감지 품목/검색 힌트는 유지된다.
- [x] smoke 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
