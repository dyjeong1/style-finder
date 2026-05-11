---
id: TSK-0001-분석및카테고리감지개선
plan_id: PLAN-20260423-동적업로드분석및카테고리감지
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
업로드 분석과 추천 카테고리가 이미지별로 달라지도록 개선한다.

## 작업 내역
- [x] 배경 제외 foreground 색상 분석
- [x] 이미지 기반 tone/mood/silhouette 산출
- [x] 감지 카테고리만 추천 조회
- [x] accessory 카테고리 추가
- [x] 테스트와 문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/src/services/store.py`
  - `backend/src/services/naver_shopping.py`
  - `frontend/app/(main)/*`
  - `frontend/lib/api.ts`
  - `backend/tests/*`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- 백엔드 테스트: `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_naver_shopping.py backend/tests/test_api_e2e.py -q`
- 프론트 빌드: `cd frontend && npm run build`

## 의존성/리스크
- heuristic 기반이라 복잡한 이미지에서는 정확도가 제한적일 수 있다.

## 완료 기준(DoD)
- [x] 이미지별 업로드 분석 변화
- [x] 없는 카테고리 제외
- [x] accessory 반영
- [x] 테스트 통과
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
