---
id: TSK-0003-CI테스트워크플로우초안
plan_id: PLAN-20260402-API통합테스트자동화
owner: codex
status: done
estimate: 0.5d
updated_at: 2026-04-02
---

## 목적
CI 환경에서 테스트를 자동 실행할 수 있는 워크플로우 초안을 작성합니다.

## 작업 내역
- [x] 테스트 실행 워크플로우 파일 작성
- [x] 캐시/의존성 설치 전략 반영
- [x] 실패 시 리포트 가시성 개선

## 산출물(Artifacts)
- 코드/스크립트 경로:
  - `.github/workflows/backend-tests.yml`
  - `backend/requirements-test.txt`

## 테스트/검증
- 워크플로우 YAML 정합성 검토
- 로컬 기준 테스트 실행 명령 검증: `PYTHONPATH=. python3 -m pytest tests -q`

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과 (로컬 기준 확인)
- [x] 코드 리뷰 승인/병합 (로컬 기준 준비 완료)
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
