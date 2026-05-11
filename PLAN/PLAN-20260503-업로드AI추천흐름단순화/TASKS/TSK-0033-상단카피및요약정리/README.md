---
id: TSK-0033-상단카피및요약정리
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-03
---

## 목적
브라우저 주석 기준으로 브랜드 보조 문구와 업로드/추천/위시리스트 상단 표현을 더 간결하게 정리하고, 필터와 중복되는 요약 카드 노이즈를 제거한다.

## 작업 내역
- [x] 헤더 브랜드 보조 문구를 `이미지 기반 스타일 추천`으로 교체
- [x] 업로드 화면 메인 헤드라인 제거
- [x] 추천/위시리스트 상단 요약 카드 묶음 제거
- [x] 문서와 화면 검증 반영

## 산출물(Artifacts)
- `frontend/components/app-shell.tsx`
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/app/(main)/wishlist/page.tsx`
- `README.md`
- `TODO.md`
- `PLAN/PLAN-20260503-업로드AI추천흐름단순화/PLAN.md`

## 테스트/검증
- `cd frontend && npm run build` 통과
- 인앱 브라우저에서 `/upload`, `/recommendations`, `/wishlist` 화면을 다시 확인해 주석 반영 여부 검증

## 의존성/리스크
- 추천/위시리스트의 상단 요약 카드를 제거해도 핵심 상태는 필터/빈 상태/상품 카드에서 충분히 드러나야 한다.

## 완료 기준(DoD)
- [x] 브랜드 보조 문구가 요청 문구로 교체됨
- [x] 업로드 상단 헤드라인이 제거됨
- [x] 추천/위시리스트 상단 요약 카드가 제거됨
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서 갱신
