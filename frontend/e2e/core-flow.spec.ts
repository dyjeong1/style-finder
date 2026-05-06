import { expect, Page, test } from "@playwright/test";

function okResponse(data: unknown) {
  return {
    data,
    error: null,
    meta: {
      request_id: "req-playwright",
      timestamp: "2026-05-03T00:00:00Z",
    },
  };
}

type UploadAnalysisFixture = {
  checksum: string;
  dominant_tone: string;
  dominant_color?: string;
  style_mood: string;
  silhouette: string;
  preferred_categories: string[];
  analysis_source: "vision" | "rule_fallback";
  query_source: "detected_items" | "rule_fallback" | "none";
  category_query_hints?: Record<string, string>;
  detected_items?: Array<{
    category: string;
    color: string;
    item_label: string;
    query: string;
  }>;
};

type RecommendationFixture = {
  query: string;
  analysis: UploadAnalysisFixture;
  items: Array<{
    product_id: string;
    source: string;
    product_name: string;
    category: string;
    price: number;
    product_url: string;
    image_url: string;
    similarity_score: number;
    rank: number;
    score_breakdown: {
      vector_similarity: number;
      tone_bonus: number;
      mood_bonus: number;
      silhouette_bonus: number;
      category_bonus: number;
    };
    matched_signals: {
      dominant_tone: string;
      dominant_color?: string;
      style_mood: string;
      silhouette: string;
      preferred_categories: string[];
    };
  }>;
};

const API_BASE = "http://127.0.0.1:8000";

function createWishlistRoutes() {
  const wishlistItems: Array<{
    id: string;
    product_id: string;
    product_name: string;
    source: string;
    category: string;
    price: number;
    product_url: string;
    image_url: string;
    created_at: string;
  }> = [];

  return {
    wishlistItems,
    async register(page: Page) {
      await page.route(`${API_BASE}/wishlist`, async (route) => {
        const method = route.request().method();

        if (method === "GET") {
          await route.fulfill({
            status: 200,
            contentType: "application/json",
            body: JSON.stringify(
              okResponse({
                items: wishlistItems,
                total_count: wishlistItems.length,
              }),
            ),
          });
          return;
        }

        if (method === "POST") {
          wishlistItems.push({
            id: "wsh-prd-top-001",
            product_id: "prd-top-001",
            product_name: "오버핏 스트라이프 셔츠",
            source: "zigzag",
            category: "top",
            price: 39000,
            product_url: "https://example.com/products/prd-top-001",
            image_url: "https://example.com/images/prd-top-001.jpg",
            created_at: "2026-05-03T00:00:00Z",
          });

          await route.fulfill({
            status: 200,
            contentType: "application/json",
            body: JSON.stringify(okResponse(wishlistItems[0])),
          });
          return;
        }

        await route.fallback();
      });

      await page.route(`${API_BASE}/wishlist/*`, async (route) => {
        if (route.request().method() === "DELETE") {
          wishlistItems.splice(0, wishlistItems.length);
          await route.fulfill({
            status: 204,
            body: "",
          });
          return;
        }

        await route.fallback();
      });
    },
  };
}

