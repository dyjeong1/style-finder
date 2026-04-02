---
id: TSK-0001-핵심E2E테스트작성
plan_id: PLAN-20260402-API통합테스트자동화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-02
---

## 목적
로그인→업로드→추천→찜의 핵심 흐름을 하나의 E2E 테스트로 자동화합니다.

## 작업 내역
- [x] 테스트 의존성 추가
- [x] 핵심 E2E 테스트 코드 작성
- [x] 테스트 실행 및 결과 확인

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/tests/test_api_e2e.py`
  - `backend/pyproject.toml`

## 테스트/검증
- `PYTHONPATH=. python3 -m pytest tests -q`
- 결과: `1 passed`

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과
- [x] 코드 리뷰 승인/병합 (로컬 기준 준비 완료)
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
