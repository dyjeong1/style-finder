---
id: TSK-0001-업로드기록썸네일저장
plan_id: PLAN-20260422-최근업로드실제썸네일
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-22
---

## 목적
최근 업로드 카드에서 실제 업로드 이미지 썸네일이 보이도록 업로드 히스토리에 브라우저 생성 썸네일을 저장한다.

## 작업 내역
- [x] 업로드 히스토리 타입에 `thumbnail_url` 추가
- [x] 업로드 파일 기반 정사각 썸네일 생성 함수 추가
- [x] 최근 업로드 카드 이미지 소스 우선순위 변경
- [x] 문서와 검증 결과 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `frontend/lib/api.ts`
  - `frontend/app/(main)/upload/page.tsx`
- 문서:
  - `README.md`
  - `TODO.md`
  - `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build` → 성공

## 의존성/리스크
- 기존 기록은 실제 원본 파일을 복원할 수 없어 fallback 썸네일이 유지될 수 있다.
- localStorage 용량을 위해 썸네일을 축소 저장한다.

## 완료 기준(DoD)
- [x] 새 업로드부터 최근 업로드 카드에 실제 썸네일이 표시된다.
- [x] 프론트 빌드 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
