-- V1: StyleMatch 초기 스키마
-- 환경: PostgreSQL 15+, pgvector extension

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT,
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE uploaded_images (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY,
    source VARCHAR(20) NOT NULL CHECK (source IN ('zigzag', '29cm')),
    external_product_id VARCHAR(255),
    product_name TEXT NOT NULL,
    category VARCHAR(20) NOT NULL CHECK (category IN ('top', 'bottom', 'outer', 'shoes', 'bag', 'accessory')),
    price INTEGER NOT NULL CHECK (price >= 0),
    product_url TEXT NOT NULL,
    image_url TEXT NOT NULL,
    embedding VECTOR(768),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX uq_products_source_external
    ON products(source, external_product_id)
    WHERE external_product_id IS NOT NULL;

CREATE TABLE recommendation_results (
    id UUID PRIMARY KEY,
    uploaded_image_id UUID NOT NULL REFERENCES uploaded_images(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    category VARCHAR(20) NOT NULL CHECK (category IN ('top', 'bottom', 'outer', 'shoes', 'bag', 'accessory')),
    similarity_score NUMERIC(5,4) NOT NULL CHECK (similarity_score BETWEEN 0 AND 1),
    rank INTEGER NOT NULL CHECK (rank > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(uploaded_image_id, product_id)
);

CREATE INDEX idx_recommendation_uploaded_rank
    ON recommendation_results(uploaded_image_id, rank);

CREATE TABLE wishlist (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, product_id)
);

CREATE INDEX idx_wishlist_user_created
    ON wishlist(user_id, created_at DESC);
