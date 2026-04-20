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

## 권장 로컬 실행
`next dev`에서 간헐적으로 HMR/캐시 꼬임이 생길 수 있어서, 화면 확인은 아래 명령을 기본으로 권장합니다.

```bash
cd frontend
npm run local
```

- 접속 주소: `http://127.0.0.1:3000`
- 포함 동작: `build` 후 `start --hostname 127.0.0.1 --port 3000`

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

## 최근 추천-위시리스트 연결 개선
- 추천 화면에서 위시리스트를 함께 조회해 Saved 상태를 즉시 표시
- 저장된 상품은 `Saved in Wishlist` 버튼으로 비활성화
- 저장 직후 추천 카드 상태와 상단 요약이 즉시 갱신

## 최근 하이드레이션 안정화
- 추천 페이지의 업로드 상태는 mount 이후 로컬 저장소에서 동기화
- SSR/CSR 초기 렌더 차이로 생기던 hydration mismatch를 줄임

## 최근 로컬 실행 안정화
- `npm run local` 스크립트 추가
- `next dev` 대신 프로덕션 빌드 기반으로 페이지를 확인하는 흐름 정리

## 최근 추천 복구 개선
- 백엔드 재시작 뒤 오래된 `uploaded_image_id`가 남아 있어도 추천 페이지가 치명적으로 깨지지 않음
- stale 업로드 상태를 자동으로 비우고 `/upload` 재업로드를 안내함

## 최근 위시리스트 정렬 개선
- 위시리스트에서 최신순/오래된순/가격 오름차순/가격 내림차순/이름순 정렬을 지원
- 정렬 변경은 추가 API 호출 없이 즉시 반영

## 최근 업로드 화면 리디자인
- 업로드 화면을 큰 인트로 패널 + 드롭존 + 우측 최근 업로드 패널 구조로 재정리
- 최근 업로드 카드의 썸네일과 CTA 버튼 크기를 키워 레퍼런스형 위계로 조정

## 최근 업로드 드래그앤드롭 개선
- 업로드 드롭존에 이미지 파일 drag-and-drop 선택을 지원
- 드래그 중 드롭존 활성 상태를 색상/그림자로 강조

## 최근 업로드 문구 단순화
- 업로드 화면의 영어 eyebrow, 드롭존 배지, 보조 문구를 제거해 첫 화면을 더 간결하게 정리
- 최근 업로드는 개별 CTA 버튼 대신 카드 전체 클릭으로 추천 재사용 흐름을 유지
- 업로드 메인 타이틀은 더 작은 크기로 조정해 화면 균형을 맞춤

## 최근 폰트 단위 정리
- `frontend/app/globals.css`의 폰트 크기 선언을 `pt` 기준으로 정리
- 업로드 화면 메인 타이틀 `.upload-stage-copy h1`은 `36pt`로 적용
- 남아 있던 반응형 `clamp(...)` font-size도 제거해 버튼을 포함한 주요 텍스트를 고정 pt 값으로 정리
- 이후 업로드 화면 메인 타이틀은 `30pt`, 메인 CTA 버튼 텍스트는 `14pt`로 줄이고 버튼 박스도 함께 축소

## 최근 업로드 박스 통합 개선
- 업로드 선택 영역과 미리보기 영역을 하나의 박스로 통합
- 이미지 선택 후 같은 박스 안에서 정사각형 미리보기를 바로 확인 가능
- `사진 삭제` 버튼으로 선택 파일과 상태를 즉시 초기화
- `이미지 분석하기` 버튼은 선택 파일이 있을 때만 활성화
