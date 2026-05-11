---
id: TSK-0001-네이버쇼핑후보조회연동
plan_id: PLAN-20260421-네이버쇼핑검색연동
owner: Codex
status: done
estimate: 1d
updated_at: 2026-04-21
---

## 목적
네이버 쇼핑 검색 API를 추천 후보 조회 소스로 추가하고, 키가 없는 로컬 개발 환경에서는 기존 목데이터로 fallback 한다.

## 작업 내역
- [x] 네이버 쇼핑 검색 클라이언트 추가
- [x] 추천 API에 네이버 후보 조회 연결
- [x] 네이버 상품 내부 저장소 등록 처리
- [x] 설정/문서/테스트 정리

## 산출물(Artifacts)
- 코드/스크립트 경로: `backend/src/services/naver_shopping.py`, `backend/src/api/routes/recommendation.py`, `backend/src/core/config.py`
- 문서/노트북: `PLAN/PLAN-20260421-네이버쇼핑검색연동/*`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 의존성/리스크
- 네이버 개발자 센터에서 검색 API 애플리케이션 등록 및 Client ID/Secret 발급 필요

## 완료 기준(DoD)
- [x] 키 없는 환경에서 기존 테스트 통과
- [x] 네이버 응답을 추천 상품 구조로 변환 가능
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
