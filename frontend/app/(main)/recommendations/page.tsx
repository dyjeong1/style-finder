"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

import {
  addWishlist,
  getRecommendations,
  getUploadedImageFileUrl,
  getWishlist,
  RecommendationItem,
  UploadAnalysis,
} from "@/lib/api";
import { getStoredUploadImageByUploadedImageId } from "@/lib/recent-upload-store";

type SortOption = "similarity_desc" | "price_asc" | "price_desc";

const CATEGORY_LABELS: Record<string, string> = {
  top: "상의",
  bottom: "하의",
  outer: "아우터",
  shoes: "신발",
  bag: "가방",
  accessory: "악세서리",
};

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

function getAnalysisDerivationDescription(analysis: UploadAnalysis | null): string | null {
  if (!analysis) {
    return null;
  }

  return "톤과 색상은 업로드 이미지의 대표 색상에서, 무드와 실루엣은 감지된 품목 조합에서 계산합니다.";
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

function buildUploadedImageFallback(uploadedImageId: string | null): string {
  const label = uploadedImageId ? "현재 업로드 이미지" : "업로드 이미지 없음";
  const subtitle = uploadedImageId ? "Recommendation Source" : "No Upload";
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
      <defs>
        <linearGradient id="uploadThumb" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="#f6d6a7" />
          <stop offset="100%" stop-color="#e5b16a" />
        </linearGradient>
      </defs>
      <rect width="240" height="240" rx="36" fill="url(#uploadThumb)" />
      <rect x="22" y="22" width="196" height="196" rx="28" fill="rgba(255,255,255,0.55)" />
      <text x="40" y="88" fill="#9a3412" font-family="Pretendard, Arial, sans-serif" font-size="16" font-weight="700">${subtitle}</text>
      <text x="40" y="128" fill="#111827" font-family="Pretendard, Arial, sans-serif" font-size="20" font-weight="800">${label}</text>
      <text x="40" y="164" fill="#4b5563" font-family="Pretendard, Arial, sans-serif" font-size="14">StyleMatch</text>
    </svg>
  `;

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

function RecommendationPageContent() {
  const searchParams = useSearchParams();
  const uploadedImageIdFromUrl = searchParams.get("uploaded_image_id") ?? readUploadedImageIdFromLocation();
  const lastResolvedUploadIdRef = useRef<string | null>(null);
  const latestRequestKeyRef = useRef(0);
  const uploadedImagePreviewObjectUrlRef = useRef<string | null>(null);
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
  const [isUploadedImageModalOpen, setIsUploadedImageModalOpen] = useState(false);
  const [uploadedImagePreviewUrl, setUploadedImagePreviewUrl] = useState(() => buildUploadedImageFallback(null));
  const shouldShowUploadedImagePreview = Boolean(uploadedImageId && uploadedImageAnalysis);

  function revokeUploadedImagePreviewObjectUrl() {
    if (!uploadedImagePreviewObjectUrlRef.current) {
      return;
    }

    URL.revokeObjectURL(uploadedImagePreviewObjectUrlRef.current);
    uploadedImagePreviewObjectUrlRef.current = null;
  }

  useEffect(() => {
    document.title = "스타일매치 | 추천 상품";
  }, []);

  useEffect(() => {
    return () => {
      revokeUploadedImagePreviewObjectUrl();
    };
  }, []);

  useEffect(() => {
    if (!isUploadedImageModalOpen) {
      return;
    }

    function handleEscapeKey(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setIsUploadedImageModalOpen(false);
      }
    }

    window.addEventListener("keydown", handleEscapeKey);
    return () => {
      window.removeEventListener("keydown", handleEscapeKey);
    };
  }, [isUploadedImageModalOpen]);

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
      setIsUploadedImageModalOpen(false);
    }

    lastResolvedUploadIdRef.current = nextUploadedImageId;
    setUploadedImageId(nextUploadedImageId);
  }, [uploadedImageIdFromUrl]);

  useEffect(() => {
    let cancelled = false;

    async function syncUploadedImagePreview() {
      revokeUploadedImagePreviewObjectUrl();

      if (!uploadedImageId) {
        setUploadedImagePreviewUrl(buildUploadedImageFallback(null));
        return;
      }

      try {
        const storedUpload = await getStoredUploadImageByUploadedImageId(uploadedImageId);
        if (cancelled) {
          return;
        }

        if (storedUpload) {
          const objectUrl = URL.createObjectURL(storedUpload.blob);
          uploadedImagePreviewObjectUrlRef.current = objectUrl;
          setUploadedImagePreviewUrl(objectUrl);
          return;
        }
      } catch (storageError) {
        console.warn("추천 업로드 이미지 프리뷰를 브라우저 저장소에서 복원하지 못했습니다.", storageError);
      }

      if (!cancelled) {
        setUploadedImagePreviewUrl(getUploadedImageFileUrl(uploadedImageId));
      }
    }

    void syncUploadedImagePreview();

    return () => {
      cancelled = true;
    };
  }, [uploadedImageId]);

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
        message.includes("Recommendation result does not exist for uploaded_image_id") ||
        message.includes("uploaded_image_id");

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
    <section className="card recommendations-shell" aria-labelledby="recommendations-title" aria-busy={loading}>
      <div className="page-header page-header-secondary">
        <p className="eyebrow">추천</p>
        <div className="page-title-row">
          <div>
            <h1 id="recommendations-title">추천 상품</h1>
            <p className="lead page-lead">분석 결과와 유사도 점수를 함께 보면서 바로 찜할 수 있습니다.</p>
          </div>
          {shouldShowUploadedImagePreview ? (
            <button
              type="button"
              className="uploaded-image-preview-card uploaded-image-preview-button"
              aria-label="현재 추천 기준 업로드 이미지 크게 보기"
              onClick={() => setIsUploadedImageModalOpen(true)}
            >
              <img
                src={uploadedImagePreviewUrl}
                alt="현재 추천 기준 업로드 이미지"
                className="uploaded-image-preview"
                onError={(event) => {
                  event.currentTarget.onerror = null;
                  event.currentTarget.src = buildUploadedImageFallback(uploadedImageId);
                }}
              />
              <span className="uploaded-image-preview-hint">크게 보기</span>
            </button>
          ) : null}
        </div>
      </div>

      {fallbackMessage ? (
        <p className="warning-text" role="status">
          {fallbackMessage}
        </p>
      ) : null}

      <div className="filter-panel">
        <div className="filter-row">
          <label className="control-field" htmlFor="recommendation-category">
            <span className="field-label">카테고리</span>
            <select id="recommendation-category" value={category} onChange={(event) => setCategory(event.target.value)}>
              <option value="">전체</option>
              <option value="top">상의</option>
              <option value="bottom">하의</option>
              <option value="outer">아우터</option>
              <option value="shoes">신발</option>
              <option value="bag">가방</option>
              <option value="accessory">악세서리</option>
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
            <input
              id="recommendation-min-price"
              type="number"
              min={0}
              inputMode="numeric"
              placeholder="최소 가격"
              value={minPrice}
              onChange={(event) => setMinPrice(event.target.value)}
            />
          </label>
          <label className="control-field" htmlFor="recommendation-max-price">
            <span className="field-label">최대 가격</span>
            <input
              id="recommendation-max-price"
              type="number"
              min={0}
              inputMode="numeric"
              placeholder="최대 가격"
              value={maxPrice}
              onChange={(event) => setMaxPrice(event.target.value)}
            />
          </label>
        </div>
        <div className="custom-query-row">
          <label className="control-field" htmlFor="recommendation-custom-query">
            <span className="field-label">추천 검색어 직접 입력</span>
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
              검색어 초기화
            </button>
          </div>
        </div>
        {appliedCustomQuery ? (
          <p className="hint-text">현재 직접 입력 검색어: {appliedCustomQuery}</p>
        ) : (
          <p className="hint-text">비워두면 현재 업로드의 분석 결과로 검색어를 자동 생성합니다.</p>
        )}
        <div className="action-row">
          <button type="button" className="ghost-button" onClick={() => void loadRecommendations()}>
            새로고침
          </button>
          <button type="button" className="ghost-button" onClick={resetFilters}>
            필터 초기화
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
            <h2>업로드 분석</h2>
            <span className="metric-chip">{getAnalysisSourceLabel(uploadedImageAnalysis)}</span>
          </div>
          <div className="analysis-chip-row">
            <span className="analysis-chip">톤 {uploadedImageAnalysis.dominant_tone}</span>
            {uploadedImageAnalysis.dominant_color ? <span className="analysis-chip">색상 {uploadedImageAnalysis.dominant_color}</span> : null}
            <span className="analysis-chip">무드 {uploadedImageAnalysis.style_mood}</span>
            <span className="analysis-chip">실루엣 {uploadedImageAnalysis.silhouette}</span>
          </div>
          {getAnalysisSourceDescription(uploadedImageAnalysis) ? (
            <p className="hint-text">{getAnalysisSourceDescription(uploadedImageAnalysis)}</p>
          ) : null}
          {getAnalysisDerivationDescription(uploadedImageAnalysis) ? (
            <p className="hint-text">{getAnalysisDerivationDescription(uploadedImageAnalysis)}</p>
          ) : null}
          <p className="hint-text">감지 카테고리: {getPreferredCategorySummary(uploadedImageAnalysis)}</p>
          {uploadedImageAnalysis.detected_items && uploadedImageAnalysis.detected_items.length > 0 ? (
            <p className="hint-text">감지 품목: {uploadedImageAnalysis.detected_items.map((item) => item.query).join(" / ")}</p>
          ) : null}
          {uploadedImageAnalysis.category_query_hints ? (
            <p className="hint-text">검색 힌트: {Object.values(uploadedImageAnalysis.category_query_hints).join(" / ")}</p>
          ) : null}
        </section>
      ) : null}

      {!loading && items.length > 0 && !category ? (
        <nav className="category-jump-panel" aria-label="추천 카테고리 바로가기">
          <div className="category-jump-copy">
            <p className="eyebrow">바로가기</p>
            <strong>원하는 제품군으로 빠르게 이동하세요.</strong>
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
              <section
                className="recommendation-category-section"
                id={sectionId}
                key={section.key}
                aria-labelledby={sectionTitleId}
              >
                <div className="recommendation-section-header">
                  <div>
                    <p className="eyebrow">카테고리 추천</p>
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
        <div className="empty-box soft-empty-box">
          <p className="lead">추천 결과가 없습니다.</p>
          <p className="hint-text">
            먼저 <Link href="/upload">업로드</Link>에서 다른 이미지를 올리거나 가격 필터를 완화해보세요.
          </p>
        </div>
      ) : null}

      {isUploadedImageModalOpen && shouldShowUploadedImagePreview ? (
        <div
          className="image-preview-modal-backdrop"
          role="dialog"
          aria-modal="true"
          aria-label="추천 기준 업로드 이미지 확대 보기"
          onClick={() => setIsUploadedImageModalOpen(false)}
        >
          <div className="image-preview-modal-sheet" onClick={(event) => event.stopPropagation()}>
            <button
              type="button"
              className="image-preview-modal-close"
              aria-label="업로드 이미지 확대 보기 닫기"
              onClick={() => setIsUploadedImageModalOpen(false)}
            >
              닫기
            </button>
            <div className="image-preview-modal-frame">
              <img
                src={uploadedImagePreviewUrl}
                alt="현재 추천 기준 업로드 이미지 확대 보기"
                className="image-preview-modal-image"
                onError={(event) => {
                  event.currentTarget.onerror = null;
                  event.currentTarget.src = buildUploadedImageFallback(uploadedImageId);
                }}
              />
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}

export default function RecommendationPage() {
  return (
    <Suspense
      fallback={
        <section className="card recommendations-shell" aria-busy="true">
          <p className="lead" role="status">
            추천 결과를 불러오는 중입니다...
          </p>
        </section>
      }
    >
      <RecommendationPageContent />
    </Suspense>
  );
}
