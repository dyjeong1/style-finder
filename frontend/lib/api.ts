const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

const UPLOADED_IMAGE_ID_KEY = "stylematch_uploaded_image_id";
const UPLOADED_IMAGE_ANALYSIS_KEY = "stylematch_uploaded_image_analysis";
const UPLOAD_HISTORY_KEY = "stylematch_upload_history";

type ApiMeta = {
  request_id: string;
  timestamp: string;
};

type ApiError = {
  code: string;
  message: string;
  detail: Record<string, unknown>;
};

type ApiEnvelope<T> = {
  data: T;
  error: ApiError | null;
  meta: ApiMeta;
};

export type UploadAnalysis = {
  checksum: string;
  dominant_tone: string;
  style_mood: string;
  silhouette: string;
  preferred_categories: string[];
};

export type UploadedImage = {
  id: string;
  image_url: string;
  created_at: string;
  analysis: UploadAnalysis;
};

export type UploadHistoryItem = {
  id: string;
  image_url: string;
  created_at: string;
  file_name: string;
  analysis: UploadAnalysis;
};

export type RecommendationScoreBreakdown = {
  vector_similarity: number;
  tone_bonus: number;
  mood_bonus: number;
  silhouette_bonus: number;
  category_bonus: number;
};

export type RecommendationMatchedSignals = {
  dominant_tone: string;
  style_mood: string;
  silhouette: string;
  preferred_categories: string[];
};

export type RecommendationItem = {
  product_id: string;
  source: string;
  product_name: string;
  category: string;
  price: number;
  product_url: string;
  image_url: string;
  similarity_score: number;
  rank: number;
  score_breakdown: RecommendationScoreBreakdown;
  matched_signals: RecommendationMatchedSignals;
};

type RecommendationListResponse = {
  items: RecommendationItem[];
  total_count: number;
  source?: "naver_shopping" | "mock";
  query?: string;
  fallback_reason?: string | null;
  fallback_message?: string | null;
};

export type WishlistItem = {
  id: string;
  product_id: string;
  product_name: string;
  source: string;
  category: string;
  price: number;
  product_url: string;
  image_url: string;
  created_at: string;
};

type WishlistListResponse = {
  items: WishlistItem[];
  total_count: number;
};

function parseHttpError(fallbackMessage: string, payload: unknown): Error {
  if (typeof payload !== "object" || payload === null) {
    return new Error(fallbackMessage);
  }

  const apiError = (payload as { error?: unknown }).error;
  if (typeof apiError === "object" && apiError !== null) {
    const apiErrorMessage = (apiError as { message?: unknown }).message;
    if (typeof apiErrorMessage === "string" && apiErrorMessage.length > 0) {
      return new Error(apiErrorMessage);
    }
  }

  const detail = (payload as { detail?: unknown }).detail;
  if (typeof detail === "string") {
    return new Error(detail);
  }

  if (typeof detail === "object" && detail !== null) {
    const detailMessage = (detail as { message?: unknown }).message;
    if (typeof detailMessage === "string" && detailMessage.length > 0) {
      return new Error(detailMessage);
    }
  }

  return new Error(fallbackMessage);
}

async function apiRequest<T>(path: string, options?: RequestInit): Promise<T> {
  const { headers, ...restOptions } = options ?? {};
  const mergedHeaders = new Headers(headers ?? {});

  const hasFormDataBody = typeof FormData !== "undefined" && restOptions.body instanceof FormData;
  if (!hasFormDataBody && !mergedHeaders.has("Content-Type")) {
    mergedHeaders.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...restOptions,
    headers: mergedHeaders,
    cache: "no-store",
  });

  if (response.status === 204) {
    return undefined as T;
  }

  const payload = (await response.json().catch(() => null)) as ApiEnvelope<T> | null;

  if (!response.ok) {
    throw parseHttpError(`${(options?.method ?? "GET").toUpperCase()} ${path} failed`, payload);
  }

  if (!payload) {
    throw new Error("Empty API response");
  }

  if (payload.error) {
    throw new Error(payload.error.message);
  }

  return payload.data;
}

export function getStoredUploadedImageId(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(UPLOADED_IMAGE_ID_KEY);
}

