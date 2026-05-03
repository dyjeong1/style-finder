---
id: SPEC-PLAN-20260504-프론트디자인고급화
title: 프론트 디자인 고급화 스펙
status: done
priority: P1
created_at: 2026-05-04
updated_at: 2026-05-04
related:
  plan: [PLAN-20260504-프론트디자인고급화]
  tasks: [TSK-0001-편집숍감성비주얼고도화]
tags: [frontend, typography, polish]
---

## 1. 목적
StyleMatch 프론트가 기능적으로 정돈된 수준을 넘어서, 시각적으로 더 아름답고 기억에 남는 편집숍형 경험을 제공하도록 고급화합니다.

## 2. 시각 스펙
- 디스플레이 타이포: 본문은 Pretendard를 유지하고, 대형 타이틀에는 세리프 계열 디스플레이 폰트를 제한적으로 사용합니다.
- 히어로 방향: 업로드/추천/위시리스트 각각 하나의 강한 비주얼 앵커와 얇은 서포트 레일을 둡니다.
- 색/재질: 웜 베이지 기반은 유지하되, 잉크 네이비 대비와 메탈릭 골드 포인트를 더 분명하게 사용합니다.

## 3. 인터랙션 스펙
- 느린 부유 모션과 섹션 오버레이로 첫 화면의 분위기를 강화합니다.
- 카드 hover는 더 깊은 리프트와 하이라이트 이동으로 정교화합니다.
- CTA와 보조 레일은 서로 다른 시각 밀도로 구분합니다.

## 4. 구현 스펙
- `frontend/app/globals.css`: 디스플레이 폰트, 히어로 오버레이, 섹션 레일, 상품 카드 광택/리프트 스타일 보강
- `frontend/components/app-shell.tsx`: 헤더 카피 구조와 브랜드 프레젠테이션 고도화
- `frontend/app/(main)/upload/page.tsx`: 히어로 카피와 드롭존 무드 강화
- `frontend/app/(main)/recommendations/page.tsx`: 추천 상단에 편집형 하이라이트와 비주얼 포인트 추가
- `frontend/app/(main)/wishlist/page.tsx`: 저장 보드의 프리미엄 톤 강화

## 5. 비기능 스펙
- 기존 업로드/추천/저장 흐름을 유지합니다.
- 모바일 대응과 빌드 안정성을 보장합니다.

## 6. 수용 기준
- [x] 세 화면 모두 이전보다 더 강한 미감과 화면별 개성을 가짐
- [x] 추천 상품/저장 상품 카드가 더 매력적으로 보임
- [x] `cd frontend && npm run build` 통과
