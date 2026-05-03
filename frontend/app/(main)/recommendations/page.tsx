"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

import { addWishlist, getRecommendations, getWishlist, RecommendationItem, UploadAnalysis } from "@/lib/api";

type SortOption = "similarity_desc" | "price_asc" | "price_desc";

const CATEGORY_LABELS: Record<string, string> = {
  top: "상의",
  bottom: "하의",
  outer: "아우터",
  shoes: "신발",
  bag: "가방",
  accessory: "악세서리",
};

const CATEGORY_OPTIONS = [
  { value: "", label: "전체" },
  { value: "top", label: "상의" },
  { value: "bottom", label: "하의" },
  { value: "outer", label: "아우터" },
  { value: "shoes", label: "신발" },
  { value: "bag", label: "가방" },
  { value: "accessory", label: "악세서리" },
];

const CATEGORY_ORDER = ["top", "bottom", "outer", "shoes", "bag", "accessory"] as const;
const CATEGORY_ORDER_SET = new Set<string>(CATEGORY_ORDER);

const SOURCE_LABELS: Record<string, string> = {
  naver: "네이버 쇼핑",
  zigzag: "지그재그",
  "29cm": "29CM",
};

function formatSimilarity(score: number): string {
  return `${Math.round(score * 100)}%`;
}

type RecommendationCategorySection = {
  key: string;
  label: string;
  items: RecommendationItem[];
};

function getCategoryLabel(category: string): string {
  return CATEGORY_LABELS[category] ?? category;
}

function getRecommendationSectionId(sectionKey: string): string {
  return `recommendation-category-${sectionKey}`;
}

function buildRecommendationSections(items: RecommendationItem[]): RecommendationCategorySection[] {
  const sections: RecommendationCategorySection[] = CATEGORY_ORDER.map((key) => ({
    key,
    label: getCategoryLabel(key),
    items: items.filter((item) => item.category === key),
  }));
  const uncategorizedItems = items.filter((item) => !CATEGORY_ORDER_SET.has(item.category));

  if (uncategorizedItems.length > 0) {
    sections.push({
      key: "etc",
      label: "기타",
      items: uncategorizedItems,
    });
  }

  return sections.filter((section) => section.items.length > 0);
}

function getTopMatchLabel(items: RecommendationItem[]): string {
  const topScore = Math.max(...items.map((item) => item.similarity_score));
  return Number.isFinite(topScore) ? formatSimilarity(topScore) : "0%";
}

function getAnalysisSourceLabel(analysis: UploadAnalysis | null): string {
  if (analysis?.analysis_source === "rule_fallback") {
    return "fallback 분석 기준";
  }
  return "AI 분석 기준";
}

function getAnalysisSourceDescription(analysis: UploadAnalysis | null): string | null {
  if (!analysis) {
    return null;
  }

  if (analysis.analysis_source === "rule_fallback") {
    if (analysis.fallback_reason) {
      return `AI 분석 경로를 사용할 수 없어 규칙 fallback 으로 추천을 이어가고 있습니다. (${analysis.fallback_reason})`;
    }
    return "AI 분석 경로를 사용할 수 없어 규칙 fallback 으로 추천을 이어가고 있습니다.";
  }

  return "현재 업로드의 AI 감지 품목 기준으로 추천을 만들고 있습니다.";
}

function getPreferredCategorySummary(analysis: UploadAnalysis): string {
  if (analysis.preferred_categories.length === 0) {
    return "없음";
  }

  return analysis.preferred_categories.map(getCategoryLabel).join(", ");
}

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

function resolveRecommendationImage(item: RecommendationItem): string {
  if (!item.image_url || item.image_url.includes("example.com/")) {
    return buildRecommendationFallbackImage(item);
  }

  return item.image_url;
}

function readUploadedImageIdFromLocation(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return new URLSearchParams(window.location.search).get("uploaded_image_id");
}

