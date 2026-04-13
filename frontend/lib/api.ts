const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

const TOKEN_KEY = "stylematch_access_token";
const UPLOADED_IMAGE_ID_KEY = "stylematch_uploaded_image_id";

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

type LoginResponse = {
  access_token: string;
  token_type: string;
  expires_in: number;
};

export type UploadedImage = {
  id: string;
  image_url: string;
  created_at: string;
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
};

type RecommendationListResponse = {
  items: RecommendationItem[];
  total_count: number;
};

export type WishlistItem = {
  id: string;
  product_id: string;
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

async function apiRequest<T>(path: string, options?: RequestInit & { token?: string }): Promise<T> {
  const { token, headers, ...restOptions } = options ?? {};
  const mergedHeaders = new Headers(headers ?? {});

  if (token) {
    mergedHeaders.set("Authorization", `Bearer ${token}`);
  }

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

export function getStoredToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearStoredToken(): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(TOKEN_KEY);
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

export async function login(email: string, password: string): Promise<LoginResponse> {
  return apiRequest<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function uploadImage(image: File, token: string): Promise<UploadedImage> {
  const formData = new FormData();
  formData.append("image", image);

  return apiRequest<UploadedImage>("/images/upload", {
    method: "POST",
    body: formData,
    token,
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

export async function getRecommendations(query: RecommendationQuery, token: string): Promise<RecommendationListResponse> {
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

  return apiRequest<RecommendationListResponse>(`/recommendations?${searchParams.toString()}`, {
    token,
  });
}

export async function getWishlist(token: string, category?: string): Promise<WishlistListResponse> {
  const query = category ? `?category=${encodeURIComponent(category)}` : "";
  return apiRequest<WishlistListResponse>(`/wishlist${query}`, { token });
}

export async function addWishlist(productId: string, token: string): Promise<WishlistItem> {
  return apiRequest<WishlistItem>("/wishlist", {
    method: "POST",
    token,
    body: JSON.stringify({ product_id: productId }),
  });
}

export async function removeWishlist(productId: string, token: string): Promise<void> {
  return apiRequest<void>(`/wishlist/${encodeURIComponent(productId)}`, {
    method: "DELETE",
    token,
  });
}
