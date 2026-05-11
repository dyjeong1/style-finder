---
id: TSK-0001-검색어제품군추론구현
plan_id: PLAN-20260423-직접검색어카테고리추론
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
직접 입력 검색어에 제품군이 포함된 경우 해당 카테고리만 추천 조회하도록 조정한다.

## 작업 내역
- [x] 제품군 키워드 추론 함수 추가
- [x] 직접 검색어 카테고리 쿼리 생성 범위 조정
- [x] 테스트 추가/수정
- [x] 문서와 검증 결과 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/naver_shopping.py`
  - `backend/tests/test_naver_shopping.py`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 성공

## 의존성/리스크
- 네이버 쇼핑 검색 결과 자체가 완전히 통제되지는 않으므로, 우선 검색 쿼리 단계에서 사용자의 제품군 의도를 명확히 반영한다.

## 완료 기준(DoD)
- [x] 제품군 명시 직접 검색어는 해당 카테고리 쿼리만 생성한다.
- [x] 제품군 없는 직접 검색어는 전체 카테고리 쿼리를 유지한다.
- [x] 백엔드 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