function RecommendationPageContent() {
  const searchParams = useSearchParams();
  const uploadedImageIdFromUrl = searchParams.get("uploaded_image_id") ?? readUploadedImageIdFromLocation();
  const lastResolvedUploadIdRef = useRef<string | null>(null);
  const latestRequestKeyRef = useRef(0);
  const [items, setItems] = useState<RecommendationItem[]>([]);
  const [category, setCategory] = useState("");
  const [sort, setSort] = useState<SortOption>("similarity_desc");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [loading, setLoading] = useState(false);
  const [savedProductIds, setSavedProductIds] = useState<string[]>([]);
  const [wishlistLoading, setWishlistLoading] = useState(false);
  const [uploadedImageId, setUploadedImageId] = useState<string | null>(null);
  const [uploadedImageAnalysis, setUploadedImageAnalysis] = useState<UploadAnalysis | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [customQueryInput, setCustomQueryInput] = useState("");
  const [appliedCustomQuery, setAppliedCustomQuery] = useState("");
  const [fallbackMessage, setFallbackMessage] = useState<string | null>(null);

  useEffect(() => {
    document.title = "스타일매치 | 추천 상품";
  }, []);

  useEffect(() => {
    const nextUploadedImageId = uploadedImageIdFromUrl ?? readUploadedImageIdFromLocation();
    const uploadChanged = lastResolvedUploadIdRef.current !== nextUploadedImageId;

    if (uploadChanged) {
      setItems([]);
      setSearchQuery("");
      setFallbackMessage(null);
      setFeedbackMessage(null);
      setCategory("");
      setSort("similarity_desc");
      setMinPrice("");
      setMaxPrice("");
      setCustomQueryInput("");
      setAppliedCustomQuery("");
      setUploadedImageAnalysis(null);
    }

    lastResolvedUploadIdRef.current = nextUploadedImageId;
    setUploadedImageId(nextUploadedImageId);
  }, [uploadedImageIdFromUrl]);

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
    if (!uploadedImageId) {
      setErrorMessage("업로드된 이미지가 없습니다. /upload에서 이미지를 먼저 올려주세요.");
      setItems([]);
      setSearchQuery("");
      setFallbackMessage(null);
      setUploadedImageAnalysis(null);
      return;
    }

    setLoading(true);
    setErrorMessage(null);
    setFallbackMessage(null);
    const requestKey = latestRequestKeyRef.current + 1;
    latestRequestKeyRef.current = requestKey;
    const requestUploadedImageId = uploadedImageId;

    try {
      const result = await getRecommendations({
        uploadedImageId: requestUploadedImageId,
        category: category || undefined,
        sort,
        minPrice: minPrice ? Number(minPrice) : undefined,
        maxPrice: maxPrice ? Number(maxPrice) : undefined,
        customQuery: appliedCustomQuery || undefined,
      });
      if (latestRequestKeyRef.current !== requestKey || lastResolvedUploadIdRef.current !== requestUploadedImageId) {
        return;
      }
      setItems(result.items);
      setSearchQuery(result.query ?? "");
      setFallbackMessage(result.fallback_message ?? null);
      if (result.analysis) {
        setUploadedImageAnalysis(result.analysis);
      }
    } catch (error) {
      if (latestRequestKeyRef.current !== requestKey || lastResolvedUploadIdRef.current !== requestUploadedImageId) {
        return;
      }
      const message = error instanceof Error ? error.message : "추천 조회 중 오류가 발생했습니다.";
      const isStaleUpload =
        message.includes("Recommendation result does not exist for uploaded_image_id") || message.includes("uploaded_image_id");

      if (isStaleUpload) {
        setUploadedImageId(null);
        setUploadedImageAnalysis(null);
        setErrorMessage("이전 업로드 정보가 만료되었습니다. /upload에서 이미지를 다시 올려주세요.");
        setItems([]);
        setSearchQuery("");
        setFallbackMessage(null);
        return;
      }

      setErrorMessage(message);
      setItems([]);
      setSearchQuery("");
      setFallbackMessage(null);
    } finally {
      if (latestRequestKeyRef.current === requestKey && lastResolvedUploadIdRef.current === requestUploadedImageId) {
        setLoading(false);
      }
    }
  }

  useEffect(() => {
    void loadRecommendations();
  }, [category, sort, minPrice, maxPrice, appliedCustomQuery, uploadedImageId]);

  useEffect(() => {
    void loadSavedWishlistState();
  }, []);

  function resetFilters() {
    setCategory("");
    setSort("similarity_desc");
    setMinPrice("");
    setMaxPrice("");
  }

  function applyCustomQuery() {
    setAppliedCustomQuery(customQueryInput.trim());
  }

  function clearCustomQuery() {
    setCustomQueryInput("");
    setAppliedCustomQuery("");
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

  const recommendationSections = buildRecommendationSections(items);
  const visibleCount = items.length;
  const savedCount = savedProductIds.length;
  const activeQueryLabel = appliedCustomQuery || searchQuery || "자동 생성";
  const featuredItem = items[0] ?? null;
  const supportingItems = items.slice(1, 4);

  function renderProductCard(item: RecommendationItem) {
    const saved = savedProductIds.includes(item.product_id);

    return (
      <article className="product-card product-card-rich" key={item.product_id} role="listitem">
        <div className="product-visual-wrap">
          <img
            src={resolveRecommendationImage(item)}
            alt={`${item.product_name} 상품 이미지`}
            className="product-visual"
            onError={(event) => {
              event.currentTarget.onerror = null;
              event.currentTarget.src = buildRecommendationFallbackImage(item);
            }}
          />
          <div className="product-badges">
            <span className="badge neutral-badge">{SOURCE_LABELS[item.source] ?? item.source.toUpperCase()}</span>
            <div className="product-badge-stack">
              {saved ? <span className="badge saved-badge">저장됨</span> : null}
              <span className="badge">#{item.rank}</span>
            </div>
          </div>
          <span className="product-category-chip">{getCategoryLabel(item.category)}</span>
        </div>
        <div className="product-card-body">
          <div className="product-meta-row">
            <span>추천 정확도</span>
            <span>매칭 {formatSimilarity(item.similarity_score)}</span>
          </div>
          <h3>{item.product_name}</h3>
          <div className="product-price-row">
            <p className="product-price">{item.price.toLocaleString("ko-KR")}원</p>
            <span className="product-source-inline">{SOURCE_LABELS[item.source] ?? item.source.toUpperCase()}</span>
          </div>
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
              {saved ? "위시리스트 저장됨" : "위시리스트 담기"}
            </button>
          </div>
          <details className="product-match-details">
            <summary>매칭 정보 보기</summary>
            <div className="signal-list">
              <span>톤 {item.matched_signals.dominant_tone}</span>
              {item.matched_signals.dominant_color ? <span>색상 {item.matched_signals.dominant_color}</span> : null}
              {item.matched_signals.category_target_color ? <span>검색 색상 {item.matched_signals.category_target_color}</span> : null}
              {item.matched_signals.product_dominant_color && item.matched_signals.product_dominant_color !== "unknown" ? (
                <span>상품 이미지 {item.matched_signals.product_dominant_color}</span>
              ) : null}
              <span>무드 {item.matched_signals.style_mood}</span>
              <span>실루엣 {item.matched_signals.silhouette}</span>
            </div>
            <dl className="score-breakdown">
              <div>
                <dt>벡터</dt>
                <dd>{item.score_breakdown.vector_similarity.toFixed(2)}</dd>
              </div>
              <div>
                <dt>톤</dt>
                <dd>+{item.score_breakdown.tone_bonus.toFixed(2)}</dd>
              </div>
              <div>
                <dt>무드</dt>
                <dd>+{item.score_breakdown.mood_bonus.toFixed(2)}</dd>
              </div>
              <div>
                <dt>실루엣</dt>
                <dd>+{item.score_breakdown.silhouette_bonus.toFixed(2)}</dd>
              </div>
              {typeof item.score_breakdown.color_bonus === "number" ? (
                <div>
                  <dt>상품명 색상</dt>
                  <dd>+{item.score_breakdown.color_bonus.toFixed(2)}</dd>
                </div>
              ) : null}
              {typeof item.score_breakdown.product_image_color_bonus === "number" ? (
                <div>
                  <dt>이미지 색상</dt>
                  <dd>+{item.score_breakdown.product_image_color_bonus.toFixed(2)}</dd>
                </div>
              ) : null}
            </dl>
          </details>
        </div>
      </article>
    );
  }

  return (
    <section className="recommendation-page" aria-labelledby="recommendations-title" aria-busy={loading}>
      <div className="curation-hero curation-hero-luxe">
        <div className="curation-hero-copy">
          <p className="eyebrow">Curated Feed</p>
          <h1 id="recommendations-title" className="display-title">AI가 읽은 분위기를 실제 쇼핑 가능한 스타일 에디트로 정리했습니다.</h1>
          <p className="lead page-lead">
            현재 업로드에서 읽은 스타일 신호를 바탕으로 비슷한 상품을 정렬했습니다. 필터를 조정하거나 검색어를 직접 입력해 더 정교하게 다시 볼 수 있습니다.
          </p>
          <div className="hero-pill-row">
            <span className="hero-pill">검색어 {activeQueryLabel}</span>
            <span className="hero-pill">추천 {visibleCount}개</span>
            <span className="hero-pill">{category ? `${getCategoryLabel(category)} 필터` : "전체 카테고리"}</span>
          </div>
          {fallbackMessage ? (
            <p className="warning-text" role="status">
              {fallbackMessage}
            </p>
          ) : null}
        </div>
        <div className="hero-spotlight-shell">
          {featuredItem ? (
            <article className="hero-spotlight-card">
              <div className="hero-spotlight-visual">
                <img
                  src={resolveRecommendationImage(featuredItem)}
                  alt={`${featuredItem.product_name} 하이라이트 이미지`}
                  onError={(event) => {
                    event.currentTarget.onerror = null;
                    event.currentTarget.src = buildRecommendationFallbackImage(featuredItem);
                  }}
                />
              </div>
              <div className="hero-spotlight-copy">
                <span className="workspace-chip">Top Match</span>
                <strong>{featuredItem.product_name}</strong>
                <p>{SOURCE_LABELS[featuredItem.source] ?? featuredItem.source.toUpperCase()} · {getCategoryLabel(featuredItem.category)} · 매칭 {formatSimilarity(featuredItem.similarity_score)}</p>
                <div className="hero-spotlight-actions">
                  <a className="product-link" href={featuredItem.product_url} target="_blank" rel="noreferrer">
                    대표 상품 보기
                  </a>
                </div>
              </div>
            </article>
          ) : (
            <div className="hero-spotlight-placeholder" aria-hidden="true">
              <span>Curated Spotlight</span>
              <small>업로드 후 대표 매칭 상품이 여기에 표시됩니다.</small>
            </div>
          )}
          <div className="hero-metrics-board hero-metrics-board-compact" aria-label="추천 화면 요약">
            <div className="metric-tile">
              <span>Visible Items</span>
              <strong>{visibleCount}</strong>
              <small>현재 화면에 보이는 추천 수</small>
            </div>
            <div className="metric-tile">
              <span>Saved Products</span>
              <strong>{savedCount}</strong>
              <small>위시리스트에 저장된 상품 수</small>
            </div>
            <div className="metric-tile">
              <span>Curated Sections</span>
              <strong>{recommendationSections.length}</strong>
              <small>카테고리별 섹션 수</small>
            </div>
          </div>
        </div>
      </div>

      {supportingItems.length > 0 ? (
        <section className="featured-strip" aria-label="하이라이트 추천 요약">
          {supportingItems.map((item) => (
            <article className="featured-mini-card" key={`featured-${item.product_id}`}>
              <span>{getCategoryLabel(item.category)}</span>
              <strong>{item.product_name}</strong>
              <small>{item.price.toLocaleString("ko-KR")}원</small>
            </article>
          ))}
        </section>
      ) : null}

      <div className="recommendation-layout">
        <aside className="filter-sidebar">
          <div className="filter-panel filter-panel-elevated">
            <div className="support-panel-header">
              <p className="eyebrow">Refine Feed</p>
              <h2>추천 조건 조정</h2>
            </div>
            <div className="filter-row">
              <label className="control-field" htmlFor="recommendation-category">
                <span className="field-label">카테고리</span>
                <select id="recommendation-category" value={category} onChange={(event) => setCategory(event.target.value)}>
                  {CATEGORY_OPTIONS.map((option) => (
                    <option key={option.value || "all"} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
              <label className="control-field" htmlFor="recommendation-sort">
                <span className="field-label">정렬</span>
                <select id="recommendation-sort" value={sort} onChange={(event) => setSort(event.target.value as SortOption)}>
                  <option value="similarity_desc">유사도 높은 순</option>
                  <option value="price_asc">가격 낮은 순</option>
                  <option value="price_desc">가격 높은 순</option>
                </select>
              </label>
              <label className="control-field" htmlFor="recommendation-min-price">
                <span className="field-label">최소 가격</span>
                <input id="recommendation-min-price" type="number" min={0} inputMode="numeric" placeholder="최소 가격" value={minPrice} onChange={(event) => setMinPrice(event.target.value)} />
              </label>
              <label className="control-field" htmlFor="recommendation-max-price">
                <span className="field-label">최대 가격</span>
                <input id="recommendation-max-price" type="number" min={0} inputMode="numeric" placeholder="최대 가격" value={maxPrice} onChange={(event) => setMaxPrice(event.target.value)} />
              </label>
            </div>
            <div className="custom-query-row">
              <label className="control-field" htmlFor="recommendation-custom-query">
                <span className="field-label">직접 검색어</span>
                <input
                  id="recommendation-custom-query"
                  type="search"
                  maxLength={80}
                  placeholder="예: 블랙 미니멀 재킷"
                  value={customQueryInput}
                  onChange={(event) => setCustomQueryInput(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      event.preventDefault();
                      applyCustomQuery();
                    }
                  }}
                />
              </label>
              <div className="custom-query-actions">
                <button type="button" onClick={applyCustomQuery}>
                  검색어 적용
                </button>
                <button type="button" className="ghost-button" onClick={clearCustomQuery} disabled={!customQueryInput && !appliedCustomQuery}>
                  초기화
                </button>
              </div>
            </div>
            <p className="hint-text">
              {appliedCustomQuery ? `현재 직접 입력 검색어: ${appliedCustomQuery}` : "비워두면 현재 업로드 분석 결과로 검색어를 자동 생성합니다."}
            </p>
            <div className="action-row">
              <button type="button" className="ghost-button" onClick={() => void loadRecommendations()}>
                새로고침
              </button>
              <button type="button" className="ghost-button" onClick={resetFilters}>
                필터 초기화
              </button>
            </div>
          </div>

          <div className="status-region recommendation-status" aria-live="polite" aria-atomic="true">
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
            <section className="analysis-panel analysis-panel-elevated" aria-label="업로드 이미지 분석 요약">
              <div className="panel-title-row">
                <h2>업로드 분석</h2>
                <span className="metric-chip">{getAnalysisSourceLabel(uploadedImageAnalysis)}</span>
              </div>
              <div className="analysis-chip-row">
                <span className="analysis-chip">톤 {uploadedImageAnalysis.dominant_tone}</span>
                {uploadedImageAnalysis.dominant_color ? <span className="analysis-chip">색상 {uploadedImageAnalysis.dominant_color}</span> : null}
                <span className="analysis-chip">무드 {uploadedImageAnalysis.style_mood}</span>
                <span className="analysis-chip">실루엣 {uploadedImageAnalysis.silhouette}</span>
              </div>
              {getAnalysisSourceDescription(uploadedImageAnalysis) ? <p className="hint-text">{getAnalysisSourceDescription(uploadedImageAnalysis)}</p> : null}
              <p className="hint-text">감지 카테고리: {getPreferredCategorySummary(uploadedImageAnalysis)}</p>
              {uploadedImageAnalysis.detected_items && uploadedImageAnalysis.detected_items.length > 0 ? (
                <p className="hint-text">감지 품목: {uploadedImageAnalysis.detected_items.map((item) => item.query).join(" / ")}</p>
              ) : null}
              {uploadedImageAnalysis.category_query_hints ? (
                <p className="hint-text">검색 힌트: {Object.values(uploadedImageAnalysis.category_query_hints).join(" / ")}</p>
              ) : null}
            </section>
          ) : null}

          <section className="support-panel compact-support-panel">
            <div className="support-panel-header">
              <p className="eyebrow">Quick Reset</p>
              <h2>새 이미지를 기준으로 다시 시작</h2>
            </div>
            <p className="hint-text">
              현재 추천이 마음에 들지 않으면 <Link href="/upload">업로드 화면</Link>에서 새 코디 이미지를 넣어 바로 다른 컬렉션을 만들 수 있습니다.
            </p>
          </section>
        </aside>

        <div className="recommendation-content">
          {!loading && items.length > 0 && !category ? (
            <nav className="category-jump-panel" aria-label="추천 카테고리 바로가기">
              <div className="category-jump-copy">
                <div>
                  <p className="eyebrow">Section Jump</p>
                  <strong>원하는 제품군으로 바로 이동하세요.</strong>
                </div>
                <span className="workspace-chip">Curated by Category</span>
              </div>
              <div className="category-jump-list">
                {recommendationSections.map((section) => (
                  <a className="category-jump-card" href={`#${getRecommendationSectionId(section.key)}`} key={section.key}>
                    <span>{section.label}</span>
                    <strong>{section.items.length}개</strong>
                    <small>최고 매칭 {getTopMatchLabel(section.items)}</small>
                  </a>
                ))}
              </div>
            </nav>
          ) : null}

          {loading ? (
            <div className="card-grid product-grid" role="list" aria-label="추천 상품 로딩 목록">
              {Array.from({ length: 4 }).map((_, idx) => (
                <article className="product-card skeleton-card" key={`skeleton-${idx}`} aria-hidden="true">
                  <div className="product-visual skeleton-block" />
                  <div className="skeleton-line skeleton-title" />
                  <div className="skeleton-line" />
                  <div className="skeleton-line skeleton-short" />
                </article>
              ))}
            </div>
          ) : null}

          {!loading && items.length > 0 && category ? (
            <div className="card-grid product-grid" role="list" aria-label={`${getCategoryLabel(category)} 추천 상품 목록`}>
              {items.map(renderProductCard)}
            </div>
          ) : null}

          {!loading && items.length > 0 && !category ? (
            <div className="recommendation-section-list" aria-label="카테고리별 추천 상품 목록">
              {recommendationSections.map((section) => {
                const sectionId = getRecommendationSectionId(section.key);
                const sectionTitleId = `${sectionId}-title`;

                return (
                  <section className="recommendation-category-section" id={sectionId} key={section.key} aria-labelledby={sectionTitleId}>
                    <div className="recommendation-section-header">
                      <div>
                        <p className="eyebrow">Category Edit</p>
                        <h2 id={sectionTitleId}>{section.label}</h2>
                      </div>
                      <div className="section-stat-row" aria-label={`${section.label} 추천 요약`}>
                        <span>{section.items.length}개 상품</span>
                        <span>최고 매칭 {getTopMatchLabel(section.items)}</span>
                      </div>
                    </div>
                    <div className="card-grid product-grid" role="list" aria-label={`${section.label} 추천 상품 목록`}>
                      {section.items.map(renderProductCard)}
                    </div>
                  </section>
                );
              })}
            </div>
          ) : null}

          {!loading && items.length === 0 && !errorMessage ? (
            <div className="empty-box soft-empty-box large-empty-box">
              <p className="lead">추천 결과가 없습니다.</p>
              <p className="hint-text">
                먼저 <Link href="/upload">업로드</Link>에서 다른 이미지를 올리거나 가격 필터를 완화해보세요.
              </p>
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}

export default function RecommendationPage() {
  return (
    <Suspense
      fallback={
        <section className="recommendation-page" aria-busy="true">
          <div className="empty-box soft-empty-box large-empty-box">
            <p className="lead" role="status">
              추천 결과를 불러오는 중입니다...
            </p>
          </div>
        </section>
      }
    >
      <RecommendationPageContent />
    </Suspense>
  );
}
