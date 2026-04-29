---
id: TSK-0027-추천분석동기화회귀수정
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-29
---

## 목적
추천 페이지에서 다른 이미지를 업로드해도 이전 로컬 분석 요약과 검색 힌트가 남아 검색어가 바뀌지 않는 것처럼 보이는 회귀를 수정한다.

## 작업 내역
- [x] 추천 API 응답에 업로드 분석 요약 포함
- [x] 추천 페이지가 추천 응답 기준으로 업로드 분석/히스토리를 다시 동기화하도록 수정
- [x] 테스트와 문서 갱신

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/src/api/routes/upload.py`
- `backend/src/api/routes/recommendation.py`
- `backend/tests/test_api_e2e.py`
- `frontend/lib/api.ts`
- `frontend/app/(main)/recommendations/page.tsx`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_api_e2e.py tests/test_api_failures.py tests/test_vision_outfit_analyzer.py tests/test_vision_dataset_evaluator.py tests/test_naver_shopping.py -q`
- `cd frontend && npm run build`

## 의존성/리스크
- 프론트는 로컬스토리지 히스토리를 계속 사용하므로, 서버 응답으로 덮어쓰지 않으면 오래된 분석값이 다시 노출될 수 있다.
- 브라우저 E2E는 현재 업로드 파일 입력 시뮬레이션 하네스가 불안정해 별도 보강이 필요하다.

## 완료 기준(DoD)
- [x] 추천 API 응답이 업로드 분석 요약을 함께 반환함
- [x] 추천 페이지가 서버 응답 기준으로 업로드 분석/검색 힌트를 갱신함
- [x] 백엔드 테스트 통과
- [x] 프론트 빌드 통과
- [x] README/TODO/PLAN 문서 갱신
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
