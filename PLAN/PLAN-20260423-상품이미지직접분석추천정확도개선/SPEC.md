---
id: SPEC-PLAN-20260423-상품이미지직접분석추천정확도개선
title: 상품 이미지 직접 분석 추천 정확도 개선 스펙
status: done
priority: P0
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-상품이미지직접분석추천정확도개선
  tasks: [TSK-0001-상품이미지색상분석랭킹반영]
tags: [backend, recommendation, image-analysis]
---

## 목표
네이버 쇼핑 상품 이미지의 실제 색상 정보를 추출해 업로드 이미지와 직접 비교한다.

## 백엔드 스펙
- 이미지 색상 분석 로직을 `src.services.image_analysis` 공용 서비스로 분리한다.
- 네이버 상품 이미지 URL을 짧은 timeout으로 다운로드한다.
- 상품 이미지 분석 성공 시 `ProductRecord.dominant_color`, `ProductRecord.feature_vector`에 이미지 기반 값을 반영한다.
- 상품 이미지 분석 실패 시 상품명 색상 추론과 hash vector fallback을 사용한다.
- 추천 점수에 상품 이미지 색상 일치 보너스 `product_image_color_bonus`를 추가한다.
- 환경값으로 이미지 분석 여부, 이미지 timeout, 최대 이미지 bytes, 분석 시도 개수를 조정할 수 있다.

## 프론트 스펙
- 추천 매칭 정보에서 상품 이미지 대표 색상을 표시한다.
- 점수 breakdown에서 상품명 색상 보너스와 이미지 색상 보너스를 분리해 표시한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 통과
- `cd frontend && npm run build` 통과
