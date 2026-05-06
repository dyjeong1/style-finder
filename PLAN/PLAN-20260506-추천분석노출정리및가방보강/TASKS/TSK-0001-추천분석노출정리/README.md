---
id: TSK-0001-추천분석노출정리
plan_id: PLAN-20260506-추천분석노출정리및가방보강
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-06
---

## 목적
추천 페이지의 중복 검색어 노출을 줄이고, 업로드 분석 패널의 이해도를 높이며, AI가 놓친 가방 카테고리를 제한적으로 복원한다.

## 작업 내역
- [x] 추천 페이지 상단 `검색어:` 줄 제거
- [x] 분석 칩 도출 근거 설명 문구 추가
- [x] AI 결과 누락 시 가방 카테고리 보강 로직 추가
- [x] 프론트/백엔드 회귀 테스트 및 문서 정리

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/e2e/core-flow.spec.ts`
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd frontend && npm run build`
- `cd frontend && npm run test:e2e:local:smoke -- --grep "@smoke 업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다"`
- `cd backend && python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- 인앱 브라우저 `http://127.0.0.1:3000/recommendations?...` 확인

## 의존성/리스크
- 가방 보강이 다른 카테고리 오탐을 늘리지 않도록 카테고리 범위를 제한해야 한다.
- 직접 입력 검색어 UX와 분석 패널 설명 문구가 서로 중복되지 않게 배치해야 한다.

## 완료 기준(DoD)
- [x] 상단 `검색어:` 줄이 사라진다.
- [x] 분석 칩 도출 근거 설명이 화면에 보인다.
- [x] 가방 카테고리 누락 회귀 테스트가 통과한다.
- [x] 유닛/통합/E2E 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