function createRecommendationFixtures(): Record<string, RecommendationFixture> {
  return {
    "upload-e2e-001": {
      query: "쿨톤 스트라이프 셔츠",
      analysis: {
        checksum: "abc123def4567890",
        dominant_tone: "cool",
        dominant_color: "blue",
        style_mood: "casual",
        silhouette: "relaxed",
        preferred_categories: ["top", "outer"],
        analysis_source: "vision",
        query_source: "detected_items",
        category_query_hints: {
          top: "블루 스트라이프 셔츠",
          outer: "네이비 가디건",
        },
        detected_items: [
          {
            category: "top",
            color: "blue",
            item_label: "스트라이프 셔츠",
            query: "블루 스트라이프 셔츠",
          },
        ],
      },
      items: [
        {
          product_id: "prd-top-001",
          source: "zigzag",
          product_name: "오버핏 스트라이프 셔츠",
          category: "top",
          price: 39000,
          product_url: "https://example.com/products/prd-top-001",
          image_url: "https://example.com/images/prd-top-001.jpg",
          similarity_score: 0.95,
          rank: 1,
          score_breakdown: {
            vector_similarity: 0.82,
            tone_bonus: 0.08,
            mood_bonus: 0.06,
            silhouette_bonus: 0.05,
            category_bonus: 0.04,
          },
          matched_signals: {
            dominant_tone: "cool",
            dominant_color: "blue",
            style_mood: "casual",
            silhouette: "relaxed",
            preferred_categories: ["top", "outer"],
          },
        },
      ],
    },
    "upload-sync-a": {
      query: "네이비 가디건",
      analysis: {
        checksum: "sync-a-checksum",
        dominant_tone: "cool",
        dominant_color: "navy",
        style_mood: "minimal",
        silhouette: "slim",
        preferred_categories: ["outer", "top"],
        analysis_source: "vision",
        query_source: "detected_items",
        category_query_hints: {
          outer: "네이비 가디건",
        },
        detected_items: [
          {
            category: "outer",
            color: "navy",
            item_label: "가디건",
            query: "네이비 가디건",
          },
        ],
      },
      items: [
        {
          product_id: "prd-sync-a-001",
          source: "zigzag",
          product_name: "네이비 가디건 크롭 가디건",
          category: "top",
          price: 52000,
          product_url: "https://example.com/products/prd-sync-a-001",
          image_url: "https://example.com/images/prd-sync-a-001.jpg",
          similarity_score: 0.91,
          rank: 1,
          score_breakdown: {
            vector_similarity: 0.8,
            tone_bonus: 0.05,
            mood_bonus: 0.03,
            silhouette_bonus: 0.02,
            category_bonus: 0.01,
          },
          matched_signals: {
            dominant_tone: "cool",
            dominant_color: "navy",
            style_mood: "minimal",
            silhouette: "slim",
            preferred_categories: ["outer", "top"],
          },
        },
      ],
    },
    "upload-sync-b": {
      query: "화이트 셔츠",
      analysis: {
        checksum: "sync-b-checksum",
        dominant_tone: "neutral",
        dominant_color: "white",
        style_mood: "classic",
        silhouette: "straight",
        preferred_categories: ["top", "bottom"],
        analysis_source: "vision",
        query_source: "detected_items",
        category_query_hints: {
          top: "화이트 셔츠",
          bottom: "블랙 슬랙스",
        },
        detected_items: [
          {
            category: "top",
            color: "white",
            item_label: "셔츠",
            query: "화이트 셔츠",
          },
          {
            category: "bottom",
            color: "black",
            item_label: "슬랙스",
            query: "블랙 슬랙스",
          },
        ],
      },
      items: [
        {
          product_id: "prd-sync-b-001",
          source: "29cm",
          product_name: "화이트 셔츠 레이어드 세트",
          category: "top",
          price: 61000,
          product_url: "https://example.com/products/prd-sync-b-001",
          image_url: "https://example.com/images/prd-sync-b-001.jpg",
          similarity_score: 0.93,
          rank: 1,
          score_breakdown: {
            vector_similarity: 0.81,
            tone_bonus: 0.06,
            mood_bonus: 0.03,
            silhouette_bonus: 0.02,
            category_bonus: 0.01,
          },
          matched_signals: {
            dominant_tone: "neutral",
            dominant_color: "white",
            style_mood: "classic",
            silhouette: "straight",
            preferred_categories: ["top", "bottom"],
          },
        },
      ],
    },
    "upload-race-a": {
      query: "민트 니트 베스트",
      analysis: {
        checksum: "race-a-checksum",
        dominant_tone: "cool",
        dominant_color: "mint",
        style_mood: "layered",
        silhouette: "boxy",
        preferred_categories: ["top"],
        analysis_source: "vision",
        query_source: "detected_items",
        detected_items: [
          {
            category: "top",
            color: "mint",
            item_label: "니트 베스트",
            query: "민트 니트 베스트",
          },
        ],
      },
      items: [
        {
          product_id: "prd-race-a-001",
          source: "zigzag",
          product_name: "민트 니트 베스트",
          category: "top",
          price: 47000,
          product_url: "https://example.com/products/prd-race-a-001",
          image_url: "https://example.com/images/prd-race-a-001.jpg",
          similarity_score: 0.88,
          rank: 1,
          score_breakdown: {
            vector_similarity: 0.76,
            tone_bonus: 0.05,
            mood_bonus: 0.04,
            silhouette_bonus: 0.02,
            category_bonus: 0.01,
          },
          matched_signals: {
            dominant_tone: "cool",
            dominant_color: "mint",
            style_mood: "layered",
            silhouette: "boxy",
            preferred_categories: ["top"],
          },
        },
      ],
    },
    "upload-race-b": {
      query: "버건디 가디건 자켓",
      analysis: {
        checksum: "race-b-checksum",
        dominant_tone: "warm",
        dominant_color: "burgundy",
        style_mood: "formal",
        silhouette: "tailored",
        preferred_categories: ["outer"],
        analysis_source: "vision",
        query_source: "detected_items",
        detected_items: [
          {
            category: "outer",
            color: "burgundy",
            item_label: "가디건 자켓",
            query: "버건디 가디건 자켓",
          },
        ],
      },
      items: [
        {
          product_id: "prd-race-b-001",
          source: "29cm",
          product_name: "버건디 가디건 재킷",
          category: "outer",
          price: 78000,
          product_url: "https://example.com/products/prd-race-b-001",
          image_url: "https://example.com/images/prd-race-b-001.jpg",
          similarity_score: 0.94,
          rank: 1,
          score_breakdown: {
            vector_similarity: 0.82,
            tone_bonus: 0.06,
            mood_bonus: 0.03,
            silhouette_bonus: 0.02,
            category_bonus: 0.01,
          },
          matched_signals: {
            dominant_tone: "warm",
            dominant_color: "burgundy",
            style_mood: "formal",
            silhouette: "tailored",
            preferred_categories: ["outer"],
          },
        },
      ],
    },
  };
}

