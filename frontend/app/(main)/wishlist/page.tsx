"use client";

import { useEffect, useMemo, useState } from "react";

import { getStoredToken, getWishlist, removeWishlist, WishlistItem } from "@/lib/api";

export default function WishlistPage() {
  const [items, setItems] = useState<WishlistItem[]>([]);
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
      const result = await getWishlist(token);
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
  }, []);

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
    <section className="card">
      <p className="eyebrow">Saved Items</p>
      <h1>Wishlist</h1>
      {loading ? <p className="lead">찜 목록을 불러오는 중입니다...</p> : null}
      {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
      <ul className="wishlist-list">
        {items.map((item) => (
          <li key={item.id}>
            <div>
              <strong>{item.product_id}</strong>
              <p>{new Date(item.created_at).toLocaleString("ko-KR")}</p>
            </div>
            <div className="wishlist-right">
              <button type="button" onClick={() => handleRemove(item.product_id)}>
                Remove
              </button>
            </div>
          </li>
        ))}
      </ul>
      {!loading && items.length === 0 && !errorMessage ? <p className="lead">저장된 찜 상품이 없습니다.</p> : null}
    </section>
  );
}
