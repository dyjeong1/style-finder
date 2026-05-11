---
id: TSK-0030-업로드상태비영속화
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-03
---

## 목적
업로드 ID/분석 결과/업로드 히스토리를 localStorage에 남기지 않도록 프론트 상태 흐름을 정리한다.

## 작업 내역
- [x] 업로드 관련 localStorage 키와 헬퍼 제거 범위 정리
- [x] 업로드/추천 페이지를 메모리 기준 현재 업로드 1건 흐름으로 변경
- [x] 최근 업로드 재사용 UI 제거

## 산출물(Artifacts)
- `frontend/lib/api.ts`
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/e2e/core-flow.spec.ts`

## 테스트/검증
- `cd frontend && npm run build`로 타입/빌드 검증 통과
- `cd frontend && npm run test:e2e -- --project=chromium --grep "업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"` 통과
- 업로드 페이지가 `uploaded_image_id` 쿼리만 전달하고 추천 페이지가 응답 `analysis`만으로 패널을 구성하는지 코드 경로 확인

## 의존성/리스크
- URL 기반 추천 진입 방식과 충돌하지 않도록 업로드 직후 이동 흐름을 함께 조정해야 한다.

## 완료 기준(DoD)
- [x] 업로드 관련 localStorage 영속 상태 제거
- [x] 새 업로드 시 이전 분석 상태 미노출
- [x] 테스트/문서 갱신
