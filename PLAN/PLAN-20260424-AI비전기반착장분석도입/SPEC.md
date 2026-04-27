---
id: PLAN-20260424-AI비전기반착장분석도입-SPEC
plan_id: PLAN-20260424-AI비전기반착장분석도입
status: doing
created_at: 2026-04-24
updated_at: 2026-04-27
---

## 기술 스펙
- 입력: 업로드 이미지 bytes
- 출력: `DetectedOutfitItem[]` 형식의 표준 착장 분석 결과
- 현재 provider: `disabled`, `mock`, `openai`
- 확장 예정 provider: `clip`, `custom_detector`
- OpenAI provider는 `Responses API`의 이미지 입력과 `json_schema` 형식 응답을 사용한다.
- 기존 `VISION_OUTFIT_ANALYZER_*` 설정과 함께 `OPENAI_VISION_*`, `OPENAI_API_KEY` 이름도 동일하게 인식한다.

## 공통 분석 결과 포맷
- category: `top|bottom|outer|shoes|bag|accessory`
- color: 색상 키(`white`, `black`, `blue` 등)
- item_label: 세부 품목명
- query: 추천 검색어로 직접 사용할 수 있는 문자열

## fallback 정책
- 비전 분석기가 비활성화이거나 결과가 비어 있으면 기존 `analyze_outfit_items` 규칙 기반 결과를 사용한다.
- 비전 분석 결과가 일부 카테고리만 제공되면 해당 결과만 우선 사용하고, 비어 있는 카테고리는 규칙 기반 결과로 보완할 수 있도록 설계한다.
- OpenAI 호출 실패, 인증 실패, 타임아웃 발생 시에도 예외를 전파하지 않고 규칙 기반 분석으로 자동 fallback 한다.

## 데이터셋 포맷
- 이미지: `backend/data/vision_dataset/images/<sample_id>.<ext>`
- 라벨: `backend/data/vision_dataset/labels/<sample_id>.json`
- 라벨 필수 필드: `sample_id`, `source`, `items[]`
- items 필드: `category`, `color`, `item_label`, `notes`
