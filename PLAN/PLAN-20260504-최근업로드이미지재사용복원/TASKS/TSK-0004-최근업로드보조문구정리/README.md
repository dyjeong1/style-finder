---
id: TSK-0004-최근업로드보조문구정리
plan_id: PLAN-20260504-최근업로드이미지재사용복원
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-04
---

## 목적
최근 업로드 패널의 중복 보조 문구를 제거해 제목과 빈 상태 핵심 메시지만 남긴다.

## 작업 내역
- [x] 패널 상단 설명 문구 제거
- [x] 빈 상태 보조 문구 제거
- [x] 브라우저에서 문구 제거 상태 확인

## 산출물(Artifacts)
- `frontend/app/(main)/upload/page.tsx`
- 관련 PLAN/TASK/README/TODO 문서

## 테스트/검증
- `cd frontend && npm run local` 재실행 후 인앱 브라우저 `http://127.0.0.1:3000/upload`에서 보조 문구 제거 확인
- DOM snapshot 기준 상단/빈 상태 보조 문구가 모두 사라지고 `최근 업로드가 없습니다.`만 남아 있는지 확인

## 의존성/리스크
- 빈 상태에서 정보가 너무 부족해 보이지 않도록 제목과 핵심 문장 위계는 유지해야 한다.

## 완료 기준(DoD)
- [x] 선택된 두 보조 문구가 제거된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
