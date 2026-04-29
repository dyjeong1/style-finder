---
id: TSK-0001-전체카테고리품목키워드확장
plan_id: PLAN-20260423-제품군키워드사전확장
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
모든 제품군의 하위 품목 검색어를 카테고리로 추론할 수 있도록 키워드 사전을 확장한다.

## 작업 내역
- [x] 상의/하의/아우터/가방 하위 품목 키워드 확장
- [x] 신발 키워드 사전 유지 및 보강
- [x] 카테고리별 추론 테스트 추가
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
- 키워드 기반 추론이므로 향후 누락 품목이 발견되면 사전을 계속 보강한다.

## 완료 기준(DoD)
- [x] 모든 카테고리 대표 하위 품목 검색어 테스트 통과
- [x] 제품군 없는 검색어의 전체 카테고리 분산 조회 유지
- [x] 백엔드 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
