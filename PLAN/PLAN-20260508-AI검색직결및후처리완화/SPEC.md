---
id: SPEC-PLAN-20260508-AI검색직결및후처리완화
title: AI 검색 직결 및 후처리 완화 스펙
status: done
priority: P1
created_at: 2026-05-08
updated_at: 2026-05-08
related:
  plan:
    - PLAN-20260508-AI검색직결및후처리완화
  tasks:
    - TSK-0001-AI검색직결및필터완화
tags:
  - backend
  - recommendations
  - naver
  - ai
---

## 1. 요구사항
1. AI가 정상 응답한 경우에는 규칙 분석으로 누락 카테고리를 추가 보강하지 않는다.
2. 추천 검색은 `analysis.category_query_hints`에 담긴 AI query를 그대로 사용한다.
3. 네이버 후보 필터는 잘못된 카테고리만 제외하고, 세부 품목/의도 mismatch 때문에 같은 카테고리 상품을 버리지 않는다.
4. AI provider 오류/미가동 시에는 기존 규칙 fallback 경로를 유지한다.

## 2. 상태 관리 규칙
- `analysis_source == vision`이면 규칙 기반 추가 카테고리 병합을 수행하지 않는다.
- `analysis_source == rule_fallback`일 때만 규칙 분석 결과를 그대로 사용한다.
- 네이버 후보 필터는 `category_hint` 기준 카테고리 일치 여부만 검사한다.

## 3. 검증 시나리오
- AI가 `top`과 `accessory`만 반환한 경우 분석 결과에 `bag`이 자동 추가되지 않는다.
- AI predictor 가 예외를 던지면 기존처럼 규칙 fallback 결과를 사용한다.
- `그레이 가디건` query로 검색했을 때 `그레이 집업 점퍼` 같은 같은 outer 카테고리 후보는 유지된다.
- `남색 롱슬리브 티셔츠` query로 검색했을 때 `네이비 반팔 티셔츠` 같은 같은 top 카테고리 후보는 유지된다.
