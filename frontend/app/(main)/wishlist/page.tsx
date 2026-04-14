"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";

import { getStoredToken, getWishlist, removeWishlist, WishlistItem } from "@/lib/api";

export default function WishlistPage() {
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const token = useMemo(() => getStoredToken(), []);

  async function loadWishlist() {
    if (!token) {
      setErrorMessage("로그인이 필요합니다. /login에서 먼저 로그인해주세요.");
      setItems([]);
      return;
    }

    setLoading(true);
    setErrorMessage(null);

    try {
      const result = await getWishlist(token, category || undefined);
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
    if (!token) {
      setErrorMessage("로그인이 필요합니다.");
      return;
    }

    try {
      await removeWishlist(productId, token);
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
            <div>
              <strong>{item.product_id}</strong>
              <p>{new Date(item.created_at).toLocaleString("ko-KR")}</p>
            </div>
            <div className="wishlist-right">
              <button type="button" aria-label={`${item.product_id} 찜 해제`} onClick={() => handleRemove(item.product_id)}>
                Remove
              </button>
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
