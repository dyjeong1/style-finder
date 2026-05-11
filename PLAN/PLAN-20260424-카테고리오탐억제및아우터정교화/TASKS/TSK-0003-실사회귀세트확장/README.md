---
id: TSK-0003-실사회귀세트확장
plan_id: PLAN-20260424-카테고리오탐억제및아우터정교화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
실사 착용 사진에서 카테고리 존재 여부와 품목 추론이 안정적으로 유지되도록 회귀 테스트 세트를 늘린다.

## 작업 내역
- [x] 실사 셀카형 추가 픽스처 작성
- [x] 카테고리 존재/부재 회귀 테스트 추가
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/tests/test_outfit_query_hints.py`

## 테스트/검증
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py -q`

## 완료 기준(DoD)
- [x] 실사형 테스트 케이스 2건 이상 추가
- [x] 기존 회귀 테스트 유지
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
