---
id: SPEC-PLAN-20260415-로컬개발CORS정리
title: 로컬 개발 CORS 정리 스펙
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  plan: [PLAN-20260415-로컬개발CORS정리]
  tasks: [TSK-0001-백엔드CORS허용추가]
tags: [backend, cors]
---

## 1. 목적
프론트와 백엔드가 서로 다른 포트에서 실행되는 로컬 개발 환경에서 CORS 문제 없이 로그인/업로드를 진행할 수 있게 합니다.

## 2. 기능 스펙
- FastAPI에 CORS 미들웨어 추가
- 허용 origin:
  - `http://localhost:3000`
  - `http://127.0.0.1:3000`
- 인증 헤더와 일반 메서드 허용

## 3. 비기능 스펙
- 기존 API 경로와 응답 형식 유지
- 로컬 개발 환경에 필요한 최소 범위만 허용

## 4. 구현 스펙
- 대상 파일:
  - `backend/src/main.py`
  - PLAN/TASK 문서

## 5. 수용 기준
- [x] preflight 응답 정상
- [x] 로그인 흐름 복구
