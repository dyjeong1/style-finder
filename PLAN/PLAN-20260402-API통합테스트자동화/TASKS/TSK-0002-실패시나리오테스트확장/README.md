---
id: TSK-0002-실패시나리오테스트확장
plan_id: PLAN-20260402-API통합테스트자동화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-02
---

## 목적
인증 실패/중복 찜/검증 실패 등 주요 실패 시나리오를 자동화합니다.

## 작업 내역
- [x] 인증 실패 케이스
- [x] 찜 중복/미존재 삭제 케이스
- [x] 파라미터 검증 실패 케이스

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/tests/test_api_failures.py`

## 테스트/검증
- `PYTHONPATH=. python3 -m pytest tests -q`
- 결과: `5 passed`

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과
- [x] 코드 리뷰 승인/병합 (로컬 기준 준비 완료)
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
