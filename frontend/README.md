# Frontend (Next.js)

## 실행 전제
- Node.js 20+
- npm 10+

## 설치/실행
```bash
cd frontend
npm install
npm run dev
```

## 테스트
```bash
cd frontend
npx playwright install chromium
npm run test:e2e
```

## 주요 라우트
- `/upload`
- `/recommendations`
- `/wishlist`

## API 베이스 URL
- 환경변수: `NEXT_PUBLIC_API_BASE_URL`
- 기본값: `http://localhost:8000`

## 의존성 보안 상태
- `next`: `15.5.15`
- 검증: `npm audit` 기준 `0 vulnerabilities`

## 현재 연결된 API 흐름
- `/upload`: `POST /images/upload` 호출 후 업로드 ID를 `stylematch_uploaded_image_id`에 저장
- `/recommendations`: `GET /recommendations` 조회 및 `POST /wishlist` 찜 추가
- `/wishlist`: `GET /wishlist` 조회 시 상품명/가격/쇼핑몰/카테고리/링크를 함께 노출하고 `DELETE /wishlist/{product_id}`로 찜 삭제

## UI 개선 사항 (TSK-0003)
- 추천 페이지: 카테고리/정렬/가격 필터, 재조회/필터 초기화, 스켈레톤 로딩, 빈 상태 안내
- 찜 페이지: 카테고리 필터, 재조회, 빈 상태 CTA
- 공통 네비게이션: 로컬 모드 배지 및 업로드 상태 초기화 버튼
- 위시리스트 카드: 상품 썸네일, 카테고리 배지, 가격/쇼핑몰 메타데이터, 이미지 실패 시 대체 썸네일

## E2E 자동화
- 도구: `@playwright/test`
- 시나리오: 업로드 → 추천 조회 → 찜 추가 → 찜 해제
- 테스트 파일: `frontend/e2e/core-flow.spec.ts`

## CI 자동화
- 워크플로우: `.github/workflows/frontend-e2e.yml`
- 트리거: `frontend/**` 또는 워크플로우 파일 변경 시
- 업로드 아티팩트: `playwright-report`, `test-results`

## 최근 비주얼 리프레시
- 전역 폰트: Pretendard
- 공통 앱 셸: 유리 질감 네비게이션, 브랜드 헤더, 웜 톤 배경
- 업로드/추천/위시리스트: 페이지 헤더 강화, 카드 레이아웃 정리, 추천/최근 업로드 썸네일 밀도 향상
