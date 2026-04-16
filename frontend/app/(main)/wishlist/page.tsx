"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { getWishlist, removeWishlist, WishlistItem } from "@/lib/api";

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
      <text x="30" y="66" fill="#7c2d12" font-family="Arial, sans-serif" font-size="18" font-weight="700">${subtitle}</text>
      <text x="30" y="108" fill="#111827" font-family="Arial, sans-serif" font-size="26" font-weight="700">${title}</text>
      <text x="30" y="152" fill="#4b5563" font-family="Arial, sans-serif" font-size="16">Saved in StyleMatch</text>
    </svg>
  `;

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

export default function WishlistPage() {
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function loadWishlist() {
    setLoading(true);
    setErrorMessage(null);

    try {
      const result = await getWishlist(category || undefined);
      setItems(result.items);
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 목록 조회 중 오류가 발생했습니다.";
      setErrorMessage(message);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadWishlist();
  }, [category]);

  async function handleRemove(productId: string) {
    try {
      await removeWishlist(productId);
      setItems((prev) => prev.filter((item) => item.product_id !== productId));
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 해제 중 오류가 발생했습니다.";
      setErrorMessage(message);
    }
  }

  return (
    <section className="card" aria-labelledby="wishlist-title" aria-busy={loading}>
      <p className="eyebrow">Saved Items</p>
      <h1 id="wishlist-title">Wishlist</h1>
      <div className="action-row">
        <label className="control-field" htmlFor="wishlist-category">
          <span className="sr-only">찜 카테고리 필터</span>
          <select id="wishlist-category" value={category} onChange={(event) => setCategory(event.target.value)}>
            <option value="">All Category</option>
            <option value="top">Top</option>
            <option value="bottom">Bottom</option>
            <option value="outer">Outer</option>
            <option value="shoes">Shoes</option>
            <option value="bag">Bag</option>
          </select>
        </label>
        <button type="button" className="ghost-button" onClick={() => void loadWishlist()}>
          Refresh
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
        {items.map((item) => (
          <li key={item.id}>
            <div className="wishlist-thumbnail-wrap">
              <img
                src={item.image_url}
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
              <p className="hint-text">saved {new Date(item.created_at).toLocaleString("ko-KR")}</p>
              <div className="wishlist-right">
                <a className="product-link" href={item.product_url} target="_blank" rel="noreferrer">
                  상품 보기
                </a>
                <button type="button" aria-label={`${item.product_id} 찜 해제`} onClick={() => handleRemove(item.product_id)}>
                  Remove
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
      {!loading && items.length === 0 && !errorMessage ? (
        <div className="empty-box">
          <p className="lead">저장된 찜 상품이 없습니다.</p>
          <p className="hint-text">
            <Link href="/recommendations">추천 페이지</Link>에서 마음에 드는 상품을 추가해보세요.
          </p>
        </div>
      ) : null}
    </section>
  );
}
