---
id: PLAN-20260421-최근업로드카드액션정리
title: 최근 업로드 카드 액션 정리 스펙
status: done
priority: P2
created_at: 2026-04-21
updated_at: 2026-04-21
related:
  plan: [PLAN-20260421-최근업로드카드액션정리]
  tasks: [TSK-0001-삭제아이콘및형식문구조정]
tags: [frontend, upload, ui]
---

## 1. 목표
- 최근 업로드 카드 삭제 버튼을 카드 내부 우측 상단 아이콘으로 정리한다.
- placeholder 문구를 `허용 이미지: PNG, JPG, JPEG, WEBP`로 수정한다.

## 2. 기능 스펙
- 최근 업로드 카드는 재사용 클릭 영역을 유지한다.
- 삭제 버튼은 카드 내부 우측 상단에 위치한 원형 `x` 아이콘 버튼으로 렌더링한다.
- 삭제 버튼 클릭은 카드 재사용 동작과 분리되어야 한다.
- 업로드 placeholder에는 `허용 이미지: PNG, JPG, JPEG, WEBP` 문구를 노출한다.

## 3. 비기능 스펙
- 아이콘 버튼은 마우스와 키보드로 모두 접근 가능해야 한다.
- 빌드 오류 없이 정적 페이지 생성이 가능해야 한다.

## 4. 검증 스펙
- `cd frontend && npm run build`
- `/upload`에서 카드 삭제 아이콘 위치와 placeholder 문구 확인
