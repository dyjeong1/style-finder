---
id: TSK-0001-추천업로드이미지모달확대
plan_id: PLAN-20260505-추천업로드이미지확대미리보기
owner: codex
status: done
estimate: 0.3d
updated_at: 2026-05-05
---

## 목적
추천 상단의 현재 업로드 이미지 썸네일을 클릭 가능한 확대 미리보기로 바꿔, 추천 기준 코디를 더 쉽게 다시 확인할 수 있게 한다.

## 작업 내역
- [x] 추천 상단 업로드 썸네일을 버튼으로 전환
- [x] 모달 기반 확대 미리보기 UI 추가
- [x] 닫기 버튼, 배경 클릭, `Escape` 닫기 처리 추가
- [x] 인앱 브라우저에서 열기/닫기 동작 확인

## 산출물(Artifacts)
- `frontend/app/(main)/recommendations/page.tsx`
- `frontend/app/globals.css`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd frontend && npm run build`
- 인앱 브라우저 `http://127.0.0.1:3000/recommendations?uploaded_image_id=...`에서 상단 썸네일 클릭 후 확대 모달이 열리고 닫히는지 확인
- 브라우저 자동 확인 결과: 썸네일 버튼 표시 `true`, 닫기 후 다이얼로그 표시 `false`

## 의존성/리스크
- 추천 화면이 `uploaded_image_id` 없이 열린 경우에도 fallback 썸네일과 동일한 경로를 재사용해야 한다.
- 모달 오버레이가 추천 필터/스크롤과 충돌하지 않도록 클릭 전파를 차단해야 한다.

## 완료 기준(DoD)
- [x] 추천 상단 썸네일 클릭으로 확대 모달을 열 수 있다.
- [x] 닫기 버튼과 배경 클릭으로 모달을 닫을 수 있다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
