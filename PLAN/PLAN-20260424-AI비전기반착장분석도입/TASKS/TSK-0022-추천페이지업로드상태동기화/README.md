---
id: TSK-0022-추천페이지업로드상태동기화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-29
---

## 목적
다른 이미지를 업로드하거나 최근 업로드를 재사용했을 때 추천 페이지가 이전 이미지의 검색어/분석 상태를 재사용하지 않도록 URL의 `uploaded_image_id`와 화면 상태를 동기화합니다.

## 작업 내역
- [x] 추천 페이지가 `uploaded_image_id` URL 파라미터 변경을 계속 반영하도록 수정
- [x] 업로드 ID 변경 시 이전 검색어, 직접 입력 검색어, 필터, 결과 목록을 초기화
- [x] 업로드 히스토리에서 ID에 맞는 분석 요약을 찾아 localStorage 분석과 화면 요약을 동기화
- [x] 프론트 빌드 및 관련 테스트 검증

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 추천 페이지가 같은 경로에서 쿼리 파라미터만 바뀌는 경우에도 새 업로드 기준으로 재조회해야 합니다.

## 완료 기준(DoD)
- [x] 새 업로드 ID가 들어오면 이전 이미지 검색어가 남지 않는다.
- [x] 직접 입력 검색어가 새 이미지에 자동 재사용되지 않는다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료
