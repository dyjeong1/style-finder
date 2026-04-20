# 스타일매치 (가칭)

코디/착장 이미지를 업로드하면 이미지와 유사한 의류 상품을 지그재그와 29CM에서 찾아 추천해주는 비공개(Private) 웹 서비스입니다.  
사용자는 하나의 코디 이미지를 업로드한 뒤, 추천 결과를 상의/하의/아우터/신발/가방 등 카테고리별로 확인할 수 있고, 유사도순 정렬, 가격대 필터, 찜 기능을 통해 원하는 상품만 빠르게 모아볼 수 있습니다.

---

## 0. 개발 착수 가이드

### 문서 운영 원칙
- 코딩 작업은 `PLAN` 단위로 시작합니다.
- 각 PLAN은 `TASKS`로 분해하고, 각 TASK에 `README.md`/`TODO.md`를 유지합니다.
- 루트 `README.md`/`TODO.md`는 작업 전후로 갱신합니다.

### 현재 활성 PLAN
- `PLAN-20260421-업로드안내및최근기록정리`
- 상세 문서: `PLAN/PLAN-20260421-업로드안내및최근기록정리/PLAN.md`
- 기술 스펙: `PLAN/PLAN-20260421-업로드안내및최근기록정리/SPEC.md`
- 상태: `done` (placeholder 형식 안내 이동 및 최근 업로드 삭제 기능 추가 완료, 2026-04-21)

### 현재 저장소 구조(초기)
```text
.
├─ AGENTS.md
├─ README.md
├─ TODO.md
├─ .sisyphus/
│  └─ plans/
│     └─ PLAN-20260331-MVP초기세팅.md
├─ PLAN/
│  └─ PLAN-20260331-MVP초기세팅/
│     ├─ PLAN.md
│     ├─ SPEC.md
│     └─ TASKS/
│        ├─ TSK-0001-저장소구조세팅/
│        │  ├─ README.md
│        │  └─ TODO.md
│        └─ TSK-0002-아키텍처초안정의/
│           ├─ README.md
│           └─ TODO.md
│  └─ PLAN-20260401-API상세화및구현준비/
│     ├─ PLAN.md
│     ├─ SPEC.md
│     └─ TASKS/
│        ├─ TSK-0001-OpenAPI상세화/
│        │  ├─ README.md
│        │  └─ TODO.md
│        ├─ TSK-0002-DB마이그레이션초안작성/
│        │  ├─ README.md
│        │  └─ TODO.md
│        └─ TSK-0003-백엔드스캐폴딩/
│           ├─ README.md
│           └─ TODO.md
└─ src/
   └─ name/
      └─ data/
```

### 설치/실행 (1차)
현재는 백엔드 기초, 프론트 MVP, E2E CI, `main` 브랜치 보호 규칙 적용, PR 기준 required check 실동작 검증, GitHub Actions Node 24 대응, solo 운영 기준 브랜치 보호 정책 정리, required check 이름 정합성 수정, 업로드 이미지 분석/추천 점수 고도화와 업로드 히스토리 연결, 로그인 없는 로컬 단일 사용자 모드 전환, 위시리스트 상세화, Pretendard 기반 프론트 비주얼 리프레시, 추천 저장 상태 연결, 추천 페이지 hydration mismatch 수정, 프론트 로컬 안정 실행 스크립트 추가, stale 업로드 상태 자동 복구, 위시리스트 파일 영속 저장, 위시리스트 정렬 옵션 추가, 업로드 화면 레퍼런스형 리디자인, 업로드 드래그앤드롭 추가까지 완료됐습니다.

1. 저장소 문서 확인: `README.md`, `AGENTS.md`, `TODO.md`
2. 최신 PLAN 확인: `PLAN/PLAN-20260420-프론트하이드레이션정합성수정/PLAN.md`
3. API/DDL 초안 확인:
   - `PLAN/PLAN-20260331-MVP초기세팅/TASKS/TSK-0002-아키텍처초안정의/openapi.yaml`
   - `PLAN/PLAN-20260331-MVP초기세팅/TASKS/TSK-0002-아키텍처초안정의/schema.sql`
4. 상세 OpenAPI 확인:
   - `docs/openapi/openapi.yaml`
5. DB 마이그레이션 확인:
   - `backend/migrations/V1__init_schema.sql`
   - `backend/migrations/R__rollback_v1.sql`
6. 백엔드 스캐폴딩 확인:
   - `backend/src/main.py`
   - `backend/src/api/routes/health.py`
   - `backend/pyproject.toml`
   - `backend/scripts/run-dev.sh`
