---
id: SPEC-PLAN-20260422-최근업로드실제썸네일
title: 최근 업로드 실제 썸네일 스펙
status: done
priority: P1
created_at: 2026-04-22
updated_at: 2026-04-22
related:
  plan: PLAN-20260422-최근업로드실제썸네일
  tasks: [TSK-0001-업로드기록썸네일저장]
tags: [frontend, upload, thumbnail]
---

## 목표
업로드 직후 브라우저에서 작은 정사각 썸네일을 생성해 최근 업로드 히스토리에 저장하고, 최근 업로드 카드에 실제 업로드 이미지를 표시한다.

## 프론트 스펙
- `UploadHistoryItem`에 선택 필드 `thumbnail_url`을 추가한다.
- 업로드 성공 후 원본 파일을 캔버스에 그려 최대 360px 정사각 JPEG data URL로 변환한다.
- 최근 업로드 이미지는 `thumbnail_url` → `image_url` → fallback SVG 순서로 표시한다.
- 썸네일 생성 실패 시 기존 fallback 흐름을 유지한다.

## 검증
- `cd frontend && npm run build` → 성공
- 새 업로드 후 최근 업로드 카드 이미지가 실제 업로드 이미지로 보이는지 브라우저에서 확인한다.