test("@smoke 업로드부터 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다", async ({ page }) => {
  const fixtures = createRecommendationFixtures();
  const wishlist = createWishlistRoutes();
  const uploadedImageId = "upload-e2e-001";
  const uploadedFixture = fixtures[uploadedImageId];

  await wishlist.register(page);

  await page.route(`${API_BASE}/images/upload`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          id: uploadedImageId,
          image_url: "/mock-storage/upload-e2e-001-look.png",
          created_at: "2026-05-03T00:00:00Z",
          analysis: uploadedFixture.analysis,
        }),
      ),
    });
  });

  await page.route(`${API_BASE}/recommendations**`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          items: uploadedFixture.items,
          total_count: uploadedFixture.items.length,
          analysis: uploadedFixture.analysis,
          query: uploadedFixture.query,
        }),
      ),
    });
  });

  await page.goto("/recommendations");
  await expect(page.getByRole("heading", { name: "추천 상품" })).toBeVisible({ timeout: 20_000 });
  await expect(page.getByRole("button", { name: "현재 추천 기준 업로드 이미지 크게 보기" })).toHaveCount(0);

  await page.goto("/wishlist");
  await expect(page.getByRole("heading", { name: "찜 목록" })).toBeVisible({ timeout: 20_000 });

  await page.goto("/upload");
  await expect(page).toHaveURL(/\/upload$/);
  await expect(page.getByText("이미지를 넣으면 유사한 상품을 추천해드립니다.")).toBeVisible();

  await page.locator("#image-input").setInputFiles({
    name: "look.png",
    mimeType: "image/png",
    buffer: Buffer.from(
      "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9WlAbwAAAABJRU5ErkJggg==",
      "base64",
    ),
  });
  await page.getByRole("button", { name: "이미지 분석하기" }).click();

  await expect(page).toHaveURL(/\/recommendations\?uploaded_image_id=upload-e2e-001$/);
  await expect(page.getByRole("heading", { name: "추천 상품" })).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("AI 분석 기준")).toBeVisible();
  await expect(page.getByRole("button", { name: "현재 추천 기준 업로드 이미지 크게 보기" })).toHaveCount(1);
  await expect(page.locator(".uploaded-image-preview")).toBeVisible();
  await page.getByRole("button", { name: "현재 추천 기준 업로드 이미지 크게 보기" }).dispatchEvent("click");
  await expect(page.getByRole("dialog", { name: "추천 기준 업로드 이미지 확대 보기" })).toBeVisible();
  await expect(page.getByRole("button", { name: "업로드 이미지 확대 보기 닫기" })).toBeVisible();
  await page.getByRole("button", { name: "업로드 이미지 확대 보기 닫기" }).click();
  await expect(page.getByRole("dialog", { name: "추천 기준 업로드 이미지 확대 보기" })).toHaveCount(0);
  await expect(page.getByText("오버핏 스트라이프 셔츠")).toBeVisible();
  await expect(page.getByText("톤과 색상은 업로드 이미지의 대표 색상에서, 무드와 실루엣은 감지된 품목 조합에서 계산합니다.")).toBeVisible();
  await expect(page.getByText(/^검색어:/)).toHaveCount(0);
  const storedUploadState = await page.evaluate(() => ({
    uploadedImageId: window.localStorage.getItem("stylematch_uploaded_image_id"),
    uploadedImageAnalysis: window.localStorage.getItem("stylematch_uploaded_image_analysis"),
    uploadHistory: window.localStorage.getItem("stylematch_upload_history"),
  }));
  expect(storedUploadState).toEqual({
    uploadedImageId: null,
    uploadedImageAnalysis: null,
    uploadHistory: null,
  });

  await page.getByRole("button", { name: "오버핏 스트라이프 셔츠 찜 추가" }).click();
  await expect(page.getByText("상품이 찜 목록에 추가되었습니다: 오버핏 스트라이프 셔츠")).toBeVisible();

  await page.goto("/wishlist");
  await expect(page.getByRole("heading", { name: "찜 목록" })).toBeVisible({ timeout: 15_000 });
  await expect(page.getByText("오버핏 스트라이프 셔츠")).toBeVisible();
  await expect(page.getByText("ZIGZAG")).toBeVisible();
  await expect(page.getByText("39,000원")).toBeVisible();

  await page.getByRole("button", { name: "prd-top-001 찜 해제" }).click();
  await expect(page.getByText("저장된 찜 상품이 없습니다.")).toBeVisible();
});

