# 비전 착장 분석 데이터셋

이 폴더는 AI 비전 모델의 착장 분석 품질을 검증하기 위한 로컬 데이터셋 저장 위치입니다.

## 구조
- `images/`: 원본 테스트 이미지
- `labels/`: 이미지별 정답 라벨 JSON

## 라벨 규칙
- `sample_id`: 이미지와 라벨을 연결하는 ID
- `source`: `user-test`, `regression`, `mock` 등 출처
- `items`: 감지되어야 하는 착장 목록

### items 필드
- `category`: `top|bottom|outer|shoes|bag|accessory`
- `color`: 내부 색상 키
- `item_label`: 기대 품목명
- `notes`: 선택 설명

## 사용 방식
1. 실제 테스트 이미지를 `images/`에 넣습니다.
2. 같은 ID로 `labels/`에 JSON 라벨을 만듭니다.
3. 이후 평가 스크립트나 테스트가 이미지와 라벨을 함께 읽어 비교합니다.

## 현재 포함 샘플
- `sample-flatlay-001`: 내부 회귀용 샘플
- `codytest_1` ~ `codytest_10`: 사용자 제공 실제 코디 이미지 초안 라벨 세트

## 평가 실행
```bash
cd backend
PYTHONPATH=. python3 scripts/evaluate_vision_dataset.py
```

JSON 형식으로 보려면:
```bash
cd backend
PYTHONPATH=. python3 scripts/evaluate_vision_dataset.py --format json
```
