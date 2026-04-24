---
id: TSK-0002-실사이미지일반화분석개선
plan_id: PLAN-20260424-카테고리오탐억제및아우터정교화
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
플랫레이가 아닌 실사 착용 사진에서도 배경에 흔들리지 않고 실제 착용 아이템 중심으로 카테고리와 검색어를 추론한다.

## 작업 내역
- [x] 사람 중심 foreground 범위 추론 추가
- [x] 배경 패널/문/거울 가장자리 오염 억제
- [x] 실사 셀카형 테스트 픽스처 추가
- [x] 이너/가디건/안경 분리 보정
- [x] 테스트/문서 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/image_analysis.py`
  - `backend/tests/test_outfit_query_hints.py`

## 테스트/검증
- 실사 셀카형 테스트에서 `가방/신발`이 없으면 제외되고, `가디건/이너/데님/안경`이 분리되는지 확인
- `PYTHONPATH=backend python3 -m pytest backend/tests/test_outfit_query_hints.py backend/tests/test_naver_shopping.py backend/tests/test_api_e2e.py backend/tests/test_api_failures.py -q`

## 완료 기준(DoD)
- [x] 실사 사진에서 배경 오염 감소
- [x] 없는 카테고리 제외 유지
- [x] 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신