test("업로드 분석 중 버튼 상태와 진행 시간을 보여준다", async ({ page }) => {
  const fixtures = createRecommendationFixtures();
  const uploadedImageId = "upload-e2e-001";
  const uploadedFixture = fixtures[uploadedImageId];

  await page.route(`${API_BASE}/images/upload`, async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 500));
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          id: uploadedImageId,
          image_url: "/mock-storage/upload-e2e-001-look.png",
          created_at: "2026-05-03T00:00:00Z",
          analysis: uploadedFixture.analysis,
        }),
      ),
    });
  });

  await page.route(`${API_BASE}/recommendations**`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          items: uploadedFixture.items,
          total_count: uploadedFixture.items.length,
          analysis: uploadedFixture.analysis,
          query: uploadedFixture.query,
        }),
      ),
    });
  });

  await page.goto("/upload");
  await page.locator("#image-input").setInputFiles({
    name: "slow-look.png",
    mimeType: "image/png",
    buffer: Buffer.from(
      "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9WlAbwAAAABJRU5ErkJggg==",
      "base64",
    ),
  });

  await page.getByRole("button", { name: "이미지 분석하기" }).click({ noWaitAfter: true });

  await expect(page.locator(".upload-primary-button[aria-busy='true']")).toBeVisible();
  await expect(page.locator(".upload-progress-text")).toContainText("분석 진행 시간 :");

  await expect(page).toHaveURL(/\/recommendations\?uploaded_image_id=upload-e2e-001$/);
});

