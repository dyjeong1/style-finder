---
id: TSK-0001-삭제아이콘및형식문구조정
plan_id: PLAN-20260421-최근업로드카드액션정리
owner: Codex
status: done
estimate: 0.2d
updated_at: 2026-04-21
---

## 목적
최근 업로드 카드 삭제 액션을 더 압축된 UI로 바꾸고 업로드 형식 문구를 요청 표현으로 맞춘다.

## 작업 내역
- [x] 최근 업로드 삭제 버튼을 카드 내부 아이콘 형태로 조정
- [x] placeholder 문구를 요청 형식으로 수정
- [x] 빌드 검증 및 문서 갱신

## 산출물(Artifacts)
- 코드/스크립트 경로: `frontend/app/(main)/upload/page.tsx`, `frontend/app/globals.css`
- 문서/노트북: `README.md`, `TODO.md`, `frontend/README.md`

## 테스트/검증
- `cd frontend && npm run build`

## 의존성/리스크
- 카드 내부 절대 위치 버튼이라 모바일에서 클릭 영역이 너무 작지 않게 확인이 필요하다.

## 완료 기준(DoD)
- [x] 카드 내부 우측 상단에 `x` 삭제 아이콘이 보인다.
- [x] placeholder 문구가 `허용 이미지: PNG, JPG, JPEG, WEBP`로 보인다.
- [x] 빌드 검증 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
