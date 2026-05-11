---
id: PLAN-20260421-업로드안내및최근기록정리
title: 업로드 안내 및 최근 기록 정리 스펙
status: done
priority: P2
created_at: 2026-04-21
updated_at: 2026-04-21
related:
  plan: [PLAN-20260421-업로드안내및최근기록정리]
  tasks: [TSK-0001-형식안내및최근업로드삭제]
tags: [frontend, upload, history]
---

## 1. 목표
- 업로드 placeholder 자리에 허용 형식을 노출한다.
- 최근 업로드 카드를 개별 삭제할 수 있게 한다.
- 헤더에서 `Local Mode` 문구가 보이지 않는 상태를 유지한다.

## 2. 기능 스펙
- 파일이 선택되지 않았을 때 정사각형 placeholder에 `PNG, JPG, JPEG, WEBP` 문구를 노출한다.
- 최근 업로드 카드마다 `삭제` 버튼을 제공한다.
- 삭제 시 localStorage의 업로드 기록에서 해당 항목을 제거한다.
- 삭제 대상이 현재 저장된 업로드 ID와 같으면 관련 localStorage 상태도 함께 비운다.

## 3. 비기능 스펙
- 최근 업로드 카드의 재사용 버튼과 삭제 버튼이 서로 오작동하지 않아야 한다.
- 빌드 오류 없이 정적 페이지 생성이 가능해야 한다.

## 4. 검증 스펙
- `cd frontend && npm run build`
- `/upload`에서 허용 형식 문구, 카드 삭제 버튼, 헤더 상태 확인
