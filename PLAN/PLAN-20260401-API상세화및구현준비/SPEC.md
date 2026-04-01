---
id: SPEC-PLAN-20260401-API상세화및구현준비
title: API 상세화 및 구현 준비 스펙
status: ready
priority: P1
created_at: 2026-04-01
updated_at: 2026-04-01
related:
  plan: [PLAN-20260401-API상세화및구현준비]
  tasks: [TSK-0001-OpenAPI상세화, TSK-0002-DB마이그레이션초안작성, TSK-0003-백엔드스캐폴딩]
tags: [spec, api, database, scaffold]
---

## 1. 목적
MVP 구현 시작 전, API 계약과 DB 스키마를 구현 가능한 수준으로 상세화하고 백엔드 코드 구조를 준비합니다.

## 2. 기능 스펙
- 인증: 로그인/토큰 검증/권한 에러 표준화
- 업로드: 이미지 업로드와 메타데이터 저장
- 추천: 카테고리/가격 필터/정렬 파라미터
- 찜: 추가/조회/삭제 API

## 3. 비기능 스펙
- API 응답 포맷 통일(`data`, `error`, `meta`)
- 에러 코드 표준(`AUTH_*`, `VALIDATION_*`, `RECOMMENDATION_*`)
- 관측성: 요청 ID, 에러 로그 기본 수집

## 4. 구현 스펙
- OpenAPI 파일 경로: `docs/openapi/openapi.yaml`
- DB 마이그레이션 경로: `backend/migrations/`
- 백엔드 모듈 경로: `backend/src/api/routes/{auth,upload,recommendation,wishlist,health}.py`
- 공통 모듈 경로: `backend/src/core/{config,logger,errors}.py`
- 실행 설정: `backend/pyproject.toml`, `backend/scripts/run-dev.sh`

## 5. 수용 기준
- [x] OpenAPI 상세 스키마 작성
- [x] DB 마이그레이션 파일 1차 작성
- [x] 백엔드 스캐폴딩 구조 생성
- [x] 루트 README/TODO 반영
