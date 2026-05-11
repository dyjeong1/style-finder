---
id: PLAN-20260420-위시리스트영속저장
title: 위시리스트 영속 저장 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-위시리스트영속저장]
  tasks: [TSK-0001-백엔드찜목록파일저장]
tags: [backend, persistence]
---

## 1. 목표
- 위시리스트를 메모리 외에 로컬 파일로도 저장해 백엔드 재시작 후 복원한다.

## 2. 기능 스펙
- store 초기화 시 위시리스트 JSON 파일이 있으면 로드한다.
- `add_wishlist`, `remove_wishlist` 호출 후 파일에 즉시 저장한다.
- 파일이 없거나 파싱에 실패하면 빈 상태로 안전하게 시작한다.
- 저장 포맷은 `user_id -> product_id -> created_at` 맵 구조를 유지한다.

## 3. 비기능 스펙
- 디렉터리가 없으면 자동 생성한다.
- 파일 쓰기는 UTF-8 JSON으로 저장한다.
- 테스트는 임시 파일 경로를 사용해 실제 로컬 데이터와 분리한다.

## 4. 검증 스펙
- 추가 후 파일 생성 확인
- 재초기화 후 기존 위시리스트 복구 확인
- 삭제 후 파일 동기화 확인
