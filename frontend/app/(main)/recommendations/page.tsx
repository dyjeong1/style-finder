"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";

import {
  addWishlist,
  getRecommendations,
  getStoredUploadedImageAnalysis,
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

  const uploadedImageId = useMemo(() => getStoredUploadedImageId(), []);
  const uploadedImageAnalysis = useMemo(() => getStoredUploadedImageAnalysis(), []);

  async function loadRecommendations() {
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
    setFeedbackMessage(null);
    try {
      await addWishlist(productId);
      setFeedbackMessage(`상품이 찜 목록에 추가되었습니다: ${productId}`);
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 추가 중 오류가 발생했습니다.";
      setErrorMessage(message);
    }
  }

  return (
    <section className="card" aria-labelledby="recommendations-title" aria-busy={loading}>
      <p className="eyebrow">Step 2</p>
      <h1 id="recommendations-title">Recommendations</h1>
      <div className="filter-row">
        <label className="control-field" htmlFor="recommendation-category">
          <span className="sr-only">카테고리 필터</span>
          <select id="recommendation-category" value={category} onChange={(event) => setCategory(event.target.value)}>
            <option value="">All Category</option>
            <option value="top">Top</option>
            <option value="bottom">Bottom</option>
            <option value="outer">Outer</option>
            <option value="shoes">Shoes</option>
            <option value="bag">Bag</option>
          </select>
        </label>
        <label className="control-field" htmlFor="recommendation-sort">
          <span className="sr-only">정렬 방식</span>
          <select id="recommendation-sort" value={sort} onChange={(event) => setSort(event.target.value as SortOption)}>
            <option value="similarity_desc">Similarity Desc</option>
            <option value="price_asc">Price Asc</option>
            <option value="price_desc">Price Desc</option>
          </select>
        </label>
        <label className="control-field" htmlFor="recommendation-min-price">
          <span className="sr-only">최소 가격</span>
          <input
            id="recommendation-min-price"
            type="number"
            min={0}
            inputMode="numeric"
            placeholder="Min Price"
            value={minPrice}
            onChange={(event) => setMinPrice(event.target.value)}
          />
        </label>
        <label className="control-field" htmlFor="recommendation-max-price">
          <span className="sr-only">최대 가격</span>
          <input
            id="recommendation-max-price"
            type="number"
            min={0}
            inputMode="numeric"
            placeholder="Max Price"
            value={maxPrice}
            onChange={(event) => setMaxPrice(event.target.value)}
          />
        </label>
      </div>
      <div className="action-row">
        <button type="button" className="ghost-button" onClick={() => void loadRecommendations()}>
          Refresh
        </button>
        <button type="button" className="ghost-button" onClick={resetFilters}>
          Reset Filters
        </button>
      </div>

      <div className="status-region" aria-live="polite" aria-atomic="true">
        {loading ? (
          <p className="lead" role="status">
            추천 결과를 불러오는 중입니다...
          </p>
        ) : null}
        {errorMessage ? (
          <p className="error-text" role="alert">
            {errorMessage}
          </p>
        ) : null}
        {feedbackMessage ? (
          <p className="success-text" role="status">
            {feedbackMessage}
          </p>
        ) : null}
      </div>

      {uploadedImageAnalysis ? (
        <section className="analysis-panel compact-analysis" aria-label="업로드 이미지 분석 요약">
          <h2>Upload Analysis</h2>
          <div className="analysis-chip-row">
            <span className="analysis-chip">tone {uploadedImageAnalysis.dominant_tone}</span>
            <span className="analysis-chip">mood {uploadedImageAnalysis.style_mood}</span>
            <span className="analysis-chip">fit {uploadedImageAnalysis.silhouette}</span>
          </div>
          <p className="hint-text">preferred categories: {uploadedImageAnalysis.preferred_categories.join(", ")}</p>
        </section>
      ) : null}

      <div className="card-grid" role="list" aria-label="추천 상품 목록">
        {loading
          ? Array.from({ length: 4 }).map((_, idx) => (
              <article className="product-card skeleton-card" key={`skeleton-${idx}`} aria-hidden="true">
                <div className="skeleton-line skeleton-title" />
                <div className="skeleton-line" />
                <div className="skeleton-line skeleton-short" />
              </article>
            ))
          : null}
        {items.map((item) => (
          <article className="product-card" key={item.product_id} role="listitem">
            <div className="badge">{item.category.toUpperCase()}</div>
            <h3>{item.product_name}</h3>
            <p>{item.price.toLocaleString("ko-KR")}원</p>
            <small>similarity {item.similarity_score.toFixed(2)}</small>
            <div className="signal-list">
              <span>tone {item.matched_signals.dominant_tone}</span>
              <span>mood {item.matched_signals.style_mood}</span>
              <span>fit {item.matched_signals.silhouette}</span>
            </div>
            <dl className="score-breakdown">
              <div>
                <dt>Vector</dt>
                <dd>{item.score_breakdown.vector_similarity.toFixed(2)}</dd>
              </div>
              <div>
                <dt>Tone</dt>
                <dd>+{item.score_breakdown.tone_bonus.toFixed(2)}</dd>
              </div>
              <div>
                <dt>Mood</dt>
                <dd>+{item.score_breakdown.mood_bonus.toFixed(2)}</dd>
              </div>
              <div>
                <dt>Fit</dt>
                <dd>+{item.score_breakdown.silhouette_bonus.toFixed(2)}</dd>
              </div>
            </dl>
            <a className="product-link" href={item.product_url} target="_blank" rel="noreferrer">
              상품 보기
            </a>
            <button type="button" aria-label={`${item.product_name} 찜 추가`} onClick={() => handleAddWishlist(item.product_id)}>
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
