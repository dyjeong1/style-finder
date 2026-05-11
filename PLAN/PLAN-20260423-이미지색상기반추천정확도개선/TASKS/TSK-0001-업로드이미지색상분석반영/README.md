---
id: TSK-0001-업로드이미지색상분석반영
plan_id: PLAN-20260423-이미지색상기반추천정확도개선
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
업로드 이미지의 실제 주요 색상을 추천 검색어와 추천 점수에 반영해 체감 정확도를 높인다.

## 작업 내역
- [x] 업로드 이미지 색상 분석 추가
- [x] 분석 결과/응답에 주요 색상 필드 추가
- [x] 네이버 검색어 색상 키워드 반영
- [x] 추천 점수 색상 보너스 추가
- [x] 프론트 분석/매칭 정보 색상 표시
- [x] 테스트와 문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/store.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/src/api/routes/upload.py`
  - `backend/pyproject.toml`
  - `frontend/lib/api.ts`
  - `frontend/app/(main)/upload/page.tsx`
  - `frontend/app/(main)/recommendations/page.tsx`
  - `backend/tests/test_api_e2e.py`
  - `backend/tests/test_naver_shopping.py`
  - `backend/tests/test_store_color_matching.py`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 통과
- `cd frontend && npm run build` 통과

## 의존성/리스크
- Pillow가 없는 환경에서도 기존 fallback이 동작한다.
- 상품 이미지 자체를 분석하지 않으므로 색상 기반 1차 개선으로 한정한다.

## 완료 기준(DoD)
- [x] 주요 색상이 업로드 분석에 포함된다.
- [x] 자동 검색어에 주요 색상이 반영된다.
- [x] 추천 점수에 색상 보너스가 포함된다.
- [x] 백엔드 테스트 통과
- [x] 프론트 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
