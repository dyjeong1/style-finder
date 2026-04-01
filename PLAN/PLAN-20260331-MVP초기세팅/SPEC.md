---
id: SPEC-PLAN-20260331-MVP초기세팅
title: 스타일매치 MVP 초기 세팅 기술 스펙
status: ready
priority: P1
created_at: 2026-03-31
updated_at: 2026-03-31
related:
  plan: [PLAN-20260331-MVP초기세팅]
  tasks: [TSK-0001-저장소구조세팅, TSK-0002-아키텍처초안정의]
tags: [spec, mvp, architecture]
---

## 1. 목적
스타일매치 MVP 구현을 시작하기 전에 필수 저장소 구조와 기술 기준을 고정해 개발 일관성을 확보합니다.

## 2. 기능 스펙(초안)
- 이미지 업로드 API(단일 이미지)
- 패션 아이템 카테고리 분류(상의/하의/아우터/신발/가방)
- 유사 상품 조회 API(지그재그/29CM 소스 추상화)
- 결과 정렬(유사도순)
- 가격 필터(min/max)
- 찜 추가/조회/삭제

## 3. 비기능 스펙(초안)
- 응답시간: 추천 결과 조회 p95 2.5s 이내(초기 목표)
- 안정성: 에러 응답 포맷 표준화
- 보안: Private 접근 제어, 이미지 접근권한 체크
- 관측성: API 요청 로그/오류 로그 기본 수집

## 4. 모듈 경계(초안)
- `frontend-web`: 업로드/결과/찜 UI
- `backend-api`: 인증, 업로드, 추천, 찜 API
- `recommendation-engine`: 임베딩/유사도 계산/랭킹
- `data-access`: 상품/사용자/추천결과 저장소 접근

## 5. 수용 기준
- [x] PLAN 대비 TASK 2개 이상 분해
- [x] 각 TASK의 README/TODO 생성
- [x] 루트 README에 개발 착수 섹션 반영
- [x] API 명세 초안(OpenAPI) 작성
- [x] 데이터 스키마 초안(DDL) 작성
- [ ] 다음 PLAN에서 API 상세 스펙(OpenAPI) 고도화