test("최근 업로드 이미지를 다시 눌러 새 분석을 시작할 수 있다", async ({ page }) => {
  const fixtures = createRecommendationFixtures();
  const uploadedFixture = fixtures["upload-e2e-001"];
  const uploadedImageIds = ["upload-recent-001", "upload-recent-002"];
  let uploadRequestCount = 0;

  await page.route(`${API_BASE}/images/upload`, async (route) => {
    const uploadedImageId = uploadedImageIds[uploadRequestCount] ?? `upload-recent-${uploadRequestCount + 1}`;
    uploadRequestCount += 1;

    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          id: uploadedImageId,
          image_url: `/mock-storage/${uploadedImageId}.png`,
          created_at: "2026-05-04T00:00:00Z",
          analysis: uploadedFixture.analysis,
        }),
      ),
    });
  });

  await page.route(`${API_BASE}/recommendations**`, async (route) => {
    const uploadedImageId = new URL(route.request().url()).searchParams.get("uploaded_image_id");

    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          items: uploadedFixture.items,
          total_count: uploadedFixture.items.length,
          analysis: uploadedFixture.analysis,
          query: `${uploadedFixture.query} ${uploadedImageId ?? ""}`.trim(),
        }),
      ),
    });
  });

  await page.goto("/upload");
  await page.locator("#image-input").setInputFiles({
    name: "look.png",
    mimeType: "image/png",
    buffer: Buffer.from(
      "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9WlAbwAAAABJRU5ErkJggg==",
      "base64",
    ),
  });
  await page.getByRole("button", { name: "이미지 분석하기" }).click();

  await expect(page).toHaveURL(/\/recommendations\?uploaded_image_id=upload-recent-001$/);

  await page.goto("/upload");
  await expect(page.getByRole("heading", { name: "최근 업로드" })).toBeVisible();
  await expect(page.locator(".recent-upload-card-button")).toHaveCount(1);
  await expect(page.getByText("look.png")).toBeVisible();

  await page.locator(".recent-upload-card-button").first().click();

  await expect(page).toHaveURL(/\/recommendations\?uploaded_image_id=upload-recent-002$/);
  expect(uploadRequestCount).toBe(2);
});

