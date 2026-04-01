# Backend Migrations

## 파일 규칙
- `V{버전}__설명.sql`: 순방향 마이그레이션
- `R__rollback_{버전}.sql`: 롤백 초안

## 현재 상태
- `V1__init_schema.sql`: 초기 테이블/인덱스/제약조건 생성
- `R__rollback_v1.sql`: V1 롤백 초안

## 적용 예시 (psql)
```bash
psql "$DATABASE_URL" -f backend/migrations/V1__init_schema.sql
```

## 롤백 예시 (주의)
```bash
psql "$DATABASE_URL" -f backend/migrations/R__rollback_v1.sql
```
