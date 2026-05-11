---
id: TSK-0023-이전추천응답및고정시그니처차단
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-04-29
---

## 목적
새 이미지를 업로드했는데도 이전 이미지의 추천 검색어가 화면에 다시 표시되는 문제를 막고, 규칙 기반 분석기가 특정 레이어드 코디 키워드를 과도하게 재사용하지 않도록 보정합니다.

## 작업 내역
- [x] 이전 추천 API 응답이 늦게 도착해 새 업로드 화면 상태를 덮어쓰지 않도록 요청 키 검증 추가
- [x] 레이어드 베스트 특수 규칙이 컬러 의상에서도 고정 키워드를 반환하지 않도록 색상 오염 조건 추가
- [x] 컬러 의상에서 `블랙 니트 베스트`, `브라운 메리제인 슈즈` 고정 키워드가 반복되지 않는 회귀 테스트 추가
- [x] 프론트 빌드 및 백엔드 테스트 검증

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `backend/src/services/image_analysis.py`
- `backend/tests/test_outfit_query_hints.py`

## 테스트/검증
- `cd frontend && npm run build`
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_outfit_query_hints.py -q`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 의존성/리스크
- 규칙 기반 분석은 여전히 실제 AI 비전보다 약하므로, provider가 꺼져 있으면 품목 정확도는 제한적입니다.

## 완료 기준(DoD)
- [x] 이전 업로드의 늦은 추천 응답이 새 업로드 결과를 덮어쓰지 않는다.
- [x] 컬러 의상에서 레이어드 베스트 특수 키워드가 반복되지 않는다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료