export function setStoredUploadedImageId(uploadedImageId: string): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(UPLOADED_IMAGE_ID_KEY, uploadedImageId);
}

export function clearStoredUploadedImageId(): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(UPLOADED_IMAGE_ID_KEY);
}

export function getStoredUploadedImageAnalysis(): UploadAnalysis | null {
  if (typeof window === "undefined") {
    return null;
  }

  const rawValue = window.localStorage.getItem(UPLOADED_IMAGE_ANALYSIS_KEY);
  if (!rawValue) {
    return null;
  }

  try {
    return JSON.parse(rawValue) as UploadAnalysis;
  } catch {
    return null;
  }
}

export function setStoredUploadedImageAnalysis(analysis: UploadAnalysis): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(UPLOADED_IMAGE_ANALYSIS_KEY, JSON.stringify(analysis));
}

export function clearStoredUploadedImageAnalysis(): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(UPLOADED_IMAGE_ANALYSIS_KEY);
}

export function getUploadHistory(): UploadHistoryItem[] {
  if (typeof window === "undefined") {
    return [];
  }

  const rawValue = window.localStorage.getItem(UPLOAD_HISTORY_KEY);
  if (!rawValue) {
    return [];
  }

  try {
    return JSON.parse(rawValue) as UploadHistoryItem[];
  } catch {
    return [];
  }
}

export function prependUploadHistory(item: UploadHistoryItem): UploadHistoryItem[] {
  if (typeof window === "undefined") {
    return [item];
  }

  const nextItems = [
    item,
    ...getUploadHistory().filter((existingItem) => existingItem.id !== item.id),
  ].slice(0, 6);

  window.localStorage.setItem(UPLOAD_HISTORY_KEY, JSON.stringify(nextItems));
  return nextItems;
}

export function removeUploadHistoryItem(uploadHistoryId: string): UploadHistoryItem[] {
  if (typeof window === "undefined") {
    return [];
  }

  const nextItems = getUploadHistory().filter((item) => item.id !== uploadHistoryId);
  window.localStorage.setItem(UPLOAD_HISTORY_KEY, JSON.stringify(nextItems));

  if (getStoredUploadedImageId() === uploadHistoryId) {
    clearStoredUploadedImageId();
    clearStoredUploadedImageAnalysis();
  }

  return nextItems;
}

export async function uploadImage(image: File): Promise<UploadedImage> {
  const formData = new FormData();
  formData.append("image", image);

  return apiRequest<UploadedImage>("/images/upload", {
    method: "POST",
    body: formData,
  });
}

export type RecommendationQuery = {
  uploadedImageId: string;
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  sort?: "similarity_desc" | "price_asc" | "price_desc";
  limit?: number;
};

export async function getRecommendations(query: RecommendationQuery): Promise<RecommendationListResponse> {
  const searchParams = new URLSearchParams();
  searchParams.set("uploaded_image_id", query.uploadedImageId);

  if (query.category) {
    searchParams.set("category", query.category);
  }
  if (typeof query.minPrice === "number") {
    searchParams.set("min_price", String(query.minPrice));
  }
  if (typeof query.maxPrice === "number") {
    searchParams.set("max_price", String(query.maxPrice));
  }
  if (query.sort) {
    searchParams.set("sort", query.sort);
  }
  if (typeof query.limit === "number") {
    searchParams.set("limit", String(query.limit));
  }

  return apiRequest<RecommendationListResponse>(`/recommendations?${searchParams.toString()}`);
}

export async function getWishlist(category?: string): Promise<WishlistListResponse> {
  const query = category ? `?category=${encodeURIComponent(category)}` : "";
  return apiRequest<WishlistListResponse>(`/wishlist${query}`);
}

export async function addWishlist(productId: string): Promise<WishlistItem> {
  return apiRequest<WishlistItem>("/wishlist", {
    method: "POST",
    body: JSON.stringify({ product_id: productId }),
  });
}

export async function removeWishlist(productId: string): Promise<void> {
  return apiRequest<void>(`/wishlist/${encodeURIComponent(productId)}`, {
    method: "DELETE",
  });
}
