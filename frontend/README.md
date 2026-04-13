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

## 주요 라우트
- `/login`
- `/upload`
- `/recommendations`
- `/wishlist`

## API 베이스 URL
- 환경변수: `NEXT_PUBLIC_API_BASE_URL`
- 기본값: `http://localhost:8000`

## 현재 연결된 API 흐름
- `/login`: `POST /auth/login` 호출 후 토큰을 `stylematch_access_token`에 저장
- `/upload`: `POST /images/upload` 호출 후 업로드 ID를 `stylematch_uploaded_image_id`에 저장
- `/recommendations`: `GET /recommendations` 조회 및 `POST /wishlist` 찜 추가
- `/wishlist`: `GET /wishlist` 조회 및 `DELETE /wishlist/{product_id}` 찜 삭제
