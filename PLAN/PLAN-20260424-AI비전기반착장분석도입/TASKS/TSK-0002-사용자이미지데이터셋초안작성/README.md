---
id: TSK-0002-사용자이미지데이터셋초안작성
plan_id: PLAN-20260424-AI비전기반착장분석도입
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-24
---

## 목적
사용자가 제공한 실제 코디 이미지 10장을 비전 평가용 데이터셋에 편입하고, 이미지별 정답 라벨 초안을 작성한다.

## 작업 내역
- [x] 사용자 이미지 10장 데이터셋 폴더 반영
- [x] 이미지별 라벨 JSON 초안 작성
- [x] 문서/루트 README/TODO 갱신
- [x] 커밋

## 산출물(Artifacts)
- 이미지 경로:
  - `backend/data/vision_dataset/images/codytest_1.png`
  - `backend/data/vision_dataset/images/codytest_2.jpg`
  - `backend/data/vision_dataset/images/codytest_3.png`
  - `backend/data/vision_dataset/images/codytest_4.png`
  - `backend/data/vision_dataset/images/codytest_5.png`
  - `backend/data/vision_dataset/images/codytest_6.png`
  - `backend/data/vision_dataset/images/codytest_7.png`
  - `backend/data/vision_dataset/images/codytest_8.png`
  - `backend/data/vision_dataset/images/codytest_9.png`
  - `backend/data/vision_dataset/images/codytest_10.png`
- 라벨 경로:
  - `backend/data/vision_dataset/labels/codytest_1.json`
  - `backend/data/vision_dataset/labels/codytest_2.json`
  - `backend/data/vision_dataset/labels/codytest_3.json`
  - `backend/data/vision_dataset/labels/codytest_4.json`
  - `backend/data/vision_dataset/labels/codytest_5.json`
  - `backend/data/vision_dataset/labels/codytest_6.json`
  - `backend/data/vision_dataset/labels/codytest_7.json`
  - `backend/data/vision_dataset/labels/codytest_8.json`
  - `backend/data/vision_dataset/labels/codytest_9.json`
  - `backend/data/vision_dataset/labels/codytest_10.json`

## 테스트/검증
- 원본 이미지가 데이터셋 폴더에 복사되었는지 확인
- 라벨 JSON이 10장 모두 생성되었는지 확인
- 라벨은 초안이므로 이후 사용자 확인/수정이 가능함

## 완료 기준(DoD)
- [x] 10장 이미지와 10개 라벨 JSON 생성
- [x] README/TODO 갱신
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)

## 완료 메모
- 10장 모두 데이터셋 폴더로 복사하고 샘플별 라벨 JSON 초안을 생성했다.
- 일부 품목명과 색상은 내부 색상 키 체계에 맞춰 근사값으로 작성했으며, 이후 사용자 검수로 보정할 수 있다.
