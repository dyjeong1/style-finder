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
- `PLAN-20260416-단일사용자모드전환`
- 상세 문서: `PLAN/PLAN-20260416-단일사용자모드전환/PLAN.md`
- 기술 스펙: `PLAN/PLAN-20260416-단일사용자모드전환/SPEC.md`
- 상태: `doing` (백엔드 단일 사용자 모드 전환 완료, 프론트 인증 제거 진행 중, 2026-04-16)

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
현재는 백엔드 기초, 프론트 MVP, E2E CI, `main` 브랜치 보호 규칙 적용, PR 기준 required check 실동작 검증, GitHub Actions Node 24 대응, solo 운영 기준 브랜치 보호 정책 정리, required check 이름 정합성 수정, 업로드 이미지 분석/추천 점수 고도화와 업로드 히스토리 연결, 로컬 로그인 CORS 오류 수정, 백엔드 단일 사용자 모드 전환까지 완료된 상태입니다.

1. 저장소 문서 확인: `README.md`, `AGENTS.md`, `TODO.md`
2. 최신 PLAN 확인: `PLAN/PLAN-20260416-단일사용자모드전환/PLAN.md`
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
   - `frontend/app/(auth)/login/page.tsx`
   - `frontend/app/(main)/upload/page.tsx`
   - `frontend/app/(main)/recommendations/page.tsx`
   - `frontend/app/(main)/wishlist/page.tsx`
   - `frontend/components/app-shell.tsx`
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
- 사용자별 개인 저장 기능 제공

---

## 3. 플랫폼 및 서비스 범위

### 플랫폼
- 웹(Web)

### 서비스 범위
- Private 서비스
- 승인된 사용자 또는 제한된 사용자만 접근 가능
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
- Private 서비스 접근 제어
- 사용자 인증
- 권한 관리(선택)

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

### 인증
- 이메일 로그인
- OAuth 또는 초대 기반 접근 제어

---

## 9. 핵심 데이터 구조 예시

### User
- id
- email
- password_hash / oauth_id
- role
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
- 로그인 기반 Private 접근 제어

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

**스타일매치는 코디 이미지를 업로드하면, 지그재그와 29CM에서 유사한 의류 상품을 카테고리별로 추천해주는 Private 웹 서비스입니다.**
