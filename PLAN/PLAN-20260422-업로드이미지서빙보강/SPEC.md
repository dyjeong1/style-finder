---
id: SPEC-PLAN-20260422-업로드이미지서빙보강
title: 업로드 이미지 서빙 보강 스펙
status: done
priority: P1
created_at: 2026-04-22
updated_at: 2026-04-22
related:
  plan: PLAN-20260422-업로드이미지서빙보강
  tasks: [TSK-0001-업로드이미지실제응답]
tags: [backend, frontend, upload, thumbnail]
---

## 목표
업로드한 이미지를 백엔드가 실제로 응답하고, 프론트 최근 업로드 카드가 그 URL을 정확히 사용하도록 한다.

## 백엔드 스펙
- `UploadedImageRecord`에 `content: bytes`를 저장한다.
- 업로드 생성 시 `image_url`은 `/images/{upload_id}/file`로 설정한다.
- `GET /images/{upload_id}/file`은 업로드 bytes를 `content_type`과 함께 반환한다.
- 없는 업로드 ID는 404를 반환한다.

## 프론트 스펙
- API가 상대경로 이미지 URL을 반환하면 `API_BASE_URL`을 붙여 절대 URL로 저장한다.
- 최근 업로드 카드는 `thumbnail_url`이 있으면 우선 쓰고, 없으면 정규화된 `image_url`을 사용한다.

## 검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` → 11 passed
- `cd frontend && npm run build` → 성공
