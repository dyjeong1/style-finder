---
id: TSK-0013-경량모델후처리정규화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-29
---

## 목적
`gemma3:4b`가 생성하는 자유로운 품목명을 서비스의 정규 카테고리/품목 표현으로 보정해, 로컬 경량 모델의 실사용 품질을 높인다.

## 작업 내역
- [x] 경량 모델 응답에서 자주 나오는 표현 편차를 정리한다.
- [x] 색상/품목명 후처리 정규화 규칙을 추가한다.
- [x] 테스트 케이스를 보강한다.
- [x] 실샘플 재검증과 문서 갱신을 수행한다.
- [x] TASK 완료 직후 커밋한다.

## 산출물(Artifacts)
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `README.md`
- `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --sample-ids codytest_2 --format text --timeout-seconds 120 --max-retries 0`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 결과 요약
- 경량 모델 응답에서 자주 나오는 표현을 서비스 품목명으로 정규화했다.
- `선글라스 -> 안경`, `청바지 팬츠 -> 데님 팬츠`, `나시 -> 슬리브리스 탑` 같은 규칙을 후처리에 추가했다.
- `codytest_2.jpg` 재검증에서 `블루 데님 팬츠`, `블랙 안경` 형태로 더 서비스 친화적인 결과를 확인했다.
- 다만 단일 샘플 비교 기준 정밀도/재현율은 아직 규칙 기반보다 낮아서, 다음 단계는 상의/아우터 색상과 품목 판별 정밀화가 필요하다.

## 의존성/리스크
- 과한 정규화는 원래 모델이 맞춘 세부 표현을 단순화할 수 있다.
- 현재 후처리는 품목명 표준화에는 효과가 있지만, 모델 자체의 오인식까지 해결하지는 못한다.

## 완료 기준(DoD)
- [x] 경량 모델 후처리 정규화가 코드에 추가된다.
- [x] 관련 테스트가 통과한다.
- [x] 실샘플에서 적어도 일부 품목명이 더 서비스 친화적으로 정리된다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
