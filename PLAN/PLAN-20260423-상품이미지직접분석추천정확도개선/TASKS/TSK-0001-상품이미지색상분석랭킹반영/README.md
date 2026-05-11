---
id: TSK-0001-상품이미지색상분석랭킹반영
plan_id: PLAN-20260423-상품이미지직접분석추천정확도개선
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
네이버 상품 이미지 자체의 대표 색상을 분석해 업로드 이미지와 더 직접적으로 비교한다.

## 작업 내역
- [x] 공용 이미지 색상 분석 유틸 분리
- [x] 네이버 상품 이미지 다운로드/분석 추가
- [x] 상품 이미지 색상 보너스 추가
- [x] 프론트 매칭 정보 표시 보강
- [x] 테스트와 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/src/services/store.py`
  - `backend/src/core/config.py`
  - `backend/src/api/routes/recommendation.py`
  - `frontend/lib/api.ts`
  - `frontend/app/(main)/recommendations/page.tsx`
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
- 외부 이미지 다운로드가 실패하면 fallback이 동작한다.
- 상품 이미지 분석은 응답 시간에 영향을 줄 수 있어 timeout/용량/시도 개수 제한을 둔다.

## 완료 기준(DoD)
- [x] 상품 이미지 대표 색상 분석
- [x] 추천 점수 반영
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
