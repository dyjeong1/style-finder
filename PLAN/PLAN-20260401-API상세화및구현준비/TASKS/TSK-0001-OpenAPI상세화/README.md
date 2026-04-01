---
id: TSK-0001-OpenAPI상세화
plan_id: PLAN-20260401-API상세화및구현준비
owner: codex
status: done
estimate: 1d
updated_at: 2026-04-01
---

## 목적
구현팀이 바로 사용할 수 있도록 OpenAPI 명세를 상세화합니다.

## 작업 내역
- [x] 엔드포인트별 요청/응답 스키마 구체화
- [x] 에러 응답 표준(`code`, `message`, `detail`) 정리
- [x] 인증/인가 요구사항 명시

## 산출물(Artifacts)
- 코드/스크립트 경로: `docs/openapi/openapi.yaml`
- 모델/파일: 해당 없음
- 문서/노트북: API 명세 변경 로그

## 테스트/검증
- OpenAPI 핵심 섹션 존재 여부 점검(`paths`, `components.responses`, `components.schemas`)
- 샘플 요청/응답 시나리오(`Auth`, `Recommendation`, `Wishlist`) 검토

## 의존성/리스크
- 선행 TASK/시스템/권한: 없음
- 리스크: 인증 정책 미확정 시 재작업 가능

## 완료 기준(DoD)
- [x] 유닛/통합 테스트 통과 (문서 작업으로 해당 없음)
- [x] 코드 리뷰 승인/병합 (로컬 기준 준비 완료)
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/실험 로그/모델 카드 갱신
