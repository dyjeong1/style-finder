"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";

import {
  addWishlist,
  getRecommendations,
  getStoredToken,
  getStoredUploadedImageId,
  RecommendationItem,
} from "@/lib/api";

type SortOption = "similarity_desc" | "price_asc" | "price_desc";

export default function RecommendationPage() {
  const [items, setItems] = useState<RecommendationItem[]>([]);
  const [category, setCategory] = useState("");
  const [sort, setSort] = useState<SortOption>("similarity_desc");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);

  const token = useMemo(() => getStoredToken(), []);
  const uploadedImageId = useMemo(() => getStoredUploadedImageId(), []);

  async function loadRecommendations() {
    if (!token) {
      setErrorMessage("로그인이 필요합니다. /login에서 먼저 로그인해주세요.");
      setItems([]);
      return;
    }

    if (!uploadedImageId) {
      setErrorMessage("업로드된 이미지가 없습니다. /upload에서 이미지를 먼저 올려주세요.");
      setItems([]);
      return;
    }

    setLoading(true);
    setErrorMessage(null);

    try {
      const result = await getRecommendations(
        {
          uploadedImageId,
          category: category || undefined,
          sort,
          minPrice: minPrice ? Number(minPrice) : undefined,
          maxPrice: maxPrice ? Number(maxPrice) : undefined,
        },
        token,
      );
      setItems(result.items);
    } catch (error) {
      const message = error instanceof Error ? error.message : "추천 조회 중 오류가 발생했습니다.";
      setErrorMessage(message);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadRecommendations();
  }, [category, sort, minPrice, maxPrice]);

  function resetFilters() {
    setCategory("");
    setSort("similarity_desc");
    setMinPrice("");
    setMaxPrice("");
  }

  async function handleAddWishlist(productId: string) {
    if (!token) {
      setErrorMessage("로그인이 필요합니다.");
      return;
    }

    setFeedbackMessage(null);
    try {
      await addWishlist(productId, token);
      setFeedbackMessage(`상품이 찜 목록에 추가되었습니다: ${productId}`);
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 추가 중 오류가 발생했습니다.";
      setErrorMessage(message);
    }
  }

  return (
    <section className="card">
      <p className="eyebrow">Step 2</p>
      <h1>Recommendations</h1>
      <div className="filter-row">
        <select value={category} onChange={(event) => setCategory(event.target.value)}>
          <option value="">All Category</option>
          <option value="top">Top</option>
          <option value="bottom">Bottom</option>
          <option value="outer">Outer</option>
          <option value="shoes">Shoes</option>
          <option value="bag">Bag</option>
        </select>
        <select value={sort} onChange={(event) => setSort(event.target.value as SortOption)}>
          <option value="similarity_desc">Similarity Desc</option>
          <option value="price_asc">Price Asc</option>
          <option value="price_desc">Price Desc</option>
        </select>
        <input
          type="number"
          min={0}
          placeholder="Min Price"
          value={minPrice}
          onChange={(event) => setMinPrice(event.target.value)}
        />
        <input
          type="number"
          min={0}
          placeholder="Max Price"
          value={maxPrice}
          onChange={(event) => setMaxPrice(event.target.value)}
        />
      </div>
      <div className="action-row">
        <button type="button" className="ghost-button" onClick={() => void loadRecommendations()}>
          Refresh
        </button>
        <button type="button" className="ghost-button" onClick={resetFilters}>
          Reset Filters
        </button>
      </div>

      {loading ? <p className="lead">추천 결과를 불러오는 중입니다...</p> : null}
      {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
      {feedbackMessage ? <p className="success-text">{feedbackMessage}</p> : null}

      <div className="card-grid">
        {loading
          ? Array.from({ length: 4 }).map((_, idx) => (
              <article className="product-card skeleton-card" key={`skeleton-${idx}`}>
                <div className="skeleton-line skeleton-title" />
                <div className="skeleton-line" />
                <div className="skeleton-line skeleton-short" />
              </article>
            ))
          : null}
        {items.map((item) => (
          <article className="product-card" key={item.product_id}>
            <div className="badge">{item.category.toUpperCase()}</div>
            <h3>{item.product_name}</h3>
            <p>{item.price.toLocaleString("ko-KR")}원</p>
            <small>similarity {item.similarity_score.toFixed(2)}</small>
            <a className="product-link" href={item.product_url} target="_blank" rel="noreferrer">
              상품 보기
            </a>
            <button type="button" onClick={() => handleAddWishlist(item.product_id)}>
              Add to Wishlist
            </button>
          </article>
        ))}
      </div>
      {!loading && items.length === 0 && !errorMessage ? (
        <div className="empty-box">
          <p className="lead">추천 결과가 없습니다.</p>
          <p className="hint-text">
            먼저 <Link href="/upload">업로드</Link>에서 다른 이미지를 올리거나 가격 필터를 완화해보세요.
          </p>
        </div>
      ) : null}
    </section>
  );
}
