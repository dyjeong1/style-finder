---
id: SPEC-PLAN-20260424-품목세분화및비전재정렬
title: 품목 세분화 및 비전 재정렬 스펙
status: doing
priority: P0
created_at: 2026-04-24
updated_at: 2026-04-24
related:
  plan: PLAN-20260424-품목세분화및비전재정렬
  tasks: [TSK-0001-품목명세분화, TSK-0002-다중아이템분리개선, TSK-0003-클립비전재정렬연결]
tags: [image-analysis, recommendation, vision]
---

## 목표
업로드 이미지의 품목 인식과 추천 랭킹 정확도를 동시에 끌어올린다.

## 백엔드 스펙
- 카테고리별 분석 결과에 세부 품목명과 구조화된 감지 아이템 목록을 포함한다.
- 다중 아이템 분리는 foreground 연결 컴포넌트와 위치/색상 규칙을 함께 사용한다.
- 추천 점수는 기존 색상/텍스트 점수 위에 선택적 비전 임베딩 점수를 추가로 반영한다.
- CLIP 패키지가 없거나 비활성화된 경우 기존 점수 체계로 안전하게 fallback한다.

## 프론트 스펙
- 업로드/추천 화면에서 감지된 카테고리와 세부 검색 힌트를 더 읽기 쉽게 노출한다.
- 추가된 응답 필드를 타입에 반영한다.

## 검증
- `PYTHONPATH=backend python3 -m pytest backend/tests -q`
- `cd frontend && npm run build`
