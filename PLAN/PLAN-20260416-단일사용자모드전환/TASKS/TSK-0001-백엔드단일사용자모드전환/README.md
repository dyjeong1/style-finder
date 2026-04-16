---
id: TSK-0001-백엔드단일사용자모드전환
plan_id: PLAN-20260416-단일사용자모드전환
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-16
---

## 목적
백엔드 인증 의존을 제거하고 업로드/추천/위시리스트를 단일 로컬 사용자 기준으로 동작하게 전환합니다.

## 작업 내역
- [x] 인증 라우터 노출 제거
- [x] 단일 로컬 사용자 반환 방식으로 API 의존 단순화
- [x] 백엔드 테스트와 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/api/router.py`
  - `backend/src/core/auth.py`
  - `backend/tests/test_api_e2e.py`
  - `backend/tests/test_api_failures.py`
  - `backend/README.md`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 의존성/리스크
- 프론트는 아직 토큰 기반이므로 다음 TASK에서 함께 제거 필요

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
