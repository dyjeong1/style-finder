---
id: PLAN-20260510-AI분석검색정확도보강
title: AI 분석·검색 정확도 보강
status: done
priority: P1
created_at: 2026-05-10
updated_at: 2026-05-10
related:
  tasks:
    - TSK-0001-AI품목및검색정확도보강
tags:
  - backend
  - ai
  - naver
  - ranking
  - vision
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 사용자는 업로드 이미지에서 AI가 읽은 품목과 네이버 쇼핑 추천 상품이 자연스럽게 이어지길 기대합니다.
- 현재 성능/운영 이슈:
  - AI가 카테고리는 맞게 감지해도 `가방`, `슈즈`, `팬츠`처럼 일반 품목명으로 남는 경우가 있습니다.
  - 네이버 쇼핑 검색이 한 번의 query와 카테고리 중심 완화 규칙에 치우치면서, 같은 카테고리지만 실제 의도와 다른 상품이 상단에 뜰 수 있습니다.

## 2. 목표/가설
- 1차 지표(Primary): 감지 품목의 세부명이 더 구체적으로 유지되고, 추천 상단 상품이 AI query의 품목 의도와 더 잘 맞는다.
- 2차 지표(Secondary): 긴 query에서도 네이버 후보가 비거나 과하게 흔들리지 않고, 보조 query를 통해 안정적으로 후보를 확보한다.
- 가설: 같은 카테고리 안의 제한적 품목 보정과 query 정합성 기반 재정렬을 함께 적용하면 감지 정확도와 추천 정확도가 동시에 올라간다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - AI 일반 품목명에 대한 same-category 규칙 보정
  - 네이버 query variant 생성
  - 네이버 후보 정렬 및 추천 점수의 query 정합성 보강
  - 회귀 테스트와 문서 갱신
- 제외 범위:
  - 비전 provider 모델 자체 교체
  - 프론트 UI 구조 변경
- 산출물(코드/모델/대시보드/문서):
  - `backend/src/services/recommendation_intent.py`
  - `backend/src/services/store.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/src/api/routes/recommendation.py`
  - `backend/tests/test_ai_search_path.py`
  - `backend/tests/test_naver_shopping.py`
  - `backend/tests/test_store_color_matching.py`
  - 관련 PLAN/TASK/README/TODO 문서

## 4. 일정/마일스톤
- M1(병목 정리 및 설계): 2026-05-10
- M2(품목/검색 정합성 보강 구현): 2026-05-10
- M3(회귀 테스트 및 문서 정리): 2026-05-10

## 5. 리스크 & 가정
- 데이터 품질/지연/누락: 규칙 보정 범위를 넓히면 AI 결과를 다시 덮어쓸 위험이 있으므로 같은 카테고리의 일반 품목명일 때만 제한적으로 적용합니다.
- 시스템/리소스 제약: 네이버 query variant 는 1개 보조 query까지만 허용해 API 호출 수를 과도하게 늘리지 않습니다.
- 보안/개인정보: 외부 전송 대상과 저장 구조 변화는 없습니다.

## 6. 검증/수용 기준(DoD)
- [x] AI 일반 품목명이 같은 카테고리 규칙 품목명으로 제한 보정된다.
- [x] 네이버 query variant 와 후보 재정렬이 테스트로 검증된다.
- [x] 추천 랭킹이 query 품목/디스크립터 정합성을 반영한다.
- [x] 관련 README/TODO/PLAN/TASK 문서가 최신 상태다.

## 7. 변경 이력
- 2026-05-10: PLAN 생성.
- 2026-05-10: same-category 규칙 보정, 네이버 query variant, 후보/랭킹 정합성 보강, 회귀 테스트를 추가함.
- 2026-05-10: 후속 PLAN에서 same-category 규칙 보정은 제거하고, query variant/랭킹 보강만 유지함.
