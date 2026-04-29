"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";

import { getWishlist, removeWishlist, WishlistItem } from "@/lib/api";

type WishlistSortOption = "latest" | "oldest" | "price_asc" | "price_desc" | "name_asc";

const CATEGORY_LABELS: Record<string, string> = {
  top: "상의",
  bottom: "하의",
  outer: "아우터",
  shoes: "신발",
  bag: "가방",
  accessory: "악세서리",
};

const SORT_LABELS: Record<WishlistSortOption, string> = {
  latest: "최신순",
  oldest: "오래된 순",
  price_asc: "가격 낮은 순",
  price_desc: "가격 높은 순",
  name_asc: "이름순",
};

function buildWishlistFallbackImage(item: WishlistItem): string {
  const title = item.product_name.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const subtitle = `${item.source.toUpperCase()} / ${item.category.toUpperCase()}`;
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="320" height="220" viewBox="0 0 320 220">
      <defs>
        <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="#f3e2b8" />
          <stop offset="100%" stop-color="#e8c88f" />
        </linearGradient>
      </defs>
      <rect width="320" height="220" rx="24" fill="url(#g)" />
      <rect x="18" y="18" width="284" height="184" rx="18" fill="rgba(255,255,255,0.55)" />
      <text x="30" y="66" fill="#7c2d12" font-family="Pretendard, Arial, sans-serif" font-size="18" font-weight="700">${subtitle}</text>
      <text x="30" y="108" fill="#111827" font-family="Pretendard, Arial, sans-serif" font-size="26" font-weight="700">${title}</text>
      <text x="30" y="152" fill="#4b5563" font-family="Pretendard, Arial, sans-serif" font-size="16">Saved in StyleMatch</text>
    </svg>
  `;

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

function resolveWishlistImage(item: WishlistItem): string {
  if (!item.image_url || item.image_url.includes("example.com/")) {
    return buildWishlistFallbackImage(item);
  }

  return item.image_url;
}

export default function WishlistPage() {
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [category, setCategory] = useState("");
  const [sort, setSort] = useState<WishlistSortOption>("latest");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const sortedItems = useMemo(() => {
    const nextItems = [...items];

    if (sort === "oldest") {
      nextItems.sort((left, right) => new Date(left.created_at).getTime() - new Date(right.created_at).getTime());
      return nextItems;
    }

    if (sort === "price_asc") {
      nextItems.sort((left, right) => left.price - right.price);
      return nextItems;
    }

    if (sort === "price_desc") {
      nextItems.sort((left, right) => right.price - left.price);
      return nextItems;
    }

    if (sort === "name_asc") {
      nextItems.sort((left, right) => left.product_name.localeCompare(right.product_name, "ko-KR"));
      return nextItems;
    }

    nextItems.sort((left, right) => new Date(right.created_at).getTime() - new Date(left.created_at).getTime());
    return nextItems;
  }, [items, sort]);

  async function loadWishlist() {
    setLoading(true);
    setErrorMessage(null);

    try {
      const result = await getWishlist(category || undefined);
      setItems(result.items);
      setTotalCount(result.total_count);
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 목록 조회 중 오류가 발생했습니다.";
      setErrorMessage(message);
      setItems([]);
      setTotalCount(0);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    document.title = "스타일매치 | 위시리스트";
    void loadWishlist();
  }, [category]);

  async function handleRemove(productId: string) {
    try {
      await removeWishlist(productId);
      setItems((prev) => prev.filter((item) => item.product_id !== productId));
      setTotalCount((prev) => Math.max(0, prev - 1));
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 해제 중 오류가 발생했습니다.";
      setErrorMessage(message);
    }
  }

  return (
    <section className="card wishlist-shell" aria-labelledby="wishlist-title" aria-busy={loading}>
      <div className="page-header page-header-soft">
        <p className="eyebrow">위시리스트</p>
        <div className="page-title-row">
          <div>
            <h1 id="wishlist-title">찜 목록</h1>
            <p className="lead page-lead">저장해둔 상품을 다시 확인하고 바로 쇼핑몰 링크로 이동할 수 있습니다.</p>
          </div>
          <div className="page-summary-grid compact-summary-grid">
            <div className="summary-pill">
              <span className="summary-label">상품 수</span>
              <strong>{totalCount}</strong>
            </div>
            <div className="summary-pill">
              <span className="summary-label">필터</span>
              <strong>{category ? CATEGORY_LABELS[category] ?? category : "전체"}</strong>
            </div>
            <div className="summary-pill">
              <span className="summary-label">정렬</span>
              <strong>{SORT_LABELS[sort]}</strong>
            </div>
          </div>
        </div>
      </div>
      <div className="action-row wishlist-toolbar">
        <label className="control-field" htmlFor="wishlist-category">
          <span className="field-label">카테고리</span>
          <select id="wishlist-category" value={category} onChange={(event) => setCategory(event.target.value)}>
            <option value="">전체</option>
            <option value="top">상의</option>
            <option value="bottom">하의</option>
            <option value="outer">아우터</option>
            <option value="shoes">신발</option>
            <option value="bag">가방</option>
            <option value="accessory">악세서리</option>
          </select>
        </label>
        <label className="control-field" htmlFor="wishlist-sort">
          <span className="field-label">정렬</span>
          <select id="wishlist-sort" value={sort} onChange={(event) => setSort(event.target.value as WishlistSortOption)}>
            <option value="latest">최신순</option>
            <option value="oldest">오래된 순</option>
            <option value="price_asc">가격 낮은 순</option>
            <option value="price_desc">가격 높은 순</option>
            <option value="name_asc">이름순</option>
          </select>
        </label>
        <button type="button" className="ghost-button" onClick={() => void loadWishlist()}>
          새로고침
        </button>
      </div>
      <div className="status-region" aria-live="polite" aria-atomic="true">
        {loading ? (
          <p className="lead" role="status">
            찜 목록을 불러오는 중입니다...
          </p>
        ) : null}
        {errorMessage ? (
          <p className="error-text" role="alert">
            {errorMessage}
          </p>
        ) : null}
      </div>
      <ul className="wishlist-list" aria-label="찜 목록">
        {sortedItems.map((item) => (
          <li key={item.id}>
            <div className="wishlist-thumbnail-wrap">
              <img
                src={resolveWishlistImage(item)}
                alt={`${item.product_name} 썸네일`}
                className="wishlist-thumbnail"
                onError={(event) => {
                  event.currentTarget.onerror = null;
                  event.currentTarget.src = buildWishlistFallbackImage(item);
                }}
              />
            </div>
            <div className="wishlist-card-body">
              <div className="wishlist-meta">
                <span className="badge">{item.category.toUpperCase()}</span>
                <span className="wishlist-source">{item.source.toUpperCase()}</span>
              </div>
              <strong>{item.product_name}</strong>
              <p className="wishlist-price">{item.price.toLocaleString("ko-KR")}원</p>
              <p className="hint-text">저장 일시 {new Date(item.created_at).toLocaleString("ko-KR")}</p>
              <div className="wishlist-right">
                <a className="product-link" href={item.product_url} target="_blank" rel="noreferrer">
                  상품 보기
                </a>
                <button type="button" aria-label={`${item.product_id} 찜 해제`} onClick={() => handleRemove(item.product_id)}>
                  삭제
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
      {!loading && items.length === 0 && !errorMessage ? (
        <div className="empty-box soft-empty-box">
          <p className="lead">저장된 찜 상품이 없습니다.</p>
          <p className="hint-text">
            <Link href="/recommendations">추천 페이지</Link>에서 마음에 드는 상품을 추가해보세요.
          </p>
        </div>
      ) : null}
    </section>
  );
}
