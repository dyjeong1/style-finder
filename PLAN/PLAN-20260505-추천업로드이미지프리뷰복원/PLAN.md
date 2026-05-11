---
id: PLAN-20260505-추천업로드이미지프리뷰복원
title: 추천 업로드 이미지 프리뷰 복원
status: done
priority: P1
created_at: 2026-05-05
updated_at: 2026-05-05
related:
  tasks:
    - TSK-0001-추천업로드이미지프리뷰복원
tags:
  - frontend
  - recommendations
  - upload
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 추천 화면은 현재 어떤 업로드 이미지를 기준으로 상품을 추천하는지 즉시 보여줘야 한다.
- 현재 성능/운영 이슈: 상단 `추천` 메뉴가 `uploaded_image_id` 없이 `/recommendations`로 이동하고, 추천 상단 썸네일도 백엔드 이미지 파일 경로에만 의존해 실제 업로드 이미지가 placeholder로 보이는 회귀가 발생했다.

## 2. 목표/가설
- 1차 지표(Primary): 추천 상단 썸네일이 실제 업로드 이미지를 안정적으로 보여준다.
- 2차 지표(Secondary): 추천 메뉴를 다시 눌러도 마지막 업로드 기준이 유지된다.
- 가설: 최근 업로드 브라우저 저장소에 `uploaded_image_id` 매핑을 함께 저장하고, 추천 메뉴/프리뷰가 이를 재사용하면 이미지 파일 경로 실패와 쿼리 유실 회귀를 함께 줄일 수 있다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - 최근 업로드 저장소에 `uploaded_image_id` 메타데이터 추가
  - 상단 `추천` 메뉴의 마지막 업로드 ID 유지
  - 추천 프리뷰와 확대 모달의 실제 업로드 이미지 복원
  - 관련 Playwright 회귀 테스트 추가
- 제외 범위:
  - 업로드 분석 결과 영속 저장
  - 서버 측 업로드 이력 관리 확장
- 산출물(코드/모델/대시보드/문서):
  - `frontend/lib/recent-upload-store.ts`
  - `frontend/components/app-shell.tsx`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/e2e/core-flow.spec.ts`
  - 관련 PLAN/TASK/README/TODO 문서

## 4. 일정/마일스톤
- M1(원인 확인): 2026-05-05
- M2(프리뷰 복원 구현): 2026-05-05
- M3(메뉴 유지 및 회귀 테스트): 2026-05-05
- M4(문서/커밋 마감): 2026-05-05

## 5. 리스크 & 가정
- 데이터 품질/지연/누락: 과거에 저장된 최근 업로드에는 `uploaded_image_id` 매핑이 없을 수 있다.
- 시스템/리소스 제약: 브라우저 객체 URL은 화면 전환 시 적절히 revoke 해야 메모리 누수를 줄일 수 있다.
- 보안/개인정보: 업로드 원본은 기존처럼 브라우저 `IndexedDB`에만 저장한다.

## 6. 검증/수용 기준(DoD)
- [x] 추천 상단 프리뷰가 실제 업로드 이미지로 표시된다.
- [x] 상단 `추천` 메뉴를 다시 눌러도 마지막 `uploaded_image_id`가 유지된다.
- [x] 확대 보기 모달에서도 같은 실제 업로드 이미지를 확인할 수 있다.
- [x] README/TODO/TASK 문서와 검증 기록이 최신 상태다.

## 7. 변경 이력
- 2026-05-05: PLAN 생성.
- 2026-05-05: 최근 업로드 저장소에 `uploaded_image_id` 매핑을 추가하고, 추천 메뉴/프리뷰가 브라우저 저장소 원본을 우선 복원하도록 연결함.
- 2026-05-05: `npm run build`와 기존 Playwright smoke 재검증을 통과하고 오래된 프론트 프로세스를 최신 빌드로 재시작함.
