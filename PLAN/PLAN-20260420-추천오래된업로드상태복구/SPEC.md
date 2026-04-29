---
id: PLAN-20260420-추천오래된업로드상태복구
title: 추천 오래된 업로드 상태 복구 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-추천오래된업로드상태복구]
  tasks: [TSK-0001-오래된업로드상태초기화]
tags: [frontend, recovery]
---

## 1. 목표
- 추천 페이지에서 존재하지 않는 `uploaded_image_id`를 감지하면 localStorage 상태를 초기화하고 재업로드를 안내한다.

## 2. 기능 스펙
- 추천 조회 실패 메시지가 stale 업로드 ID 상황과 일치하면 `uploaded_image_id`와 분석 요약을 localStorage에서 제거한다.
- 페이지 상태의 `uploadedImageId`, `uploadedImageAnalysis`도 즉시 초기화한다.
- 오류 문구는 사용자가 이해할 수 있는 한국어 안내로 교체한다.

## 3. 비기능 스펙
- SSR/CSR 정합성을 해치지 않는다.
- 기존 추천 필터와 Saved 상태 흐름을 유지한다.

## 4. 검증 스펙
- 오래된 `uploaded_image_id`가 저장된 상태에서 추천 페이지 진입
- 치명적 예외 없이 안내 문구 노출 확인
- `/upload` 재업로드 후 추천 정상 조회 확인
