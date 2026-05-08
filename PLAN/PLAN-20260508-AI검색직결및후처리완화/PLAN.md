---
id: PLAN-20260508-AI검색직결및후처리완화
title: AI 검색 직결 및 후처리 완화
status: done
priority: P1
created_at: 2026-05-08
updated_at: 2026-05-08
related:
  tasks:
    - TSK-0001-AI검색직결및필터완화
tags:
  - backend
  - recommendations
  - naver
  - ai
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 추천 검색은 AI가 분석한 착장 품목과 검색어를 최대한 그대로 따라가야 한다.
- 현재 성능/운영 이슈:
  - AI가 정상 응답해도 `bag` 누락 같은 일부 카테고리를 규칙 분석으로 다시 보강하는 경로가 남아 있다.
  - 네이버 후보 후처리가 AI query의 세부 품목/의도까지 강하게 검사해, 같은 카테고리 상품도 내부에서 과하게 제거된다.

## 2. 목표/가설
- 1차 지표(Primary): AI가 만든 `detected_items`/`category_query_hints`가 추천 검색의 직접 입력으로 유지된다.
- 2차 지표(Secondary): 네이버 후보가 같은 카테고리 안에서 세부 표현 차이만으로 과도하게 버려지지 않는다.
- 가설: AI 성공 시 규칙 보강을 제거하고 네이버 relevance 필터를 카테고리 중심으로 완화하면, 누락 카테고리와 빈 추천 케이스가 줄어든다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - AI 성공 시 규칙 기반 `bag` 보강 제거
  - 네이버 후보 relevance 필터 완화
  - 백엔드 테스트/문서 정리
- 제외 범위:
  - AI provider 실패 시 최후 fallback 정책 변경
  - 프론트 화면 구조 변경
- 산출물(코드/모델/대시보드/문서):
  - `backend/src/services/store.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/tests/test_vision_outfit_analyzer.py`
  - `backend/tests/test_naver_shopping.py`
  - 관련 PLAN/TASK/README/TODO 문서

## 4. 일정/마일스톤
- M1(원인 확인 및 범위 확정): 2026-05-08
- M2(AI 검색 직결 경로 정리): 2026-05-08
- M3(네이버 후처리 완화 및 테스트): 2026-05-08
- M4(문서/검증/커밋 마감): 2026-05-08

## 5. 리스크 & 가정
- 데이터 품질/지연/누락: relevance 필터를 완화하면 같은 카테고리 안의 노이즈 후보가 일부 늘 수 있다.
- 시스템/리소스 제약: AI provider 실패 시에는 기존 규칙 fallback 을 유지해야 한다.
- 보안/개인정보: 외부 전송 범위나 저장 방식 변경은 없다.

## 6. 검증/수용 기준(DoD)
- [x] AI 성공 시 규칙 기반 `bag` 보강이 더 이상 실행되지 않는다.
- [x] 네이버 후보는 카테고리만 맞으면 세부 품목 mismatch 만으로 제거되지 않는다.
- [x] 관련 백엔드 테스트와 문서가 최신 상태다.

## 7. 변경 이력
- 2026-05-08: PLAN 생성.
- 2026-05-08: AI 성공 시 규칙 기반 `bag` 보강을 제거하고, 네이버 relevance 필터를 카테고리 중심으로 완화함.
