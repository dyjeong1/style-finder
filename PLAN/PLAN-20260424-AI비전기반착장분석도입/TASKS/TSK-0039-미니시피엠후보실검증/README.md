---
id: TSK-0039-미니시피엠후보실검증
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.4d
updated_at: 2026-05-11
---

## 목적
`ollama`를 유지한 채 후보 모델 `minicpm-v:latest`를 실제 실사 이미지로 검증하고, 현재 기본 모델로 승격할지 판단한다.

## 작업 내역
- [x] `minicpm-v:latest` 모델 pull
- [x] `codytest_2.jpg` 단일 이미지 실검증
- [x] 기존 기본 모델 대비 승격 여부 판단
- [x] PLAN/TODO/운영 문서에 결과 반영
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/README.md`
- `TODO.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/PLAN.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/TASKS/TSK-0039-미니시피엠후보실검증/README.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/TASKS/TSK-0039-미니시피엠후보실검증/TODO.md`

## 테스트/검증
- `ollama pull minicpm-v:latest`
- `/bin/zsh -lc 'export OLLAMA_VISION_MODEL=minicpm-v:latest; export OLLAMA_VISION_TIMEOUT_SECONDS=120.0; python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120'`

## 결과 요약
- `minicpm-v:latest` 설치와 실제 호출은 정상 동작했다.
- `codytest_2.jpg` 기준 응답은 `top/outer`만 남고 `bottom/accessory`가 빠졌으며, `가디건`이 `카디건`으로 출력되는 표기 오차도 있었다.
- 현재 샘플 기준으로는 `gemma3:4b`보다 안정적이지 않아 기본 모델 승격은 보류했다.

## 의존성/리스크
- 단일 샘플 검증이라 다른 장면에서는 결과가 달라질 수 있다.
- `minicpm-v`는 프롬프트/정규화 보강 없이 바로 투입하기엔 품목 누락 리스크가 있다.

## 완료 기준(DoD)
- [x] `minicpm-v` 실모델 pull과 단일 이미지 호출을 완료한다.
- [x] 현재 기본 모델 승격 여부를 근거와 함께 남긴다.
- [x] PLAN/TASK/루트 TODO가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
