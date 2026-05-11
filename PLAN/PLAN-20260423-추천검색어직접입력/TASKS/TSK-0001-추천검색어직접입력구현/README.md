---
id: TSK-0001-추천검색어직접입력구현
plan_id: PLAN-20260423-추천검색어직접입력
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
추천 결과가 원하는 방향과 다를 때 사용자가 직접 검색어를 입력해 추천 후보를 재조회할 수 있게 한다.

## 작업 내역
- [x] 백엔드 `custom_query` 파라미터 추가
- [x] 직접 입력 검색어 기반 네이버 쿼리 생성 함수 추가
- [x] 프론트 검색어 입력/적용/초기화 UI 추가
- [x] 테스트와 문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/api/routes/recommendation.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/tests/test_naver_shopping.py`
  - `backend/tests/test_api_failures.py`
  - `frontend/lib/api.ts`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `frontend/app/globals.css`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 성공
- `cd frontend && npm run build` 성공

## 의존성/리스크
- 네이버 API 키가 없거나 실패하면 기존처럼 샘플 데이터 fallback을 유지한다.
- 직접 입력 검색어는 검색 결과 품질을 사용자가 보정하는 용도이며, 이미지 분석 자체를 대체하지 않는다.

## 완료 기준(DoD)
- [x] 추천 API가 직접 입력 검색어를 받는다.
- [x] 프론트에서 직접 검색어 적용/초기화가 가능하다.
- [x] 백엔드 테스트 통과
- [x] 프론트 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
