---
id: SPEC-PLAN-20260417-프론트비주얼리프레시
title: 프론트 비주얼 리프레시 스펙
status: done
priority: P1
created_at: 2026-04-17
updated_at: 2026-04-20
related:
  plan: [PLAN-20260417-프론트비주얼리프레시]
  tasks: [TSK-0001-프리텐다드및핵심화면리디자인]
tags: [frontend, design, pretendard]
---

## 1. 목적
로컬 단일 사용자용 StyleMatch 프론트의 시각 완성도를 높여, 기능 확인뿐 아니라 실제로 쓰고 싶은 화면 인상을 제공합니다.

## 2. 기능 스펙
- 전역 타이포그래피를 Pretendard 기준으로 맞춥니다.
- 공통 앱 셸에 더 명확한 브랜드 헤더와 유리 질감 네비게이션을 적용합니다.
- `/upload`, `/recommendations`, `/wishlist`에 페이지 헤더 블록과 개선된 카드 레이아웃을 적용합니다.
- 추천 카드와 최근 업로드 목록에 썸네일/메타데이터 위계를 강화합니다.

## 3. 비기능 스펙
- 기존 기능 흐름과 API 호출 방식은 유지합니다.
- 모바일 대응을 유지해야 합니다.
- 빌드 오류 없이 동작해야 합니다.

## 4. 구현 스펙
- `frontend/app/layout.tsx`에서 기존 구글 폰트 의존을 제거하고 전역 CSS 기반 폰트 적용으로 정리
- `frontend/app/globals.css`에서 색상 변수, 배경, 카드, 헤더, 페이지 섹션, 반응형 스타일 재정의
- 업로드/추천/위시리스트 페이지에 헤더 요약과 시각 강조 영역 추가

## 5. 수용 기준
- [x] Pretendard 적용 완료
- [x] 세 핵심 페이지의 시각 위계 개선 완료
- [x] `cd frontend && npm run build` 통과
