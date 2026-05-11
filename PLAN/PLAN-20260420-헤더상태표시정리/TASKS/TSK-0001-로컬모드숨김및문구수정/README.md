---
id: TSK-0001-로컬모드숨김및문구수정
plan_id: PLAN-20260420-헤더상태표시정리
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-21
---

## 목적
헤더 상태 표시와 업로드 보조 문구를 더 간결한 사용자 표현으로 정리한다.

## 작업 내역
- [x] 헤더 `Local Mode` 배지 제거
- [x] 업로드 보조 문구를 요청 문장으로 교체
- [x] 허용 이미지 형식 안내 문구 추가
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/components/app-shell.tsx`, `frontend/app/(main)/upload/page.tsx`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 헤더 우측 정렬 간격이 달라질 수 있어 필요 시 CSS 미세 조정이 필요하다.

## 완료 기준(DoD)
- [x] 헤더에서 `Local Mode`가 보이지 않음
- [x] 업로드 문구가 요청 문장으로 변경됨
- [x] 허용 형식 문구가 업로드 박스에 보임
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
