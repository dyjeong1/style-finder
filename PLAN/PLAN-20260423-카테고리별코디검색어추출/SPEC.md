---
id: SPEC-PLAN-20260423-카테고리별코디검색어추출
title: 카테고리별 코디 검색어 추출 스펙
status: done
priority: P0
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-카테고리별코디검색어추출
  tasks: [TSK-0001-배경제외영역별검색어생성]
tags: [backend, recommendation, image-analysis]
---

## 목표
업로드 이미지의 전체 대표색이 아닌 카테고리별 품목/색상 힌트로 네이버 검색어를 만든다.

## 백엔드 스펙
- `UploadAnalysis`에 `category_query_hints`를 추가한다.
- 이미지 edge 색상으로 배경색을 추정하고, 배경과 가까운 픽셀은 제외한다.
- 코디 이미지의 일반적인 위치를 기준으로 상의/하의/아우터/신발/가방 영역별 색상 분포를 계산한다.
- 생성된 힌트가 있으면 `build_naver_query`에서 카테고리별 힌트를 우선 사용한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd frontend && npm run build`
