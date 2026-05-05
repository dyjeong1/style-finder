---
id: TSK-0001-브랜드디스크립터반영
plan_id: PLAN-20260505-브랜드로고검색어반영
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-05
---

## 목적
로고나 브랜드 텍스트가 보이는 이미지에서 브랜드를 검색어 앞에 반영해 추천 검색 정확도를 높입니다.

## 작업 내역
- [x] PLAN/SPEC/TASK 문서 생성
- [x] AI 응답 스키마에 brand 필드 추가
- [x] 브랜드 query prefix 규칙 추가
- [x] 회귀 테스트 추가
- [x] 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/image_analysis.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/src/services/store.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/tests/test_api_e2e.py`
- `PLAN/PLAN-20260505-브랜드로고검색어반영/*`
- `.sisyphus/plans/PLAN-20260505-브랜드로고검색어반영.md`

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_api_e2e.py -q`

## 의존성/리스크
- 브랜드 오탐은 검색 범위를 급격히 좁힐 수 있으므로, 명확한 로고/텍스트가 보일 때만 보존하는 보수적 규칙이 필요합니다.

## 완료 기준(DoD)
- [x] 브랜드 descriptor가 서비스형 검색어에 반영된다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
