---
id: TSK-0002-다중아이템분리개선
plan_id: PLAN-20260424-품목세분화및비전재정렬
owner: Codex
status: ready
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
연결 컴포넌트와 위치 정보를 사용해 다중 아이템을 더 안정적으로 분리하고 없는 카테고리 오탐을 줄인다.

## 작업 내역
- [ ] foreground 연결 컴포넌트 추출
- [ ] 카테고리 매핑/병합 로직 개선
- [ ] 관련 테스트 보강

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/tests/test_outfit_query_hints.py`

## 테스트/검증
- 다중 아이템/없는 카테고리/악세서리 분리 테스트 통과

## 의존성/리스크
- 겹침이 심한 이미지에서는 여전히 완전한 분리가 어려울 수 있다.

## 완료 기준(DoD)
- [ ] 없는 카테고리 오탐 감소
- [ ] 다중 아이템 분리 개선
- [ ] 테스트 통과
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [ ] README/TODO/실험 로그/모델 카드 갱신
