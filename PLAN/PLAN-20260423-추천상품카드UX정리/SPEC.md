---
id: SPEC-PLAN-20260423-추천상품카드UX정리
title: 추천 상품 카드 UX 정리 스펙
status: done
priority: P1
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-추천상품카드UX정리
  tasks: [TSK-0001-추천카드쇼핑형정리]
tags: [frontend, recommendation, ux]
---

## 목표
추천 상품 카드를 실제 쇼핑 탐색에 맞게 이미지/상품명/가격/액션 중심으로 재구성한다.

## 프론트 스펙
- 상품 이미지는 카드 상단에서 더 큰 비율로 표시한다.
- 상단 배지는 데이터 출처, 카테고리, 랭킹/저장 상태를 간결하게 표시한다.
- 상품명과 가격을 주요 정보로 배치한다.
- `상품 보기`와 `위시리스트 담기` 버튼을 카드 하단 CTA로 정리한다.
- 유사도/톤/무드/실루엣/점수 breakdown은 `details` 영역으로 접어 보조 정보화한다.
- 모든 폰트 크기는 기존 규칙대로 `pt` 단위를 사용한다.

## 검증
- `cd frontend && npm run build` 성공
