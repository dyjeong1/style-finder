---
id: TSK-0004-하의품목세분화
plan_id: PLAN-20260424-카테고리오탐억제및아우터정교화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
하의를 `데님 팬츠`, `와이드 팬츠`, `슬랙스`, `스커트` 수준으로 더 정확히 구분한다.

## 작업 내역
- [x] 하의 품목 규칙 세분화
- [x] 회귀 테스트 추가
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/tests/test_outfit_query_hints.py`

## 테스트/검증
- 하의 품목 세분화 관련 테스트 통과

## 완료 기준(DoD)
- [x] 데님/슬랙스/스커트/와이드 구분 보강
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
