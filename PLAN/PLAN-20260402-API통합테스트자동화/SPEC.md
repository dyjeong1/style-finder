---
id: SPEC-PLAN-20260402-API통합테스트자동화
title: API 통합 테스트 자동화 스펙
status: ready
priority: P1
created_at: 2026-04-02
updated_at: 2026-04-02
related:
  plan: [PLAN-20260402-API통합테스트자동화]
  tasks: [TSK-0001-핵심E2E테스트작성, TSK-0002-실패시나리오테스트확장, TSK-0003-CI테스트워크플로우초안]
tags: [pytest, testclient, e2e]
---

## 1. 목적
핵심 API 사용자 흐름을 자동 테스트로 고정해 회귀를 방지합니다.

## 2. 기능 스펙
- 로그인 성공/실패
- 업로드 성공
- 추천 조회 성공/실패
- 찜 추가/조회/삭제

## 3. 비기능 스펙
- 테스트는 독립적으로 실행 가능해야 함
- 응답 포맷(data/error/meta) 검증 포함

## 4. 구현 스펙
- 테스트 경로: `backend/tests/`
- 테스트 도구: `pytest`, `fastapi.testclient`
- 실행 명령: `pytest backend/tests -q`

## 5. 수용 기준
- [x] 핵심 E2E 테스트 통과
- [x] 실패 시나리오 테스트 추가
- [x] 문서 업데이트 완료
