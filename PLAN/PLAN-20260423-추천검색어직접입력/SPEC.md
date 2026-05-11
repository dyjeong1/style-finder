---
id: SPEC-PLAN-20260423-추천검색어직접입력
title: 추천 검색어 직접 입력 스펙
status: done
priority: P1
created_at: 2026-04-23
updated_at: 2026-04-23
related:
  plan: PLAN-20260423-추천검색어직접입력
  tasks: [TSK-0001-추천검색어직접입력구현]
tags: [backend, frontend, recommendation, naver]
---

## 목표
추천 페이지에서 사용자가 직접 입력한 검색어로 네이버 쇼핑 후보를 조회할 수 있게 한다.

## 백엔드 스펙
- `GET /recommendations`에 선택 파라미터 `custom_query`를 추가한다.
- `custom_query`가 있으면 자동 생성 검색어 대신 직접 입력 검색어를 사용한다.
- 전체 보기에서는 직접 입력 검색어에 상의/하의/아우터/신발/가방 키워드를 붙여 카테고리별 조회를 유지한다.
- 특정 카테고리 필터가 있으면 해당 카테고리 키워드만 보강한다.

## 프론트 스펙
- 추천 필터 영역에 직접 검색어 입력 필드를 추가한다.
- `검색어 적용` 클릭 또는 Enter 입력으로 추천을 재조회한다.
- `검색어 초기화`를 누르면 기존 이미지 분석 기반 자동 검색어로 돌아간다.
- 적용 중인 직접 검색어를 안내 문구로 표시한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 성공
- `cd frontend && npm run build` 성공
