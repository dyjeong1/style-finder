---
id: TSK-0001-동적코디검색어생성
plan_id: PLAN-20260423-검색어하드코딩제거
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
특정 이미지용 검색어가 모든 업로드 이미지에 반복되지 않도록 검색어 힌트를 동적으로 생성한다.

## 작업 내역
- [x] 하드코딩 검색어 제거
- [x] 색상+카테고리 기반 동적 힌트 생성
- [x] 조건부 구체 품목명 유지
- [x] 회귀 테스트 추가

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/tests/test_outfit_query_hints.py`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- 백엔드 테스트와 프론트 빌드 통과

## 의존성/리스크
- 휴리스틱 기반이라 구체 품목명은 제한적으로 사용한다.

## 완료 기준(DoD)
- [x] 다른 이미지가 고정 검색어를 재사용하지 않음
- [x] 기존 테스트 이미지 기대 검색어 유지
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