7. API 통합 테스트 확인:
   - `backend/tests/test_api_e2e.py`
   - 실행: `cd backend && PYTHONPATH=. python3 -m pytest tests -q`
8. CI 테스트 워크플로우 확인:
   - `.github/workflows/backend-tests.yml`
   - `backend/requirements-test.txt`
9. 프론트 스캐폴딩 확인:
   - `frontend/app/(auth)/login/page.tsx` (`/upload`로 즉시 리다이렉트)
   - `frontend/app/(main)/upload/page.tsx`
   - `frontend/app/(main)/recommendations/page.tsx`
   - `frontend/app/(main)/wishlist/page.tsx`
   - `frontend/components/app-shell.tsx`
   - 권장 실행: `cd frontend && npm run local`
10. 프론트 API 연동 확인:
   - `frontend/lib/api.ts`
   - 업로드 이미지 ID 저장 키: `stylematch_uploaded_image_id`
11. 프론트 보안 업그레이드 확인:
   - `frontend/package.json`
   - `frontend/package-lock.json`
   - `next@15.5.15`
12. 프론트 E2E 테스트 확인:
   - `frontend/playwright.config.ts`
   - `frontend/e2e/core-flow.spec.ts`
   - 실행: `cd frontend && npm run test:e2e`
13. 프론트 E2E CI 확인:
   - `.github/workflows/frontend-e2e.yml`
14. 브랜치 보호 준비 확인:
   - `.github/branch-protection/main.json`
   - `scripts/apply-branch-protection.sh`
   - `docs/github-branch-protection.md`
15. 브랜치 보호 적용 상태 확인:
   - GitHub 저장소 `dyjeong1/style-finder`의 `main` 브랜치에 보호 규칙 적용 완료
   - required check: `Backend Tests / test`, `Frontend E2E / e2e`
16. 브랜치 보호 실검증 확인:
   - PR #1: `https://github.com/dyjeong1/style-finder/pull/1`
   - `pull_request` 기준 백엔드/프론트 required check 생성 확인
17. GitHub Actions Node 24 대응 확인:
   - `actions/checkout@v5`
   - `actions/setup-python@v6`
   - `actions/setup-node@v5`
   - `actions/upload-artifact@v6`
18. 브랜치 보호 운영 정책 메모:
   - 현재 단독 운영 저장소 기준으로 리뷰 승인 수는 `0`
   - required check는 유지하고 승인 병목만 제거
19. required check 정합성 메모:
   - required check는 `Backend Tests / test (pull_request)`, `Frontend E2E / e2e (pull_request)` 기준으로 조정
20. 업로드 분석/추천 점수 메모:
   - 업로드 응답에 `analysis` 요약이 포함됨
   - 추천 응답은 upload feature vector 기반 `score_breakdown`과 `matched_signals`를 포함함
21. 프론트 분석 노출 메모:
   - `/upload`에서 업로드 직후 Quick Analysis 확인 가능
   - `/recommendations`에서 Upload Analysis와 상품별 score breakdown 확인 가능
22. 업로드 히스토리 메모:
   - `/upload`의 Recent 목록이 실제 최근 업로드 기록과 연결됨
   - 이전 업로드를 선택해 추천 페이지로 바로 이동 가능
23. 단일 사용자 모드 메모:
   - 백엔드 업로드/추천/찜 API는 로그인 없이 바로 호출 가능
   - 위시리스트는 로컬 단일 사용자 기준으로 저장됨
24. 위시리스트 상세화 메모:
   - 위시리스트 응답에 상품명, 가격, 쇼핑몰, 카테고리, 링크가 포함됨
   - 저장 시각이 재조회 후에도 유지됨
   - 카드형 썸네일 UI와 이미지 실패 시 대체 썸네일이 적용됨
25. 프론트 비주얼 리프레시 메모:
   - Pretendard가 전역 폰트로 적용됨
   - 공통 네비게이션과 배경이 유리 질감/웜 톤 중심으로 정리됨
   - 업로드/추천/위시리스트 화면에 페이지 헤더와 카드 썸네일 위계가 강화됨
26. 추천 저장 상태 연결 메모:
   - 추천 카드에서 이미 저장된 상품에 `Saved` 배지가 표시됨
   - 저장된 상품은 버튼이 비활성화되어 중복 찜을 막음
   - 저장 직후 추천 화면 요약과 카드 상태가 즉시 갱신됨
