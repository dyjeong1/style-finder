---
id: PLAN-20260510-AI프롬프트및네이버검색정확도고도화
title: AI 프롬프트 및 네이버 검색 정확도 고도화
status: done
priority: P1
created_at: 2026-05-10
updated_at: 2026-05-10
related:
  tasks:
    - TSK-0001-AI프롬프트와검색정확도보강
tags:
  - backend
  - ai
  - naver
  - query
  - ranking
---

## 1. 배경/문제 정의
- 비즈니스 맥락: AI가 분석한 품목과 검색어가 좋을수록 네이버 쇼핑 추천 정확도도 함께 올라갑니다.
- 현재 성능/운영 이슈:
  - AI가 품목은 맞게 보더라도 쇼핑몰에서 실제로 많이 쓰는 세부 품목명보다 일반적인 표현을 쓸 수 있습니다.
  - 네이버 보조 query 가 너무 단순하면 감지 품목의 강한 신호를 충분히 활용하지 못합니다.
  - 같은 카테고리 안에서도 브랜드, 품목군, 소매/길이 같은 intent mismatch 후보가 상단에 남을 수 있습니다.

## 2. 목표/가설
- 1차 지표(Primary): AI가 더 쇼핑 친화적인 세부 품목명과 query 를 반환한다.
- 2차 지표(Secondary): 네이버 후보 목록과 최종 추천 상단이 감지 품목/브랜드/intent 와 더 잘 맞는다.
- 가설: 프롬프트를 쇼핑 query 중심으로 더 구체화하고, 감지 item 중심 보조 query + 후보 재정렬을 강화하면 검색 정확도가 오른다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - AI 비전 프롬프트 강화
  - 감지 item 중심 보조 query 생성 보강
  - 네이버 후보 정렬의 family/brand/intent conflict penalty 추가
  - 최종 추천 점수의 exact match 세분화
  - 테스트 및 문서 갱신
- 제외 범위:
  - AI 결과를 규칙 분석으로 다시 보정하는 정책 변경
  - 프론트 UI 개편
- 산출물(코드/모델/대시보드/문서):
  - `backend/src/services/vision_outfit_analyzer.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/src/services/store.py`
  - `backend/tests/test_naver_shopping.py`
  - `backend/tests/test_store_color_matching.py`
  - 관련 PLAN/TASK/README/TODO 문서

## 4. 일정/마일스톤
- M1(병목 확인 및 PLAN 확정): 2026-05-10
- M2(프롬프트/검색 정렬 보강): 2026-05-10
- M3(회귀 테스트/문서/커밋): 2026-05-10

## 5. 리스크 & 가정
- 데이터 품질/지연/누락: 보조 query 는 1개로 제한해 API 호출 수를 과도하게 늘리지 않습니다.
- 시스템/리소스 제약: brand/family mismatch penalty 가 너무 세면 recall 이 줄 수 있으므로 제거가 아니라 재정렬 위주로 적용합니다.
- 보안/개인정보: 외부 전송 구조나 저장 방식 변경은 없습니다.

## 6. 검증/수용 기준(DoD)
- [x] 프롬프트가 generic 품목명보다 쇼핑몰 세부 품목명과 핵심 query 생성을 더 강하게 유도한다.
- [x] 감지 item 중심 보조 query 가 생성된다.
- [x] 네이버 후보 정렬이 brand/family/intent mismatch 를 더 강하게 반영한다.
- [x] 관련 테스트와 README/TODO/PLAN/TASK 문서가 최신 상태다.

## 7. 변경 이력
- 2026-05-10: PLAN 생성.
- 2026-05-10: AI 프롬프트 강화, 감지 item 중심 보조 query, 네이버 후보 정렬 penalty, 추천 exact match 세분화를 적용함.
