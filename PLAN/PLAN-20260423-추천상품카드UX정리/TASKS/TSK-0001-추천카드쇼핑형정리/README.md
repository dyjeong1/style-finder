---
id: TSK-0001-추천카드쇼핑형정리
plan_id: PLAN-20260423-추천상품카드UX정리
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
추천 상품 카드를 쇼핑 탐색에 적합하게 이미지/상품명/가격/액션 중심으로 정리한다.

## 작업 내역
- [x] 추천 카드 마크업 재구성
- [x] 추천 카드 스타일 개선
- [x] 분석 점수/신호 보조 정보화
- [x] 문서와 검증 결과 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build` 성공

## 의존성/리스크
- 기존 위시리스트 저장/상품 보기 동작을 유지한다.
- 네이버 상품 이미지 비율이 다양하므로 `object-fit` 기반으로 안정화한다.

## 완료 기준(DoD)
- [x] 추천 카드가 쇼핑형 UI로 정리된다.
- [x] 프론트 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
