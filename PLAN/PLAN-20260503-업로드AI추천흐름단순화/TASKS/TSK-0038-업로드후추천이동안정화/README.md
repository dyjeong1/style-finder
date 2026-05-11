---
id: TSK-0038-업로드후추천이동안정화
plan_id: PLAN-20260503-업로드AI추천흐름단순화
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-05-03
---

## 목적
로컬 브라우저에서 업로드 완료 후 추천 페이지로 넘어갈 때 `이미지 분석 중...` 상태에 머무는 것처럼 보이는 흐름을 줄이고, 프론트-백엔드 연결 주소도 `127.0.0.1` 기준으로 일관되게 맞춘다.

## 작업 내역
- [x] 프론트 기본 API 주소를 `http://127.0.0.1:8000`으로 조정
- [x] 업로드 완료 후 추천 페이지 이동에 하드 리다이렉트 fallback 추가
- [x] 프론트 재빌드 및 로컬 서버 재기동
- [x] 백엔드 헬스체크와 프론트 응답 확인
- [x] README/TODO/PLAN/TASK 문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `frontend/lib/api.ts`
- `frontend/app/(main)/upload/page.tsx`
- `README.md`
- `TODO.md`
- `PLAN/PLAN-20260503-업로드AI추천흐름단순화/PLAN.md`

## 테스트/검증
- 백엔드: `curl http://127.0.0.1:8000/health`
- 프론트: `curl -I http://127.0.0.1:3000/upload`
- 런타임 로그 기준 업로드/추천 API가 `200 OK`로 왕복되는 것 확인
- `npm run local` 재빌드/재기동 후 `http://127.0.0.1:3000/upload`에서 수동 재테스트 가능 상태 확인

## 의존성/리스크
- 이번 수정은 라우팅 안정성을 우선한 대응이라, App Router 원인 자체를 콘솔 수준에서 완전히 분석한 것은 아니다.
- `window.location.assign` fallback 을 사용하므로 업로드 직후 추천 페이지 이동은 SPA 전환보다 더 강한 전체 페이지 이동으로 동작할 수 있다.

## 결과 요약
- 프론트 기본 API 주소를 `localhost` 대신 `127.0.0.1`로 맞춰 로컬 바인딩과 주소 체계를 일치시켰다.
- 업로드 성공 직후 추천 페이지 이동이 App Router 상태에만 의존하지 않도록 하드 리다이렉트 fallback 을 추가했다.
- 현재 로컬 테스트 URL은 `http://127.0.0.1:3000/upload`, 백엔드 헬스 URL은 `http://127.0.0.1:8000/health` 기준으로 확인했다.

## 완료 기준(DoD)
- [x] 업로드 후 추천 페이지 이동 경로가 더 안정적으로 동작한다.
- [x] 프론트-백엔드 로컬 주소 체계가 일관된다.
- [x] 로컬 서버 재기동 후 테스트 가능한 URL을 사용자에게 전달한다.
- [x] README/TODO/PLAN/TASK 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
