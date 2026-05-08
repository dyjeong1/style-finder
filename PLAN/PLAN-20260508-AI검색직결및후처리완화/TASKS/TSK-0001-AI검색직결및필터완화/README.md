---
id: TSK-0001-AI검색직결및필터완화
plan_id: PLAN-20260508-AI검색직결및후처리완화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-05-08
---

## 목적
AI가 정상 응답했을 때는 그 분석 결과를 그대로 검색에 사용하고, 네이버 후보를 내부 relevance 규칙으로 과하게 버리던 경로를 완화한다.

## 작업 내역
- [x] AI 성공 시 규칙 기반 `bag` 보강 제거
- [x] 네이버 카테고리 후보 후처리 완화
- [x] 관련 백엔드 테스트 갱신
- [x] PLAN/TASK/루트 문서 정리

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/src/services/naver_shopping.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `backend/tests/test_naver_shopping.py`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd backend && python3 -m pytest tests/test_vision_outfit_analyzer.py tests/test_naver_shopping.py -q`

## 의존성/리스크
- relevance 필터 완화로 같은 카테고리 안의 노이즈 상품이 일부 더 들어올 수 있다.
- AI provider 실패 시 fallback 경로가 유지되는지 함께 확인해야 한다.

## 완료 기준(DoD)
- [x] AI 성공 시 규칙 보강 없이 detected items 가 유지된다.
- [x] 같은 카테고리 후보는 세부 품목 mismatch 만으로 제거되지 않는다.
- [x] 유닛 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
