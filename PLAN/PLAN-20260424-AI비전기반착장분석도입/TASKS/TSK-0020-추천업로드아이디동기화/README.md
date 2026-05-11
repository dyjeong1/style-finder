---
id: TSK-0020-추천업로드아이디동기화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-29
---

## 목적
새 이미지를 업로드하거나 최근 업로드를 다시 선택했을 때 추천 페이지가 항상 최신 `uploaded_image_id` 기준으로 결과를 조회하도록 동기화 흐름을 정리하고, 이전 업로드의 외부 상품 후보가 다음 추천 fallback에 재사용되지 않도록 저장소 범위를 분리한다.

## 작업 내역
- [x] 업로드 후 추천 이동 시 `uploaded_image_id`를 URL에 명시
- [x] 추천 페이지에서 URL 우선 초기화 로직 추가
- [x] 이전 외부 상품 후보가 기본 fallback 추천에 섞이지 않도록 저장소 분리
- [x] 회귀 테스트 추가
- [x] README/TODO/PLAN 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/(main)/recommendations/page.tsx`
- `backend/src/services/store.py`
- `backend/tests/test_store_color_matching.py`
- `frontend/README.md`
- `backend/README.md`
- `README.md`
- `TODO.md`

## 테스트/검증
- `cd frontend && npm run build`
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_store_color_matching.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 의존성/리스크
- 추천 fallback이 사용자별 최근 외부 상품을 섞어 쓰지 않도록 기본 샘플 카탈로그와 등록 상품 카탈로그를 분리해야 한다.
- 기존 localStorage 기반 복구 흐름과 충돌하지 않도록 URL 우선 규칙을 명확히 유지해야 한다.

## 완료 기준(DoD)
- [x] 새 업로드마다 추천 페이지가 최신 업로드 기준으로 열린다.
- [x] 최근 업로드 재사용도 동일하게 최신 ID를 URL에 싣는다.
- [x] 이전 업로드에서 등록한 외부 상품이 기본 fallback 추천에 다시 섞이지 않는다.
- [x] 회귀 테스트가 통과한다.
- [x] 문서와 루트 TODO가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
