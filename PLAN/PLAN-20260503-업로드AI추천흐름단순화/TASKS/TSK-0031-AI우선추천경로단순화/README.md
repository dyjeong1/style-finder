---
id: TSK-0031-AI우선추천경로단순화
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: ready
estimate: 0.5d
updated_at: 2026-05-03
---

## 목적
추천 생성 경로를 "AI 분석 성공 -> 추천" 중심으로 단순화하고, 불필요한 중간 보정/상태 동기화 잔재를 줄인다.

## 작업 내역
- [ ] 추천 API와 프론트가 현재 업로드의 AI 분석만 기준으로 동작하는지 재정리
- [ ] 필요 없는 업로드 분석 보조 상태와 설명 로직 제거
- [ ] 직접 검색어/추가 옵션이 핵심 흐름을 오염시키는지 검토

## 산출물(Artifacts)
- `backend/src/api/routes/recommendation.py`
- `backend/src/services/store.py`
- `frontend/app/(main)/recommendations/page.tsx`

## 테스트/검증
- AI 분석 성공 시 규칙 분석 결과가 최종 추천 검색어/감지 품목에 섞이지 않는지 확인

## 의존성/리스크
- 검색어 직접 입력이나 필터 기능은 유지 여부를 신중히 판단해야 한다.

## 완료 기준(DoD)
- [ ] AI 성공 경로가 최종 추천 기준으로 명확히 유지됨
- [ ] 불필요한 보조 상태/설명 로직 정리
- [ ] 테스트/문서 갱신
