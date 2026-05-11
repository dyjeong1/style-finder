---
id: TSK-0004-codytest9라벨재보정
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.1d
updated_at: 2026-04-24
---

## 목적
추가 사용자 검수 내용을 반영해 `codytest_9`의 outer 라벨을 실제 착장에 맞게 재보정한다.

## 작업 내역
- [x] `codytest_9` outer 라벨 수정
- [x] 문서/루트 README/TODO 갱신
- [x] 커밋

## 산출물(Artifacts)
- `backend/data/vision_dataset/labels/codytest_9.json`

## 테스트/검증
- 수정된 JSON이 정상 파싱되는지 확인
- outer가 `버건디 가디건` 취지로 반영되었는지 확인

## 완료 기준(DoD)
- [x] 라벨 수정 완료
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO 갱신

## 완료 메모
- `codytest_9`의 outer를 `레드 니트 베스트`에서 `버건디 가디건` 취지로 수정했다.
- 내부 색상 키 체계상 버건디는 `red`로 유지하고, 실제 의미는 notes에 남겼다.
