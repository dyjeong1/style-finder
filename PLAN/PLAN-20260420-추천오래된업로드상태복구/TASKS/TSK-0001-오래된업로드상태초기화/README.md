---
id: TSK-0001-오래된업로드상태초기화
plan_id: PLAN-20260420-추천오래된업로드상태복구
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-20
---

## 목적
백엔드 재시작 등으로 업로드 기록이 사라졌을 때 추천 페이지가 깨지지 않고, 사용자가 다시 업로드로 돌아갈 수 있게 복구한다.

## 작업 내역
- [x] 추천 API 실패 시 stale 업로드 상태 감지 로직 추가
- [x] localStorage 업로드 상태 자동 초기화
- [x] 사용자 안내 문구 개선
- [x] 문서 및 루트 TODO 반영

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/recommendations/page.tsx`
- 문서/노트북: `README.md`, `frontend/README.md`, `TODO.md`

## 테스트/검증
- 오래된 업로드 ID 상태에서 추천 진입 시 안내 문구 노출 확인
- `/upload` 재업로드 후 추천 재조회 정상 동작 확인

## 의존성/리스크
- 업로드 데이터는 백엔드 메모리 저장이므로 재시작 시 초기화된다.

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과
- [x] 코드 리뷰 승인/병합
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
