---
id: TSK-0005-악세서리품목세분화
plan_id: PLAN-20260424-카테고리오탐억제및아우터정교화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
악세서리를 `안경`, `모자`, `머플러`, `귀걸이` 수준으로 더 정밀하게 구분한다.

## 작업 내역
- [x] 악세서리 품목 규칙 세분화
- [x] 회귀 테스트 추가
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/tests/test_outfit_query_hints.py`

## 테스트/검증
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_naver_shopping.py backend/tests/test_api_e2e.py backend/tests/test_api_failures.py -q`
- `cd frontend && npm run build`

## 완료 기준(DoD)
- [x] 안경/모자/머플러/귀걸이 구분 보강
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신

## 완료 메모
- 모자/귀걸이 실사형 픽스처를 추가하고 악세서리 색상-품목 추론 규칙을 보강했다.
- 상의와 같은 색상의 악세서리도 유지되도록 accessory reference color 억제 규칙을 조정했다.
