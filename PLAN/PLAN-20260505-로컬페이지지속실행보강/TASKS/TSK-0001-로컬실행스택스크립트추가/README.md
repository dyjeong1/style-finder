---
id: TSK-0001-로컬실행스택스크립트추가
plan_id: PLAN-20260505-로컬페이지지속실행보강
owner: codex
status: done
estimate: 0.4d
updated_at: 2026-05-05
---

## 목적
페이지가 계속 열리도록 프론트/백엔드 로컬 실행 스택을 한 번에 제어하는 스크립트를 추가합니다.

## 작업 내역
- [x] PLAN/SPEC/TASK 문서 생성
- [x] 시작/상태/중지 스크립트 추가
- [x] 로그/PID 관리 경로 정리
- [x] 문서 갱신
- [x] 실제 기동 검증
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `scripts/start-local-stack.sh`
- `scripts/status-local-stack.sh`
- `scripts/stop-local-stack.sh`
- `README.md`
- `frontend/README.md`
- `PLAN/PLAN-20260505-로컬페이지지속실행보강/*`
- `.sisyphus/plans/PLAN-20260505-로컬페이지지속실행보강.md`

## 테스트/검증
- `./scripts/start-local-stack.sh`
- `curl -s http://127.0.0.1:8000/health`
- `curl -I -s http://127.0.0.1:3000/upload`
- `./scripts/status-local-stack.sh`
- `./scripts/stop-local-stack.sh`

## 의존성/리스크
- 프론트는 Node/npm, 백엔드는 Python 실행 환경에 의존합니다.
- stale PID나 포트 점유 상황을 스크립트에서 방어해야 재시작이 쉬워집니다.

## 완료 기준(DoD)
- [x] 로컬 시작/상태/중지 스크립트가 동작한다.
- [x] 페이지가 실제로 열리는 것이 검증된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
