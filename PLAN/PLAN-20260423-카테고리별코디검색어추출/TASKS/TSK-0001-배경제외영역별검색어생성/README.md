---
id: TSK-0001-배경제외영역별검색어생성
plan_id: PLAN-20260423-카테고리별코디검색어추출
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
배경색을 제외하고 코디 구성품별 검색어 힌트를 생성해 추천 후보 정확도를 높인다.

## 작업 내역
- [x] 배경색 제외 영역별 색상 분석 추가
- [x] 카테고리별 검색어 힌트 생성
- [x] 네이버 검색어 생성 로직에 힌트 반영
- [x] 테스트와 문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/src/services/store.py`
  - `backend/src/services/naver_shopping.py`
  - `backend/tests/*`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- 백엔드 테스트와 프론트 빌드 통과

## 의존성/리스크
- 휴리스틱 기반이므로 코디 이미지 구도에 따라 오차가 있을 수 있다.

## 완료 기준(DoD)
- [x] 품목별 검색어 힌트 생성
- [x] 네이버 검색어 반영
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
