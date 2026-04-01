-- Rollback draft for V1__init_schema.sql
-- WARNING: 데이터가 삭제됩니다.

DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS recommendation_results;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS uploaded_images;
DROP TABLE IF EXISTS users;

-- 운영 환경에서 extension 제거는 신중히 판단한다.
-- DROP EXTENSION IF EXISTS vector;
