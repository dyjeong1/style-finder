---
id: PLAN-20260420-프론트로컬실행안정화
title: 프론트 로컬 실행 안정화 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-프론트로컬실행안정화]
  tasks: [TSK-0001-안정실행스크립트추가]
tags: [frontend, local, script]
---

## 1. 목표
- 개발용 `next dev` 대신 사용자가 바로 실행 가능한 안정 경로를 제공한다.

## 2. 기능 스펙
- `frontend/package.json`에 프로덕션 빌드 후 고정 호스트/포트로 실행하는 스크립트를 추가한다.
- 문서에서 기본 확인 경로를 `npm run local`로 안내한다.
- `127.0.0.1:3000` 기준으로 `/upload`, `/recommendations`, `/wishlist` 응답을 확인한다.

## 3. 비기능 스펙
- 사용자 입력 없이 한 줄 명령으로 실행 가능해야 한다.
- 기존 `npm run dev`는 유지하되, 기본 권장 경로는 안정 실행 스크립트로 옮긴다.

## 4. 검증 스펙
- `cd frontend && npm run build`
- `cd frontend && npm run local`
- `curl -I http://127.0.0.1:3000/upload`
- `curl -I http://127.0.0.1:3000/recommendations`
- `curl -I http://127.0.0.1:3000/wishlist`
