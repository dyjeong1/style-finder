---
id: TSK-0003-업로드타이틀및버튼축소
plan_id: PLAN-20260420-프론트폰트단위pt전환
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-20
---

## 목적
업로드 화면 메인 타이틀과 기본 CTA 버튼의 시각적 크기를 함께 낮춰 더 안정적인 균형을 만든다.

## 작업 내역
- [x] 업로드 타이틀을 `30pt`로 조정
- [x] 업로드 CTA 버튼 높이/너비/패딩 축소
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 버튼 크기 축소 후에도 클릭 영역과 가독성은 유지되어야 한다.

## 완료 기준(DoD)
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
