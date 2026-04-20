"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import {
  addWishlist,
  clearStoredUploadedImageAnalysis,
  clearStoredUploadedImageId,
  getRecommendations,
  getStoredUploadedImageAnalysis,
  getStoredUploadedImageId,
  getWishlist,
  RecommendationItem,
} from "@/lib/api";

type SortOption = "similarity_desc" | "price_asc" | "price_desc";

function buildRecommendationFallbackImage(item: RecommendationItem): string {
  const title = item.product_name.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const subtitle = `${item.source.toUpperCase()} / ${item.category.toUpperCase()}`;
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420">
      <defs>
        <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="#f7dfb7" />
          <stop offset="100%" stop-color="#e8b97a" />
        </linearGradient>
      </defs>
      <rect width="640" height="420" rx="36" fill="url(#g)" />
      <rect x="32" y="32" width="576" height="356" rx="28" fill="rgba(255,255,255,0.5)" />
      <text x="60" y="108" fill="#9a3412" font-family="Pretendard, Arial, sans-serif" font-size="28" font-weight="700">${subtitle}</text>
      <text x="60" y="174" fill="#111827" font-family="Pretendard, Arial, sans-serif" font-size="40" font-weight="700">${title}</text>
      <text x="60" y="244" fill="#4b5563" font-family="Pretendard, Arial, sans-serif" font-size="24">Curated by StyleMatch</text>
    </svg>
  `;

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

export default function RecommendationPage() {
  const [items, setItems] = useState<RecommendationItem[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [category, setCategory] = useState("");
  const [sort, setSort] = useState<SortOption>("similarity_desc");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [loading, setLoading] = useState(false);
  const [savedProductIds, setSavedProductIds] = useState<string[]>([]);
  const [wishlistLoading, setWishlistLoading] = useState(false);
  const [uploadedImageId, setUploadedImageId] = useState<string | null>(null);
  const [uploadedImageAnalysis, setUploadedImageAnalysis] = useState<ReturnType<typeof getStoredUploadedImageAnalysis>>(null);
  const [isClientReady, setIsClientReady] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);

  useEffect(() => {
    setUploadedImageId(getStoredUploadedImageId());
    setUploadedImageAnalysis(getStoredUploadedImageAnalysis());
    setIsClientReady(true);
  }, []);

  async function loadSavedWishlistState() {
    setWishlistLoading(true);
    try {
      const result = await getWishlist();
      setSavedProductIds(result.items.map((item) => item.product_id));
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 상태 조회 중 오류가 발생했습니다.";
      setErrorMessage(message);
    } finally {
      setWishlistLoading(false);
    }
  }

  async function loadRecommendations() {
    if (!isClientReady) {
      return;
    }

    if (!uploadedImageId) {
      setErrorMessage("업로드된 이미지가 없습니다. /upload에서 이미지를 먼저 올려주세요.");
      setItems([]);
      setTotalCount(0);
      return;
    }

    setLoading(true);
    setErrorMessage(null);

    try {
      const result = await getRecommendations({
        uploadedImageId,
        category: category || undefined,
        sort,
        minPrice: minPrice ? Number(minPrice) : undefined,
        maxPrice: maxPrice ? Number(maxPrice) : undefined,
      });
      setItems(result.items);
      setTotalCount(result.total_count);
    } catch (error) {
      const message = error instanceof Error ? error.message : "추천 조회 중 오류가 발생했습니다.";
      const isStaleUpload =
        message.includes("Recommendation result does not exist for uploaded_image_id") ||
        message.includes("uploaded_image_id");

      if (isStaleUpload) {
        clearStoredUploadedImageId();
        clearStoredUploadedImageAnalysis();
        setUploadedImageId(null);
        setUploadedImageAnalysis(null);
        setErrorMessage("이전 업로드 정보가 만료되었습니다. /upload에서 이미지를 다시 올려주세요.");
        setItems([]);
        setTotalCount(0);
        return;
      }

      setErrorMessage(message);
      setItems([]);
      setTotalCount(0);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!isClientReady) {
      return;
    }

    void loadRecommendations();
  }, [category, sort, minPrice, maxPrice, isClientReady, uploadedImageId]);

  useEffect(() => {
    if (!isClientReady) {
      return;
    }

    void loadSavedWishlistState();
  }, [isClientReady]);

  function resetFilters() {
    setCategory("");
    setSort("similarity_desc");
    setMinPrice("");
    setMaxPrice("");
  }

  async function handleAddWishlist(productId: string, productName: string) {
    setFeedbackMessage(null);
    try {
      await addWishlist(productId);
      setSavedProductIds((prev) => (prev.includes(productId) ? prev : [...prev, productId]));
      setFeedbackMessage(`상품이 찜 목록에 추가되었습니다: ${productName}`);
    } catch (error) {
      const message = error instanceof Error ? error.message : "찜 추가 중 오류가 발생했습니다.";
      setErrorMessage(message);
    }
  }

  return (
    <section className="card recommendations-shell" aria-labelledby="recommendations-title" aria-busy={loading}>
      <div className="page-header page-header-secondary">
        <p className="eyebrow">Step 2</p>
        <div className="page-title-row">
          <div>
            <h1 id="recommendations-title">Recommendations</h1>
            <p className="lead page-lead">분석 결과와 유사도 점수를 함께 보면서 바로 찜할 수 있습니다.</p>
          </div>
          <div className="page-summary-grid compact-summary-grid">
            <div className="summary-pill">
              <span className="summary-label">Results</span>
              <strong>{totalCount}</strong>
            </div>
            <div className="summary-pill">
              <span className="summary-label">Sort</span>
              <strong>{sort.replace("_", " ")}</strong>
            </div>
            <div className="summary-pill">
              <span className="summary-label">Category</span>
              <strong>{category || "all"}</strong>
            </div>
            <div className="summary-pill">
              <span className="summary-label">Saved</span>
              <strong>{savedProductIds.length}</strong>
            </div>
          </div>
        </div>
      </div>

      <div className="filter-panel">
        <div className="filter-row">
          <label className="control-field" htmlFor="recommendation-category">
            <span className="field-label">Category</span>
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
            <span className="field-label">Sort</span>
            <select id="recommendation-sort" value={sort} onChange={(event) => setSort(event.target.value as SortOption)}>
              <option value="similarity_desc">Similarity Desc</option>
              <option value="price_asc">Price Asc</option>
              <option value="price_desc">Price Desc</option>
            </select>
          </label>
          <label className="control-field" htmlFor="recommendation-min-price">
            <span className="field-label">Min price</span>
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
            <span className="field-label">Max price</span>
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
      </div>

      <div className="status-region" aria-live="polite" aria-atomic="true">
        {loading ? (
          <p className="lead" role="status">
            추천 결과를 불러오는 중입니다...
          </p>
        ) : null}
        {wishlistLoading ? (
          <p className="hint-text" role="status">
            저장 상태를 동기화하는 중입니다...
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
          <div className="panel-title-row">
            <h2>Upload Analysis</h2>
            <span className="metric-chip">from latest upload</span>
          </div>
          <div className="analysis-chip-row">
            <span className="analysis-chip">tone {uploadedImageAnalysis.dominant_tone}</span>
            <span className="analysis-chip">mood {uploadedImageAnalysis.style_mood}</span>
            <span className="analysis-chip">fit {uploadedImageAnalysis.silhouette}</span>
          </div>
          <p className="hint-text">preferred categories: {uploadedImageAnalysis.preferred_categories.join(", ")}</p>
        </section>
      ) : null}

      <div className="card-grid product-grid" role="list" aria-label="추천 상품 목록">
        {loading
          ? Array.from({ length: 4 }).map((_, idx) => (
              <article className="product-card skeleton-card" key={`skeleton-${idx}`} aria-hidden="true">
                <div className="product-visual skeleton-block" />
                <div className="skeleton-line skeleton-title" />
                <div className="skeleton-line" />
                <div className="skeleton-line skeleton-short" />
              </article>
            ))
          : null}
        {items.map((item) => {
          const saved = savedProductIds.includes(item.product_id);

          return (
            <article className="product-card product-card-rich" key={item.product_id} role="listitem">
              <div className="product-visual-wrap">
                <img
                  src={item.image_url}
                  alt={`${item.product_name} 상품 이미지`}
                  className="product-visual"
                  onError={(event) => {
                    event.currentTarget.onerror = null;
                    event.currentTarget.src = buildRecommendationFallbackImage(item);
                  }}
                />
                <div className="product-badges">
                  <span className="badge neutral-badge">{item.source.toUpperCase()}</span>
                  <div className="product-badge-stack">
                    {saved ? <span className="badge saved-badge">Saved</span> : null}
                    <span className="badge">#{item.rank}</span>
                  </div>
                </div>
              </div>
              <div className="product-card-body">
                <p className="product-category">{item.category.toUpperCase()}</p>
                <h3>{item.product_name}</h3>
                <p className="product-price">{item.price.toLocaleString("ko-KR")}원</p>
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
                <div className="product-actions">
                  <a className="product-link" href={item.product_url} target="_blank" rel="noreferrer">
                    상품 보기
                  </a>
                  <button
                    type="button"
                    className={saved ? "saved-button" : undefined}
                    aria-label={`${item.product_name} 찜 추가`}
                    onClick={() => handleAddWishlist(item.product_id, item.product_name)}
                    disabled={saved}
                  >
                    {saved ? "Saved in Wishlist" : "Add to Wishlist"}
                  </button>
                </div>
              </div>
            </article>
          );
        })}
      </div>
      {!loading && items.length === 0 && !errorMessage ? (
        <div className="empty-box soft-empty-box">
          <p className="lead">추천 결과가 없습니다.</p>
          <p className="hint-text">
            먼저 <Link href="/upload">업로드</Link>에서 다른 이미지를 올리거나 가격 필터를 완화해보세요.
          </p>
        </div>
      ) : null}
    </section>
  );
}
