---
id: TSK-0001-백엔드CORS허용추가
plan_id: PLAN-20260415-로컬개발CORS정리
owner: codex
status: done
estimate: 0.2d
updated_at: 2026-04-15
---

## 목적
로컬 프론트와 백엔드 간 CORS preflight를 허용해 로그인 실패를 해소합니다.

## 작업 내역
- [x] preflight 실패 원인 확인
- [x] CORS 미들웨어 추가
- [x] OPTIONS/로그인 검증 및 문서 반영

## 산출물(Artifacts)
- `backend/src/main.py`
- PLAN/TASK 문서

## 테스트/검증
- `curl -i -X OPTIONS http://127.0.0.1:8000/auth/login ...`
- `curl -i -X POST http://127.0.0.1:8000/auth/login ...`

## 의존성/리스크
- 로컬 개발용 origin만 허용하므로 다른 포트 사용 시 추가 설정이 필요할 수 있습니다.

## 완료 기준(DoD)
- [x] CORS preflight 정상 처리
- [x] 로그인 API 호출 가능
- [ ] TASK 완료 직후 커밋 완료
