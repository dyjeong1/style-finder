---
id: SPEC-PLAN-20260423-검색어하드코딩제거
title: 검색어 하드코딩 제거 스펙
status: done
priority: P0
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-검색어하드코딩제거
  tasks: [TSK-0001-동적코디검색어생성]
tags: [backend, recommendation, image-analysis]
---

## 목표
검색어 힌트가 이미지별 색상 분포를 기반으로 생성되도록 한다.

## 백엔드 스펙
- 기본 검색어는 `{색상} {카테고리}` 형태로 생성한다.
- 특정 코디 조합이 명확할 때만 `셔츠`, `니트 베스트`, `메리제인 슈즈`, `숄더백` 같은 구체 명칭을 사용한다.
- 다른 이미지 fixture가 기존 테스트 이미지 검색어를 그대로 재사용하지 않는 회귀 테스트를 둔다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- `cd frontend && npm run build`
