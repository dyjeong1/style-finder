import { expect, test } from "@playwright/test";

function okResponse(data: unknown) {
  return {
    data,
    error: null,
    meta: {
      request_id: "req-playwright",
      timestamp: "2026-04-14T00:00:00Z",
    },
  };
}

test("로그인부터 업로드, 추천, 찜 추가/삭제까지 핵심 흐름이 동작한다", async ({ page }) => {
  const wishlistItems: Array<{ id: string; product_id: string; created_at: string }> = [];
  const uploadedImageId = "upload-e2e-001";
  const productId = "prd-top-001";
  const apiBase = "http://localhost:8000";

  await page.route(`${apiBase}/auth/login`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          access_token: "token-e2e",
          token_type: "bearer",
          expires_in: 3600,
        }),
      ),
    });
  });

  await page.route(`${apiBase}/images/upload`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          id: uploadedImageId,
          image_url: "/mock-storage/upload-e2e-001-look.png",
          created_at: "2026-04-14T00:00:00Z",
        }),
      ),
    });
  });

  await page.route(`${apiBase}/recommendations**`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(
        okResponse({
          items: [
            {
              product_id: productId,
              source: "zigzag",
              product_name: "오버핏 스트라이프 셔츠",
              category: "top",
              price: 39000,
              product_url: "https://example.com/products/prd-top-001",
              image_url: "https://example.com/images/prd-top-001.jpg",
              similarity_score: 0.95,
              rank: 1,
            },
          ],
          total_count: 1,
        }),
      ),
    });
  });

  await page.route(`${apiBase}/wishlist`, async (route) => {
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
        product_id: productId,
        created_at: "2026-04-14T00:00:00Z",
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

  await page.route(`${apiBase}/wishlist/*`, async (route) => {
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

  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@stylematch.com");
  await page.getByLabel("Password").fill("stylematch1234");
  await page.getByRole("button", { name: "Sign In" }).click();

  await expect(page).toHaveURL(/\/upload$/);
  await expect(page.getByRole("heading", { name: "Upload Outfit Image" })).toBeVisible();

  await page.locator("#image-input").setInputFiles({
    name: "look.png",
    mimeType: "image/png",
    buffer: Buffer.from(
      "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9WlAbwAAAABJRU5ErkJggg==",
      "base64",
    ),
  });
  await page.getByRole("button", { name: "Upload & Analyze" }).click();

  await expect(page).toHaveURL(/\/recommendations$/);
  await expect(page.getByRole("heading", { name: "Recommendations" })).toBeVisible();
  await expect(page.getByText("오버핏 스트라이프 셔츠")).toBeVisible();

  await page.getByRole("button", { name: "오버핏 스트라이프 셔츠 찜 추가" }).click();
  await expect(page.getByText(`상품이 찜 목록에 추가되었습니다: ${productId}`)).toBeVisible();

  await page.goto("/wishlist");
  await expect(page.getByRole("heading", { name: "Wishlist" })).toBeVisible();
  await expect(page.getByText(productId)).toBeVisible();

  await page.getByRole("button", { name: `${productId} 찜 해제` }).click();
  await expect(page.getByText("저장된 찜 상품이 없습니다.")).toBeVisible();
});
