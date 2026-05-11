---
id: PLAN-20260415-로컬개발CORS정리
title: 로컬 개발 CORS 정리
status: done
priority: P1
created_at: 2026-04-15
updated_at: 2026-04-15
related:
  tasks: [TSK-0001-백엔드CORS허용추가]
tags: [backend, cors, local-dev]
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 프론트 `localhost:3000`에서 백엔드 `localhost:8000`으로 로그인 요청을 보내는 로컬 개발 흐름이 기본 동작이어야 합니다.
- 현재 성능/운영 이슈: 백엔드가 브라우저 preflight `OPTIONS` 요청을 허용하지 않아 로그인 화면에서 `Load failed`가 발생합니다.

## 2. 목표/가설
- 1차 지표(Primary): 로컬 프론트와 백엔드 간 교차 출처 요청 허용
- 2차 지표(Secondary): 로그인/업로드 기본 흐름 복구
- 가설: FastAPI CORS 미들웨어를 `localhost:3000`, `127.0.0.1:3000`에 허용하면 Safari에서도 로그인 요청이 정상 동작합니다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위:
  - 백엔드 CORS 미들웨어 추가
  - 로컬 개발 문서 갱신
  - preflight/로그인 검증
- 제외 범위:
  - 배포 환경 CORS 정책 세분화
  - 인증 로직 변경

## 4. 일정/마일스톤
- M1(PLAN 작성): 2026-04-15
- M2(CORS 추가): 2026-04-15
- M3(검증/문서화): 2026-04-15

## 5. 리스크 & 가정
- 시스템/리소스 제약: 현재는 로컬 개발 환경만을 위한 허용 목록입니다.
- 운영 가정: 허용 origin은 `http://localhost:3000`, `http://127.0.0.1:3000`으로 충분합니다.

## 6. 검증/수용 기준(DoD)
- [x] preflight `OPTIONS /auth/login`이 200 계열로 처리됨
- [x] 로컬 로그인 요청이 브라우저에서 가능해짐
- [x] 문서/README/TODO/PLAN/TASK가 갱신됨

## 7. 변경 이력
- 2026-04-15: PLAN 생성
- 2026-04-15: localhost/127.0.0.1 프론트용 CORS 허용 및 preflight 검증 완료
