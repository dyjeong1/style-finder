---
id: TSK-0002-규칙분석fallback전용정리
plan_id: PLAN-20260508-AI검색직결및후처리완화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-08
---

## 목적
규칙 기반 착장 분석기가 AI provider 실패 시 fallback 으로만 동작하도록 런타임 경로를 다시 점검하고, 더 이상 쓰지 않는 fallback 병합 코드까지 제거해 백엔드 코드를 단순화한다.

## 작업 내역
- [x] 규칙 분석기 호출 경로 재점검
- [x] 사용하지 않는 fallback 병합 함수/테스트 제거
- [x] 관련 PLAN/TASK/README/TODO 갱신

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_ai_search_path.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_ai_search_path.py tests/test_vision_outfit_analyzer.py -q`

## 의존성/리스크
- 사용 중이지 않은 정리 코드와 사용자 진행 중인 변경이 섞여 있어 필요한 범위만 조심해서 수정해야 한다.
- 규칙 기반 fallback 자체는 유지해야 하므로 AI 실패 테스트는 계속 살아 있어야 한다.

## 완료 기준(DoD)
- [x] 규칙 분석기는 AI 실패 fallback 시에만 호출된다.
- [x] 더 이상 쓰지 않는 fallback 병합 코드가 제거된다.
- [x] 유닛 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
