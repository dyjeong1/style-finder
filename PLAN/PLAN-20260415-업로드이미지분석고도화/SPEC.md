---
id: SPEC-PLAN-20260415-업로드이미지분석고도화
title: 업로드 이미지 분석 고도화 스펙
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  plan: [PLAN-20260415-업로드이미지분석고도화]
  tasks: [TSK-0001-백엔드이미지분석및점수고도화]
tags: [backend, upload, recommendation]
---

## 1. 목적
업로드 이미지에서 feature vector와 분석 요약을 생성하고, 추천 점수 계산에 반영합니다.

## 2. 기능 스펙
- 업로드 시 이미지 바이트 기반 deterministic 분석 결과 생성
- 업로드 레코드에 vector/style summary 저장
- 상품별 mock vector와 메타데이터를 기반으로 similarity score 계산
- 업로드 응답 및 추천 응답에 설명용 필드 추가

## 3. 비기능 스펙
- 기존 로그인/업로드/추천/찜 API 흐름은 유지
- 테스트는 deterministic 해야 함

## 4. 구현 스펙
- 대상 파일:
  - `backend/src/services/store.py`
  - `backend/src/api/routes/upload.py`
  - `backend/tests/test_api_e2e.py`
  - `backend/tests/test_api_failures.py`

## 5. 수용 기준
- [x] 업로드 분석 필드 추가
- [x] 추천 점수 계산 고도화
- [x] 테스트 통과
