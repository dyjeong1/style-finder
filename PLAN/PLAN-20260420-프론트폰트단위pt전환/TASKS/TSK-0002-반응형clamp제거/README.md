---
id: TSK-0002-반응형clamp제거
plan_id: PLAN-20260420-프론트폰트단위pt전환
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-20
---

## 목적
남아 있는 반응형 `clamp(...)` 폰트 선언을 제거하고, 고정 `pt` 값으로 정리한다.

## 작업 내역
- [x] `globals.css`의 남은 `clamp(...)` font-size 제거
- [x] 업로드 버튼을 포함한 주요 텍스트를 고정 pt 값으로 정리
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 고정값 전환 후 작은 화면에서 타이포 밀도가 달라질 수 있어 실제 페이지 확인이 필요하다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