27. 프론트 하이드레이션 정합성 메모:
   - 추천 페이지는 localStorage 값을 mount 이후에만 읽도록 변경됨
   - SSR/CSR 초기 DOM 차이를 줄여 hydration mismatch를 방지함
28. 프론트 로컬 실행 안정화 메모:
   - `npm run local`이 `build + start --hostname 127.0.0.1 --port 3000`를 한 번에 실행함
   - 로컬 화면 확인은 `next dev`보다 `npm run local`을 기본 경로로 권장함
29. 추천 stale 업로드 상태 복구 메모:
   - 백엔드 재시작 후 이전 `uploaded_image_id`가 남아 있어도 추천 페이지가 치명적으로 깨지지 않음
   - stale 업로드 상태를 자동 초기화하고 `/upload` 재업로드를 안내함
30. 위시리스트 영속 저장 메모:
   - 위시리스트는 `backend/data/wishlist.json`에 자동 저장됨
   - 백엔드 재시작 후에도 Saved 상태와 위시리스트 목록이 유지됨
31. 위시리스트 정렬 메모:
   - 위시리스트에서 `latest`, `oldest`, `price_asc`, `price_desc`, `name_asc` 정렬을 지원함
   - 정렬 변경은 추가 API 호출 없이 프론트에서 즉시 반영됨
32. 업로드 화면 리디자인 메모:
   - `/upload`는 큰 인트로 패널, 독립된 드롭존, 우측 최근 업로드 패널 구조로 재구성됨
   - 메인 CTA는 `이미지 분석하기` 버튼으로 강조되고, 최근 업로드 카드는 더 큰 썸네일/버튼 구성을 사용함
33. 업로드 드래그앤드롭 메모:
   - 드롭존에 이미지 파일을 끌어다 놓아 바로 선택할 수 있음
   - 드래그 중에는 드롭존이 강조 색상과 그림자로 활성 상태를 보여줌
34. 업로드 문구 단순화 메모:
   - 업로드 화면의 영어 배지와 보조 문구를 제거해 첫 화면을 더 간결하게 정리함
   - 최근 업로드는 버튼 대신 카드 전체를 눌러 재사용하는 흐름으로 단순화함
   - 메인 타이틀 폰트 크기를 낮춰 상단 헤드라인의 시각적 무게를 줄임
35. 프론트 폰트 단위 pt 전환 메모:
   - `frontend/app/globals.css`의 `font-size` 선언을 pt 기준으로 정리함
   - 업로드 화면 메인 타이틀은 요청값인 `36pt`로 고정함
   - 남아 있던 반응형 `clamp(...)` font-size는 모두 제거하고 고정 pt 값으로 통일함
   - 이후 업로드 화면 메인 타이틀은 `30pt`, CTA 버튼은 `14pt`와 더 작은 박스로 추가 조정함
36. 업로드 영역 통합 UX 메모:
   - 업로드 선택 영역과 미리보기 영역을 하나의 박스로 통합함
   - 선택한 이미지는 같은 영역 안에서 정사각형 미리보기로 노출됨
   - 삭제 버튼으로 선택 파일, 미리보기, 상태 메시지를 즉시 초기화할 수 있음
   - 통합 박스 안에서는 업로드 카피를 상단, 정사각형 미리보기는 하단으로 배치해 읽는 순서를 정리함
   - 안내 문구는 `클릭하거나 이미지를 끌어다 놓아 주세요.`로 다듬어 톤을 정리함
37. 브랜드 아이콘 교체 메모:
   - 좌측 상단 헤더 브랜드 마크를 제공된 로고 이미지로 교체함
   - 로고 자산은 `frontend/public/brand/stylefinder_logo.png`로 정리함
38. 헤더 상태 표시 정리 메모:
   - 우측 상단 `Local Mode` 배지를 제거함
   - 업로드 보조 문구를 `이미지를 넣으면 유사한 상품을 추천해드립니다.`로 변경함
   - 업로드 박스에 `PNG, JPG, JPEG, WEBP` 허용 형식 안내를 추가함
39. 업로드 안내 및 최근 기록 정리 메모:
   - 허용 형식 문구를 이미지 placeholder 자리로 이동함
   - 최근 업로드 카드별 `삭제` 버튼을 추가함
   - 삭제 대상이 현재 저장된 업로드면 관련 localStorage 상태도 함께 정리함

---

## 1. 프로젝트 소개

