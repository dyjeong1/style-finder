---
id: TSK-0001-네이버카테고리분산조회
plan_id: PLAN-20260422-추천카테고리다양화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-22
---

## 목적
추천 전체 보기에서 네이버 쇼핑 후보가 한 카테고리에만 쏠리지 않도록 카테고리별 검색을 분산 수행한다.

## 작업 내역
- [x] 전체 추천 카테고리 순서/검색어 생성 추가
- [x] 카테고리별 네이버 검색 결과 합치기 및 중복 제거
- [x] 응답 query/fallback 처리 유지
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/api/routes/recommendation.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/tests/test_naver_shopping.py`
- 문서:
  - `README.md`
  - `TODO.md`
  - `backend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` → 12 passed
- `cd frontend && npm run build` → 성공

## 의존성/리스크
- 네이버 API 호출 수가 늘어날 수 있다.
- 특정 검색어에서 결과가 적으면 일부 카테고리 결과가 적게 보일 수 있다.

## 완료 기준(DoD)
- [x] 전체 추천에서 다양한 카테고리 후보가 조회된다.
- [x] 단일 카테고리 필터 동작이 유지된다.
- [x] 테스트/빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
