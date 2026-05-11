---
id: TSK-0001-백엔드찜목록파일저장
plan_id: PLAN-20260420-위시리스트영속저장
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
백엔드 재시작 후에도 위시리스트가 유지되도록 로컬 파일 기반 persistence를 추가한다.

## 작업 내역
- [x] store에 위시리스트 파일 로드/저장 기능 추가
- [x] 임시 파일 기반 테스트 추가
- [x] README/TODO 및 PLAN/TASK 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `backend/src/services/store.py`
- 테스트 파일: `backend/tests/*`
- 문서/노트북: `README.md`, `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 의존성/리스크
- 파일 손상 시 안전하게 빈 위시리스트로 시작해야 한다.

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
