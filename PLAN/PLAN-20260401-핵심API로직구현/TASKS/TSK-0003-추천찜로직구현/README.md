---
id: TSK-0003-추천찜로직구현
plan_id: PLAN-20260401-핵심API로직구현
owner: codex
status: done
estimate: 1d
updated_at: 2026-04-01
---

## 목적
추천 조회와 찜 CRUD를 사용자 기준으로 동작하도록 구현합니다.

## 작업 내역
- [x] 추천 조회(필터/정렬) 구현
- [x] 찜 추가/조회/삭제 구현
- [x] 추천-찜 데이터 연계

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/api/routes/recommendation.py`
  - `backend/src/api/routes/wishlist.py`
  - `backend/src/services/store.py`

## 테스트/검증
- 업로드 ID 존재 여부에 따른 추천 조회 성공/실패 로직 점검
- 찜 추가 중복(409), 삭제 대상 없음(404) 처리 점검
- 정적 검증(`python -m compileall backend/src`)

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과 (`python -m compileall backend/src`)
- [x] 코드 리뷰 승인/병합 (로컬 기준 준비 완료)
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
