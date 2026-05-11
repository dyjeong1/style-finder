---
id: PLAN-20260506-추천빈업로드프리뷰숨김
title: 추천 빈 업로드 프리뷰 숨김 스펙
status: ready
priority: P1
created_at: 2026-05-06
updated_at: 2026-05-06
related:
  plan:
    - PLAN-20260506-추천빈업로드프리뷰숨김
  tasks:
    - TSK-0001-추천프리뷰조건부노출
tags:
  - frontend
  - recommendations
  - upload
---

## 1. 요구사항
1. 추천 페이지에 업로드 이미지가 없는 상태에서는 상단 프리뷰 카드가 렌더링되지 않아야 한다.
2. 업로드 이미지 분석이 완료되면 상단 프리뷰 카드가 다시 나타나야 한다.
3. 프리뷰 카드가 보이는 상태에서 확대 모달은 기존처럼 클릭으로 열리고 닫혀야 한다.

## 2. 상태 관리 규칙
- 프리뷰 노출 여부는 `uploaded_image_id` 존재 여부만이 아니라 `uploadedImageAnalysis` 준비 상태까지 함께 본다.
- 업로드 전환이나 오류로 `uploadedImageAnalysis`가 비워지면 프리뷰와 확대 모달도 함께 숨긴다.
- 기존 브라우저 저장소 기반 프리뷰 복원 로직은 유지한다.

## 3. 검증 시나리오
- `/recommendations` 단독 진입 시 프리뷰 버튼이 없다.
- 업로드 후 `/recommendations?uploaded_image_id=...`로 이동하고 분석 패널이 보이면 프리뷰 버튼도 보인다.
- 프리뷰 버튼을 클릭하면 확대 모달이 열린다.