패션 이미지를 보고 “이 코디와 비슷한 옷을 어디서 살 수 있지?”라는 니즈는 많지만, 실제로는 사용자가 여러 쇼핑몰을 오가며 직접 검색해야 합니다.  
이 서비스는 코디 이미지를 기반으로 유사한 상품을 자동으로 탐색하고, 상품을 카테고리별로 나누어 추천함으로써 탐색 시간을 줄이고 구매 전환 가능성을 높이는 것을 목표로 합니다.

### 핵심 가치
- 코디 이미지 한 장으로 유사 상품 탐색
- 쇼핑몰 검색 시간을 줄이는 빠른 추천 경험
- 코디를 아이템 단위로 나누어 더 실용적인 결과 제공
- 개인이 사용하는 Private 웹 서비스로 가볍고 집중도 높은 운영 가능

---

## 2. 주요 기능

### 2.1 코디/착장 이미지 업로드
- 사용자가 코디 또는 착장 이미지를 업로드
- 업로드된 이미지를 기반으로 스타일 및 의류 요소 분석
- 웹 환경에서 간단하게 업로드 가능한 UX 제공

### 2.2 유사 상품 추천
- 업로드한 이미지와 유사한 의류 상품을 지그재그와 29CM에서 탐색
- 이미지 유사도 기반으로 추천 결과 생성
- 사용자가 직접 검색어를 입력하지 않아도 추천 결과 확인 가능

### 2.3 카테고리별 상품 분류
추천 상품을 다음과 같은 카테고리로 나누어 표시합니다.
- 상의
- 하의
- 아우터
- 신발
- 가방
- 기타 액세서리(확장 가능)

### 2.4 유사도순 정렬
- 추천 상품은 기본적으로 유사도순으로 정렬
- 사용자는 가장 비슷한 상품부터 확인 가능

### 2.5 가격대 필터
- 최소 가격 ~ 최대 가격 범위 설정 가능
- 예산에 맞는 상품만 빠르게 필터링 가능

### 2.6 찜 기능
- 마음에 드는 상품을 찜 목록에 저장
- 찜한 상품만 따로 모아 다시 확인 가능
- 로컬 단일 사용자 기준 저장 기능 제공

---

## 3. 플랫폼 및 서비스 범위

### 플랫폼
- 웹(Web)

### 서비스 범위
- Private 서비스
- 로그인 절차 없이 로컬 단일 사용자가 바로 이용 가능
- 퍼블릭 오픈 서비스가 아닌 내부/개인용 운영을 전제로 설계

---

## 4. 타겟 사용자

- SNS, 커뮤니티, 룩북 등에서 본 코디와 비슷한 상품을 빠르게 찾고 싶은 사용자
- 여러 쇼핑몰을 직접 검색하는 과정이 번거로운 사용자
- 코디 전체가 아니라 아이템 단위로 쇼핑하고 싶은 사용자
- 개인용 또는 소규모 테스트 환경에서 서비스를 운영하려는 관리자

---

## 5. 사용자 흐름

1. 사용자가 웹 서비스에 접속
2. 코디/착장 이미지를 업로드
3. 시스템이 이미지 속 패션 아이템을 분석
4. 지그재그와 29CM에서 유사 상품을 탐색
5. 추천 결과를 카테고리별로 분류하여 표시
6. 사용자는 유사도순으로 상품을 확인
7. 가격대 필터를 적용해 결과를 좁힘
8. 원하는 상품을 찜 목록에 저장
9. 찜 페이지에서 저장한 상품을 다시 확인

---

## 6. 서비스 화면 구성 예시

### 6.1 메인/업로드 페이지
- 서비스 소개
- 이미지 업로드 영역
- 최근 업로드 이력 또는 예시 이미지 노출 가능

### 6.2 추천 결과 페이지
- 원본 업로드 이미지 표시
- 카테고리 탭(상의/하의/아우터/신발/가방 등)
- 유사도순 정렬 결과
- 가격대 필터 UI
- 상품 카드(이미지, 상품명, 가격, 쇼핑몰명, 링크, 찜 버튼)

### 6.3 찜 목록 페이지
- 찜한 상품 리스트
- 카테고리별 보기
- 쇼핑몰별 보기
- 찜 해제 기능

### 6.4 로그인/사용자 관리 페이지
- 별도 로그인 없이 바로 사용하는 로컬 모드 안내
- 업로드 이력과 찜 흐름 중심의 단순 사용성 유지

---

## 7. 추천 로직 개요

서비스는 다음 흐름으로 동작합니다.

1. **이미지 업로드**
   - 사용자가 코디 이미지를 업로드합니다.