test("@smoke 추천 페이지는 uploaded_image_id가 바뀌면 이전 검색어와 필터, 분석 요약을 초기화한다", async ({ page }) => {
  const fixtures = createRecommendationFixtures();
  const wishlist = createWishlistRoutes();

  await wishlist.register(page);

  await page.route(`${API_BASE}/recommendations**`, async (route) => {
    const requestUrl = new URL(route.request().url());
    const uploadedImageId = requestUrl.searchParams.get("uploaded_image_id");

    if (!uploadedImageId || !(uploadedImageId in fixtures)) {
      await route.fulfill({
        status: 404,
        contentType: "application/json",
        body: JSON.stringify({
          error: {
            code: "NOT_FOUND",
            message: "Recommendation result does not exist for uploaded_image_id",
            detail: {},
          },
        }),
      });
      return;
    }

    const fixture = fixtures[uploadedImageId];
    const customQuery = requestUrl.searchParams.get("custom_query");
    const query = customQuery || fixture.query;

    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          items: fixture.items,
          total_count: fixture.items.length,
          analysis: fixture.analysis,
          query,
        }),
      ),
    });
  });

  await page.goto("/recommendations?uploaded_image_id=upload-sync-a");
  await expect(page.getByText("네이비 가디건 크롭 가디건")).toBeVisible();
  await expect(page.getByText(/^검색어:/)).toHaveCount(0);
  await expect(page.getByText("감지 품목: 네이비 가디건")).toBeVisible();

  await page.locator("#recommendation-category").selectOption("top");
  await page.locator("#recommendation-sort").selectOption("price_desc");
  await page.locator("#recommendation-min-price").fill("15000");
  await page.locator("#recommendation-max-price").fill("45000");
  await page.locator("#recommendation-custom-query").fill("블랙 로퍼");
  await page.getByRole("button", { name: "검색어 적용" }).click();

  await expect(page.getByText("현재 직접 입력 검색어: 블랙 로퍼")).toBeVisible();
  await expect(page.getByText(/^검색어:/)).toHaveCount(0);

  await page.goto("/recommendations?uploaded_image_id=upload-sync-b");
  await expect(page.getByText("화이트 셔츠 레이어드 세트")).toBeVisible();
  await expect(page.getByText(/^검색어:/)).toHaveCount(0);
  await expect(page.getByText("감지 품목: 화이트 셔츠 / 블랙 슬랙스")).toBeVisible();
  await expect(page.getByText("네이비 가디건 크롭 가디건")).toHaveCount(0);
  await expect(page.getByText("현재 직접 입력 검색어: 블랙 로퍼")).toHaveCount(0);
  await expect(page.getByText("감지 품목: 네이비 가디건")).toHaveCount(0);
  await expect(page.locator("#recommendation-category")).toHaveValue("");
  await expect(page.locator("#recommendation-sort")).toHaveValue("similarity_desc");
  await expect(page.locator("#recommendation-min-price")).toHaveValue("");
  await expect(page.locator("#recommendation-max-price")).toHaveValue("");
  await expect(page.locator("#recommendation-custom-query")).toHaveValue("");
});

test("느린 이전 추천 응답이 새 uploaded_image_id 결과를 덮지 않는다", async ({ page }) => {
  const fixtures = createRecommendationFixtures();
  const wishlist = createWishlistRoutes();
  let releaseSlowResponse: (() => void) | null = null;
  let slowResponseStarted = 0;
  let slowResponseFulfilled = 0;

  await wishlist.register(page);

  await page.route(`${API_BASE}/recommendations**`, async (route) => {
    const requestUrl = new URL(route.request().url());
    const uploadedImageId = requestUrl.searchParams.get("uploaded_image_id");

    if (uploadedImageId === "upload-race-a") {
      slowResponseStarted += 1;
      await new Promise<void>((resolve) => {
        releaseSlowResponse = resolve;
      });
      slowResponseFulfilled += 1;
    }

    if (!uploadedImageId || !(uploadedImageId in fixtures)) {
      await route.fulfill({
        status: 404,
        contentType: "application/json",
        body: JSON.stringify({
          error: {
            code: "NOT_FOUND",
            message: "Recommendation result does not exist for uploaded_image_id",
            detail: {},
          },
        }),
      });
      return;
    }

    const fixture = fixtures[uploadedImageId];
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          items: fixture.items,
          total_count: fixture.items.length,
          analysis: fixture.analysis,
          query: fixture.query,
        }),
      ),
    });
  });

  await page.goto("/recommendations?uploaded_image_id=upload-race-a");
  await expect.poll(() => slowResponseStarted).toBe(1);
  await page.goto("/recommendations?uploaded_image_id=upload-race-b");

  await expect(page.getByText("버건디 가디건 재킷")).toBeVisible();
  await expect(page.getByText("감지 품목: 버건디 가디건 자켓")).toBeVisible();

  if (!releaseSlowResponse) {
    throw new Error("느린 이전 응답 해제 핸들러가 생성되지 않았습니다.");
  }

  releaseSlowResponse();
  await expect.poll(() => slowResponseFulfilled).toBe(1);

  await expect(page.getByText("버건디 가디건 재킷")).toBeVisible();
  await expect(page.getByText("민트 니트 베스트")).toHaveCount(0);
  await expect(page.getByText("감지 품목: 민트 니트 베스트")).toHaveCount(0);
  await expect(page.getByText(/^검색어:/)).toHaveCount(0);
});
