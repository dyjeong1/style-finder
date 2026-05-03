---
id: TSK-0032-최후fallback검증및정리
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: ready
estimate: 0.4d
updated_at: 2026-05-03
---

## 목적
규칙 분석기를 AI 실패 시에만 쓰는 마지막 fallback 으로 제한하고, 실패 원인을 추적할 수 있게 검증/정리한다.

## 작업 내역
- [ ] AI 실패 조건과 fallback 진입 조건 명시
- [ ] 로그/응답 메타에서 fallback 이유를 추적 가능한지 점검
- [ ] 회귀 테스트와 문서 정리

## 산출물(Artifacts)
- `backend/src/services/store.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/*`

## 테스트/검증
- AI success / AI failure / AI empty result 세 경우를 각각 고정 테스트로 확인

## 의존성/리스크
- provider별 장애 케이스가 달라서 mock 기반 테스트 설계가 중요하다.

## 완료 기준(DoD)
- [ ] fallback 이 마지막 수단으로만 동작함
- [ ] fallback 이유 추적 가능
- [ ] 테스트/문서 갱신
