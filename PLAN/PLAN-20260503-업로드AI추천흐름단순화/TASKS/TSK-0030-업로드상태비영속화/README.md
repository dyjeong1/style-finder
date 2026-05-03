---
id: TSK-0030-업로드상태비영속화
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: ready
estimate: 0.5d
updated_at: 2026-05-03
---

## 목적
업로드 ID/분석 결과/업로드 히스토리를 localStorage에 남기지 않도록 프론트 상태 흐름을 정리한다.

## 작업 내역
- [ ] 업로드 관련 localStorage 키와 헬퍼 제거 범위 정리
- [ ] 업로드/추천 페이지를 메모리 기준 현재 업로드 1건 흐름으로 변경
- [ ] 최근 업로드 재사용 UI 정리 또는 제거

## 산출물(Artifacts)
- `frontend/lib/api.ts`
- `frontend/app/(main)/upload/page.tsx`
- `frontend/app/(main)/recommendations/page.tsx`

## 테스트/검증
- 새 이미지 업로드 후 브라우저 저장소에 이전 업로드 분석 상태가 남지 않는지 확인

## 의존성/리스크
- URL 기반 추천 진입 방식과 충돌하지 않도록 업로드 직후 이동 흐름을 함께 조정해야 한다.

## 완료 기준(DoD)
- [ ] 업로드 관련 localStorage 영속 상태 제거
- [ ] 새 업로드 시 이전 분석 상태 미노출
- [ ] 테스트/문서 갱신
