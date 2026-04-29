---
id: PLAN-20260420-프론트로컬실행안정화
title: 프론트 로컬 실행 안정화
status: done
priority: P1
created_at: 2026-04-20
updated_at: 2026-04-20
related:
  tasks: [TSK-0001-안정실행스크립트추가]
tags: [frontend, local, runtime]
---

## 1. 배경/문제 정의
- 비즈니스 맥락: 개인용으로 빠르게 화면을 확인하는 로컬 웹 앱이 필요하다.
- 현재 성능/운영 이슈: `next dev` 실행 중 React Client Manifest 오류와 `.next` 캐시 꼬임으로 `/recommendations`, `/wishlist`에서 500 또는 hydration 오류가 반복됐다.

## 2. 목표/가설
- 1차 지표(Primary): 로컬 프론트 실행 후 핵심 페이지(`/upload`, `/recommendations`, `/wishlist`)가 안정적으로 200 응답한다.
- 2차 지표(Secondary): 사용자 실행 절차가 한 줄 명령으로 단순화된다.
- 가설: 프로덕션 빌드 기반 실행 명령을 기본 경로로 제공하면 HMR/캐시 꼬임 없이 안정적으로 화면을 확인할 수 있다.

## 3. 범위/산출물(Scope & Deliverables)
- 포함 범위: 프론트 로컬 안정 실행 스크립트 추가, 문서 업데이트, 실행 검증.
- 제외 범위: Next.js 버전 재교체, 렌더링 구조 대규모 변경.
- 산출물(코드/모델/대시보드/문서): `frontend/package.json`, `README.md`, `frontend/README.md`, 루트 `TODO.md`, PLAN/TASK 문서.

## 4. 일정/마일스톤
- M1(문제 재현 확인): 2026-04-20
- M2(안정 실행 스크립트 추가): 2026-04-20
- M3(로컬 페이지 검증): 2026-04-20
- M4(문서 반영 및 완료 처리): 2026-04-20

## 5. 리스크 & 가정
- 데이터 품질/지연/누락: 해당 없음.
- 시스템/리소스 제약: 로컬에서 `npm run build`가 먼저 성공해야 한다.
- 보안/개인정보: 개인 로컬 실행 기준으로 외부 노출 없음.

## 6. 검증/수용 기준(DoD)
- [x] `npm run build` 통과
- [x] 안정 실행 명령으로 핵심 페이지 200 응답 확인
- [x] README/TODO 및 PLAN/TASK 문서 최신화
- [x] TASK 완료 직후 커밋 완료

## 7. 변경 이력
- 2026-04-20: `next dev` 불안정 이슈 대응용 로컬 안정 실행 스크립트와 문서 추가
