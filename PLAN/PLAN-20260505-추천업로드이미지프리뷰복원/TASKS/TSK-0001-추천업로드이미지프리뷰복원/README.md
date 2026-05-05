---
id: TSK-0001-추천업로드이미지프리뷰복원
plan_id: PLAN-20260505-추천업로드이미지프리뷰복원
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-05
---

## 목적
추천 상단 업로드 썸네일과 확대 보기 모달이 실제 업로드 이미지를 안정적으로 표시하고, 상단 `추천` 메뉴 재진입 시 마지막 업로드 기준이 유지되게 한다.

## 작업 내역
- [x] 최근 업로드 저장소에 `uploaded_image_id` 매핑 추가
- [x] 상단 `추천` 메뉴의 마지막 업로드 ID 유지
- [x] 추천 프리뷰/모달의 실제 업로드 이미지 복원
- [x] 프론트 빌드와 기존 Playwright smoke 재검증

## 산출물(Artifacts)
- `frontend/lib/recent-upload-store.ts`
- `frontend/components/app-shell.tsx`
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/e2e/core-flow.spec.ts`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd frontend && npm run build`
- `cd frontend && npm run test:e2e -- --grep "@smoke 업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"`
- 프론트 `next start` 프로세스를 최신 빌드로 재시작 후 `http://127.0.0.1:3000/upload` 응답 확인

## 의존성/리스크
- 기존 최근 업로드 데이터에는 `uploaded_image_id`가 없을 수 있어 fallback 경로가 필요하다.
- 객체 URL revoke 누락 시 메모리 누수가 생길 수 있다.

## 완료 기준(DoD)
- [x] 추천 상단 프리뷰가 실제 업로드 이미지를 표시한다.
- [x] 상단 `추천` 메뉴가 마지막 `uploaded_image_id`를 유지한다.
- [x] 확대 모달에서도 같은 업로드 이미지가 보인다.
- [x] 유닛/통합 또는 E2E 검증 통과
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
