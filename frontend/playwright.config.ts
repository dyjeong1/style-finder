import { defineConfig, devices } from "@playwright/test";

const useLocalServer = process.env.E2E_SERVER_MODE === "local";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  fullyParallel: true,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: {
    command: useLocalServer ? "npm run local" : "npm run dev -- --hostname 127.0.0.1 --port 3000",
    url: "http://127.0.0.1:3000/upload",
    reuseExistingServer: !process.env.CI,
    timeout: useLocalServer ? 180_000 : 120_000,
  },
});
