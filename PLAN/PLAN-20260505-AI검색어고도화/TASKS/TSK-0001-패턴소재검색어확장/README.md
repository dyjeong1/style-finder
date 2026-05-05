---
id: TSK-0001-패턴소재검색어확장
plan_id: PLAN-20260505-AI검색어고도화
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-05
---

## 목적
AI가 생성하는 상품 검색어에 패턴과 소재 descriptor를 더 안정적으로 보존해 `색상 + 패턴 + 소재 + 품목` 조합을 자연스럽게 만듭니다.

## 작업 내역
- [x] 패턴/소재 descriptor 사전 확장
- [x] 검색어 순서 정규화 보강
- [x] AI 응답 정규화 테스트 추가
- [x] 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `PLAN/PLAN-20260505-AI검색어고도화/*`

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_vision_outfit_analyzer.py -q`

## 의존성/리스크
- AI query 원문에 없는 descriptor를 새로 추정하지 않고, 이미 보이는 표현만 보존해야 검색 범위가 과도하게 좁아지지 않습니다.

## 완료 기준(DoD)
- [x] 패턴과 소재 descriptor가 서비스형 검색어에 반영된다.
- [x] 관련 테스트가 통과한다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
