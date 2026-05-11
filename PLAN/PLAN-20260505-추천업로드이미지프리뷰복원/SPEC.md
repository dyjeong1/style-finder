---
id: PLAN-20260505-추천업로드이미지프리뷰복원
title: 추천 업로드 이미지 프리뷰 복원 스펙
status: ready
priority: P1
created_at: 2026-05-05
updated_at: 2026-05-05
related:
  plan:
    - PLAN-20260505-추천업로드이미지프리뷰복원
  tasks:
    - TSK-0001-추천업로드이미지프리뷰복원
tags:
  - frontend
  - recommendations
  - upload
---

## 1. 요구사항
1. 추천 상단 업로드 프리뷰는 가능하면 실제 업로드 원본을 보여줘야 한다.
2. 추천 상단 프리뷰와 확대 모달은 같은 이미지 소스를 사용해야 한다.
3. 상단 `추천` 메뉴를 눌렀을 때 마지막 `uploaded_image_id`가 있으면 `/recommendations?uploaded_image_id=...`로 이동해야 한다.
4. 백엔드 `/images/{uploaded_image_id}/file` 응답이 실패해도 브라우저에 저장된 최근 업로드 원본이 있으면 이를 우선 보여줘야 한다.

## 2. 상태 관리 규칙
- 최근 업로드 저장소 레코드는 로컬 ID와 별개로 최신 `uploaded_image_id`를 보관할 수 있어야 한다.
- 추천 페이지는 현재 `uploaded_image_id` 기준으로 저장소에서 업로드 원본을 다시 찾는다.
- 로컬 객체 URL은 새 업로드 ID로 전환되거나 컴포넌트가 unmount 될 때 revoke 한다.

## 3. UI/UX 규칙
- 프리뷰 버튼 레이아웃과 모달 UI는 기존 디자인을 유지한다.
- 추천 메뉴 링크는 업로드 ID가 없을 때만 기존 `/recommendations` 기본 경로를 사용한다.
- 프리뷰를 복원할 수 없을 때만 기존 fallback 썸네일을 사용한다.

## 4. 검증 시나리오
- 업로드 완료 후 추천 상단 프리뷰 이미지가 실제로 보인다.
- 백엔드 이미지 파일 경로를 실패시키더라도 프리뷰와 모달이 blob 기반 업로드 이미지를 표시한다.
- 업로드 후 `업로드`로 이동했다가 상단 `추천` 메뉴를 누르면 같은 `uploaded_image_id`가 붙은 URL로 돌아간다.
