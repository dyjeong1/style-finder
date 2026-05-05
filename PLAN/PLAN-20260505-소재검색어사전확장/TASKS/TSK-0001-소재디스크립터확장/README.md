---
id: TSK-0001-소재디스크립터확장
plan_id: PLAN-20260505-소재검색어사전확장
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-05
---

## 목적
AI가 생성하는 상품 검색어에 더 다양한 소재 descriptor를 반영해 검색 정확도를 높입니다.

## 작업 내역
- [x] PLAN/SPEC/TASK 문서 생성
- [x] 소재 descriptor 사전 확장
- [x] 검색어 순서 정규화 보강
- [x] 회귀 테스트 추가
- [x] 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `PLAN/PLAN-20260505-소재검색어사전확장/*`
- `.sisyphus/plans/PLAN-20260505-소재검색어사전확장.md`

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_vision_outfit_analyzer.py -q`

## 의존성/리스크
- 소재 표현이 너무 많아지면 검색어가 과도하게 좁아질 수 있어 대표성이 높은 descriptor 중심으로만 추가해야 합니다.

## 완료 기준(DoD)
- [x] 신규 소재 descriptor가 서비스형 검색어에 반영된다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
