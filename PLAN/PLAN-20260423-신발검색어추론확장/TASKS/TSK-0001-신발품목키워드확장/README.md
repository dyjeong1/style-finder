---
id: TSK-0001-신발품목키워드확장
plan_id: PLAN-20260423-신발검색어추론확장
owner: Codex
status: done
estimate: 0.5d
updated_at: 2026-04-23
---

## 목적
메리제인, 로퍼, 슬리퍼, 구두 같은 신발 하위 품목 직접 검색어를 신발 카테고리로 추론한다.

## 작업 내역
- [x] 신발 하위 품목 키워드 확장
- [x] 메리제인/로퍼/슬리퍼/구두 추론 테스트 추가
- [x] 문서와 검증 결과 갱신

## 산출물(Artifacts)
- 코드 경로:
  - `backend/src/services/naver_shopping.py`
  - `backend/tests/test_naver_shopping.py`
- 문서:
  - `README.md`
  - `TODO.md`

## 테스트/검증
- `cd backend && PYTHONPATH=. python3 -m pytest tests -q` 성공

## 의존성/리스크
- 신발 품목명은 계속 늘어날 수 있으므로 향후 검색어 사전 확장 여지를 남긴다.

## 완료 기준(DoD)
- [x] 메리제인 직접 검색어가 신발로 추론된다.
- [x] 대표 신발 하위 품목 테스트가 통과한다.
- [x] 백엔드 테스트 통과
- [x] TASK 완료 직후 커밋 완료 (커밋 메시지에 TASK ID 포함)
- [x] README/TODO/PLAN 문서 갱신