2. **이미지 분석**
   - 이미지 내 주요 패션 아이템을 식별합니다.
   - 필요 시 상의/하의/아우터/신발/가방 등으로 카테고리 분류를 수행합니다.

3. **특징 추출**
   - 이미지 임베딩 또는 비전 모델을 활용해 스타일 특징을 벡터화합니다.

4. **상품 데이터 탐색**
   - 지그재그와 29CM의 상품 이미지 및 메타데이터를 기반으로 유사 상품을 검색합니다.

5. **유사도 계산 및 랭킹**
   - 시각적 유사도, 카테고리 일치 여부, 가격 정보 등을 반영해 결과를 정렬합니다.

6. **결과 제공**
   - 카테고리별로 상품을 나누어 보여주고, 가격 필터 및 찜 기능을 제공합니다.

---

## 8. 기술 구성 예시

아래는 구현 시 고려할 수 있는 예시 스택입니다.

### 프론트엔드
- Next.js
- React
- TypeScript

### 백엔드
- FastAPI 또는 NestJS
- REST API 기반 서비스 구성

### AI / 추천
- CLIP 계열 이미지 임베딩 모델
- 패션 특화 분류/검출 모델
- 유사도 검색을 위한 벡터 검색 로직

### 데이터 저장
- PostgreSQL
- pgvector 또는 별도 벡터 검색 엔진
- Redis(캐시, 세션 등)

### 파일 저장
- AWS S3 또는 이에 준하는 오브젝트 스토리지

### 접근 제어
- 로컬 단일 사용자 모드
- 필요 시 추후 이메일 로그인 또는 OAuth 확장 가능

---

## 9. 핵심 데이터 구조 예시

### LocalUser
- id
- mode (`single-user`)
- created_at

### UploadedImage
- id
- user_id
- image_url
- created_at

### Product
- id
- source (`zigzag`, `29cm`)
- product_name
- category
- price
- product_url
- image_url
- embedding
- updated_at

### RecommendationResult
- id
- uploaded_image_id
- product_id
- category
- similarity_score
- rank

### Wishlist
- id
- user_id
- product_id
- created_at

---

## 10. MVP 범위

초기 버전에서는 아래 기능에 집중합니다.

- 코디 이미지 1장 업로드
- 지그재그 / 29CM 기반 유사 상품 추천
- 카테고리별 결과 분류
- 유사도순 정렬
- 가격대 필터
- 찜 기능
- 로그인 없는 로컬 단일 사용자 모드

---

## 11. 향후 확장 아이디어

- 색상/브랜드/스타일 태그 필터
- 유사 상품 외에 “같이 코디하면 좋은 상품” 추천
- 사용자 취향 기반 개인화 추천
- 검색 결과 저장 및 히스토리 관리
- 상품 품절 여부 반영
- 남성/여성/유니섹스 스타일 구분
- 모바일 웹 최적화
- 브라우저 확장 또는 저장 링크 기반 추천 기능

---

## 12. 운영 시 고려사항

### 외부 쇼핑몰 연동
지그재그와 29CM의 상품 데이터를 활용할 때는 반드시 다음을 확인해야 합니다.
- 공식 API 제공 여부
- 제휴 가능 여부
- 이용약관 및 robots 정책
- 허용된 범위 내 데이터 수집/노출 정책

### 개인정보 및 이미지 처리
- 업로드 이미지는 필요한 범위 내에서만 저장
- 사용자 이미지 삭제 기능 제공 권장
- 접근 제어 및 저장 데이터 암호화 고려

### 추천 품질
- 단순 이미지 유사도만으로는 정확도가 떨어질 수 있으므로
  카테고리 분류, 색상, 실루엣, 패턴 등의 보조 신호를 함께 반영하는 방식이 바람직합니다.

---

## 13. 기대 효과

- 사용자는 코디 이미지 한 장으로 빠르게 쇼핑 가능한 상품을 찾을 수 있습니다.
- 여러 쇼핑몰을 오가며 검색하는 시간을 줄일 수 있습니다.
- 코디 단위 이미지를 실제 구매 가능한 아이템 단위 결과로 연결할 수 있습니다.
- Private 환경에서 먼저 추천 품질과 사용자 경험을 검증할 수 있습니다.

---

## 14. 한 줄 요약

**스타일매치는 로그인 없이 코디 이미지를 업로드하면, 지그재그와 29CM에서 유사한 의류 상품을 카테고리별로 추천해주는 개인용 웹 서비스입니다.**
