---
id: TSK-0038-올라마기본모델재검증
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.4d
updated_at: 2026-05-11
---

## 목적
`ollama` provider는 유지하되 `qwen2.5vl:7b`와 `gemma3:4b`를 같은 실이미지로 다시 비교해, 현재 기본 비전 모델을 무엇으로 유지할지 근거를 확보한다.

## 작업 내역
- [x] `qwen2.5vl:7b`, `gemma3:4b` 설치 상태와 비교 가능 여부 확인
- [x] `codytest_2.jpg` 실이미지로 두 모델의 단일 분석 결과 재검증
- [x] 비교 결과를 바탕으로 기본 모델 유지 결론 정리
- [x] 백엔드/루트/설치 문서에 현재 권장 모델 상태를 반영
- [x] TASK 완료 직후 커밋

## 산출물(Artifacts)
- `backend/README.md`
- `docs/ollama-local-setup.md`
- `TODO.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/PLAN.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/TASKS/TSK-0038-올라마기본모델재검증/README.md`
- `PLAN/PLAN-20260424-AI비전기반착장분석도입/TASKS/TSK-0038-올라마기본모델재검증/TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests/test_vision_outfit_analyzer.py -q`
- `cd backend && PYTHONPATH=. python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120`
- `/bin/zsh -lc 'export OLLAMA_VISION_MODEL=gemma3:4b; export OLLAMA_VISION_TIMEOUT_SECONDS=120.0; python3 scripts/check_upload_analysis.py --image data/vision_dataset/images/codytest_2.jpg --provider ollama --timeout-seconds 120'`

## 결과 요약
- 로컬 장비에는 `qwen2.5vl:7b`, `gemma3:4b`가 모두 설치되어 있어 추가 pull 없이 바로 비교 가능함을 확인했다.
- `qwen2.5vl:7b`는 `화이트 셔츠 / 블루 가디건 / 블랙 데님 팬츠 / 베이지 숄더백 / 브라운 안경` 수준으로 응답해 가방 오검출과 색상 오차가 남았다.
- `gemma3:4b`는 `화이트 니트 탑 / 그레이 니트 가디건 / 블루 와이드 데님 팬츠 / 블랙 안경` 수준으로 응답해, 같은 샘플에서는 더 안정적이었다.
- 비교 결과 현재 기본 Ollama 모델은 `gemma3:4b`를 유지하는 쪽으로 정리했다.

## 의존성/리스크
- 단일 샘플 비교만으로 전체 우열이 확정되지는 않으므로, 추후 10장 이상 샘플셋 비교가 필요하다.
- `qwen2.5vl:7b`는 장면에 따라 더 강할 수 있으나 현재 실사 셀카 샘플에서는 기본값으로 올리기엔 리스크가 있다.

## 완료 기준(DoD)
- [x] 두 Ollama 모델을 같은 실이미지로 재검증한다.
- [x] 비교 결과에 따라 현재 기본 모델 유지/변경 결론을 남긴다.
- [x] 현재 권장 모델 상태가 문서에 반영된다.
- [x] README/TODO/PLAN 문서가 갱신된다.
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
