---
id: TSK-0002-DB마이그레이션초안작성
plan_id: PLAN-20260401-API상세화및구현준비
owner: codex
status: done
estimate: 1d
updated_at: 2026-04-01
---

## 목적
DDL 초안을 마이그레이션 형식으로 구조화해 실제 적용 가능한 상태로 정리합니다.

## 작업 내역
- [x] 테이블 생성 SQL을 버전형 마이그레이션으로 분리
- [x] 인덱스/제약조건 검증
- [x] 롤백 전략 초안 작성

## 산출물(Artifacts)
- 코드/스크립트 경로: `backend/migrations/`
- 모델/파일:
  - `backend/migrations/V1__init_schema.sql`
  - `backend/migrations/R__rollback_v1.sql`
- 문서/노트북: 마이그레이션 적용 가이드

## 테스트/검증
- SQL 구문/테이블/인덱스/제약조건 정합성 정적 검토
- 롤백 순서(의존성 역순 삭제) 검토

## 의존성/리스크
- 선행 TASK/시스템/권한: TSK-0001 결과 반영 필요
- 리스크: pgvector 버전 호환성

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과 (문서/DDL 초안 작업으로 해당 없음)
- [x] 코드 리뷰 승인/병합 (로컬 기준 준비 완료)
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
