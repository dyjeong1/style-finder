---
id: TSK-0001-품목명세분화
plan_id: PLAN-20260424-품목세분화및비전재정렬
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
카테고리 검색 힌트가 `상의/하의` 수준을 넘어서 실제 쇼핑 검색에 가까운 품목명으로 생성되도록 개선한다.

## 작업 내역
- [x] 카테고리별 세부 품목명 규칙 추가
- [x] 감지 아이템 구조화 응답 추가
- [x] 관련 테스트 보강

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/src/services/store.py`
  - `backend/src/api/routes/upload.py`
  - `frontend/lib/api.ts`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_api_e2e.py backend/tests/test_api_failures.py -q`
- `cd frontend && npm run build`

## 의존성/리스크
- 이미지별 형태 추론이 제한적이라 일부 카테고리는 보수적 기본 품목명으로 fallback할 수 있다.

## 완료 기준(DoD)
- [x] 카테고리별 검색 힌트에 세부 품목명이 포함된다.
- [x] 구조화된 감지 아이템 응답이 추가된다.
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
