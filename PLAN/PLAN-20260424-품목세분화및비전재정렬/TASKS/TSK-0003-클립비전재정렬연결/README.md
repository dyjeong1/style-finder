---
id: TSK-0003-클립비전재정렬연결
plan_id: PLAN-20260424-품목세분화및비전재정렬
owner: Codex
status: ready
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
선택적으로 CLIP 기반 이미지 임베딩을 사용해 추천 랭킹을 재정렬하고, 패키지가 없을 때는 안전하게 fallback한다.

## 작업 내역
- [ ] 비전 임베딩 서비스 인터페이스 추가
- [ ] CLIP provider와 fallback 연결
- [ ] 추천 점수에 비전 유사도 반영
- [ ] 설정/문서/테스트 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `backend/src/services/vision_reranker.py`
  - `backend/src/core/config.py`
  - `backend/src/api/routes/recommendation.py`
  - `backend/src/services/store.py`
  - `backend/tests/*`
- 문서:
  - `backend/README.md`
  - `README.md`
  - `TODO.md`

## 테스트/검증
- CLIP 활성/비활성 fallback 테스트 통과
- 프론트 빌드 통과

## 의존성/리스크
- CLIP는 로컬 패키지 설치가 필요할 수 있다.

## 완료 기준(DoD)
- [ ] 선택적 CLIP 재정렬 연결
- [ ] fallback 안전성 확보
- [ ] 테스트/빌드 통과
- [ ] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [ ] README/TODO/실험 로그/모델 카드 갱신
