---
id: PLAN-20260420-프론트폰트단위pt전환
title: 프론트 폰트 단위 pt 전환 스펙
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  plan: [PLAN-20260420-프론트폰트단위pt전환]
  tasks: [TSK-0001-글로벌폰트단위pt정리]
tags: [frontend, typography, style]
---

## 1. 목표
- 프론트 전역 폰트 크기를 `pt` 기준으로 통일하고, 업로드 화면 메인 타이틀을 `36pt`로 반영한다.

## 2. 기능 스펙
- `frontend/app/globals.css`의 `font-size` 선언을 `pt` 단위로 변환한다.
- 업로드 화면 타이틀인 `.upload-stage-copy h1`은 `36pt`로 고정한다.
- 모바일 구간에서도 업로드 타이틀은 `36pt` 기준을 유지한다.

## 3. 비기능 스펙
- 기존 타이포 위계는 최대한 유지하되 단위만 `pt`로 정리한다.
- 빌드 오류 없이 정적 페이지 생성이 가능해야 한다.

## 4. 검증 스펙
- `cd frontend && npm run build`
- `/upload`에서 타이틀이 기존보다 작아졌는지 확인
