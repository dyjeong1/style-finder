---
id: SPEC-PLAN-20260401-핵심API로직구현
title: 핵심 API 로직 구현 스펙
status: review
priority: P1
created_at: 2026-04-01
updated_at: 2026-04-01
related:
  plan: [PLAN-20260401-핵심API로직구현]
  tasks: [TSK-0001-인증로직구현, TSK-0002-업로드로직구현, TSK-0003-추천찜로직구현]
tags: [auth, upload, recommendation, wishlist]
---

## 1. 목적
FastAPI 스캐폴딩 위에 사용자 시나리오가 동작하는 핵심 API 비즈니스 로직을 구현합니다.

## 2. 기능 스펙
- 로그인: 이메일/비밀번호 검증, bearer 토큰 발급
- 업로드: 이미지 파일 업로드 및 업로드 이력 저장
- 추천: 업로드 이미지 기준 추천 목록 조회(필터/정렬)
- 찜: 추가/조회/삭제

## 3. 비기능 스펙
- 모든 응답 `data/error/meta` 포맷 유지
- HTTPException/Validation 에러를 표준 에러 구조로 변환
- 인메모리 저장소 기반으로 개발 속도 우선

## 4. 구현 스펙
- `backend/src/core/auth.py`: 토큰 인증 의존성
- `backend/src/core/errors.py`: 표준 에러 핸들러
- `backend/src/services/`: 인메모리 저장소 및 도메인 로직
- `backend/src/api/routes/*.py`: 라우트 실제 구현

## 5. 수용 기준
- [x] 로그인 후 보호 API 접근 가능
- [ ] 업로드 ID를 기반으로 추천 조회 가능
- [ ] 찜 추가/조회/삭제 가능
- [ ] 문서 및 TODO 갱신
