---
id: SPEC-PLAN-20260423-이미지색상기반추천정확도개선
title: 이미지 색상 기반 추천 정확도 개선 스펙
status: done
priority: P0
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-이미지색상기반추천정확도개선
  tasks: [TSK-0001-업로드이미지색상분석반영]
tags: [backend, recommendation, image-analysis]
---

## 목표
업로드 이미지의 실제 대표 색상을 분석해 네이버 검색어와 추천 점수에 반영한다.

## 백엔드 스펙
- 업로드 이미지 분석 결과에 `dominant_color`를 추가한다.
- Pillow가 사용 가능하면 이미지 픽셀을 샘플링해 평균 RGB, 밝기, 채도를 계산한다.
- 색상은 `black`, `white`, `gray`, `beige`, `brown`, `navy`, `blue`, `green`, `red`, `pink`, `yellow` 계열로 분류한다.
- 네이버 자동 검색어에는 대표 색상 키워드를 앞에 추가한다.
- 추천 점수에는 상품명에 색상 키워드가 포함될 때 `color_bonus`를 추가한다.
- Pillow 사용이 불가능하거나 이미지 파싱 실패 시 기존 해시 기반 분석으로 fallback한다.

## 프론트 스펙
- 업로드 분석 타입에 `dominant_color`를 포함한다.
- 업로드 화면과 추천 화면의 분석 요약에 색상 신호를 표시한다.
- 상품별 매칭 정보에 색상 신호와 색상 보너스를 표시한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 통과
- `cd frontend && npm run build` 통과
