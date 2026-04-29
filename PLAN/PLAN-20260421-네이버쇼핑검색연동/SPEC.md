---
id: PLAN-20260421-네이버쇼핑검색연동-SPEC
title: 네이버 쇼핑 검색 연동 스펙
status: done
priority: P1
created_at: 2026-04-21
updated_at: 2026-04-21
related:
  plan: [PLAN-20260421-네이버쇼핑검색연동]
tags: [backend, spec, naver]
---

## 1. 목적
- 업로드 이미지 분석 결과를 검색어로 변환해 네이버 쇼핑 검색 API에서 실제 상품 후보를 가져온다.

## 2. 구현 범위
- 설정
  - `NAVER_SHOPPING_CLIENT_ID`
  - `NAVER_SHOPPING_CLIENT_SECRET`
  - `NAVER_SHOPPING_DISPLAY`
  - `NAVER_SHOPPING_TIMEOUT_SECONDS`
- 백엔드
  - 네이버 쇼핑 검색 클라이언트 추가
  - 추천 API에서 네이버 상품 후보 조회 후 점수화
  - 네이버 상품을 내부 저장소에 등록해 위시리스트 동작 유지
- fallback
  - 키 없음, API 실패, 빈 결과면 기존 목데이터 사용

## 3. 비범위
- 어필리에이트/딥링크 API
- 구매 전환 트래킹
- 네이버 API 키 발급 자동화

## 4. 검증 방법
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
- 네이버 키 없이 기존 추천 테스트가 통과하는지 확인
