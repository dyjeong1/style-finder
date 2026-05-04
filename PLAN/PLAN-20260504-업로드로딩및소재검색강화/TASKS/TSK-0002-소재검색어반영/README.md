---
id: TSK-0002-소재검색어반영
plan_id: PLAN-20260504-업로드로딩및소재검색강화
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-04
---

## 목적
추천 검색어가 색상과 품목뿐 아니라 소재 descriptor도 함께 반영하도록 보강합니다.

## 작업 내역
- [x] 소재 descriptor 규칙 추가
- [x] 검색어/테스트 갱신
- [x] 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_vision_outfit_analyzer.py -q`

## 의존성/리스크
- descriptor 순서가 검색 정밀도에 영향을 줄 수 있어 기존 카테고리별 우선순위를 유지해야 합니다.

## 완료 기준(DoD)
- [x] 소재 descriptor가 검색어에 반영된다.
- [x] 테스트가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
