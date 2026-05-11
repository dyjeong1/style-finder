---
id: TSK-0014-삼자비교리포트및상의아우터정밀화
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.8d
updated_at: 2026-04-29
---

## 목적
`rule / gemini / ollama(gemma3:4b)` 비교 결과를 정리하고, 현재 경량 모델에서 특히 약한 상의/아우터 판별을 정밀화한다.

## 작업 내역
- [x] 3-way 비교 리포트 생성
- [x] 상의/아우터 오차 패턴 확인
- [x] 상의/아우터 정밀화 규칙 또는 후처리 보정 추가
- [x] 테스트/문서 갱신
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/scripts/compare_vision_predictors.py`
- `backend/src/services/vision_outfit_analyzer.py`
- `backend/tests/test_vision_outfit_analyzer.py`
- `README.md`
- `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate ollama --format text --timeout-seconds 120 --no-cache`
- `cd backend && PYTHONPATH=. python3 scripts/compare_vision_predictors.py --baseline rule --candidate gemini --format text --timeout-seconds 60`
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q`

## 비교 결과 요약
- 기준 `rule`: 정밀도 `0.2500`, 재현율 `0.2281`
- `gemini`: 정밀도 `0.4211`, 재현율 `0.4211`
- `ollama(gemma3:4b)` fresh 실행: 정밀도 `0.3784`, 재현율 `0.2456`
- 현재 3-way 순위는 `gemini > ollama(gemma3:4b) > rule`이다.

## 상의/아우터 보정 결과
- `재킷 -> 자켓`, `점프수트 -> 원피스`, `가방으로 잘못 들어온 outer -> bag` 보정을 추가했다.
- `codytest_6`에서 `블랙 원피스`는 정규화 이후 기대치에 맞게 정리됐다.
- `codytest_2`에서는 `블루 데님 팬츠`, `블랙 안경`까지는 정리됐지만, `화이트 슬리브리스 탑`과 `블루 가디건`은 아직 `셔츠/그레이 가디건` 쪽으로 흔들린다.

## 남은 오차 패턴
- `codytest_1`: `니트 베스트`를 `가디건`으로 읽는 경향
- `codytest_2`: `슬리브리스 탑`, `블루 가디건`을 놓치고 색상도 회색으로 흔들림
- `codytest_3`: `top`으로 들어온 `가디건`을 `outer`와 분리하지 못함
- `codytest_4`: `네이비 브이넥 니트 + 스트라이프 티셔츠` 레이어드 분리 실패
- `codytest_8`: `브이넥 니트`를 `가디건`으로 과해석
- `codytest_9`: `버건디 가디건` 색상을 회색으로 오인식

## 의존성/리스크
- 경량 모델은 로컬 반복성은 좋지만, 상의/아우터 색상과 레이어드 분리에 아직 취약하다.
- 캐시가 이전 결과를 재사용할 수 있어, 모델/후처리 변경 후 비교 시에는 `--no-cache`가 필요하다.

## 완료 기준(DoD)
- [x] 3-way 비교 결과를 문서로 남긴다.
- [x] 상의/아우터 보정이 코드에 반영된다.
- [x] 관련 테스트가 통과한다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
