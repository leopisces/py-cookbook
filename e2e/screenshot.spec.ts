import { test } from "@playwright/test";

test("截图 - 亮色模式首页", async ({ page }) => {
  await page.goto("/");
  await page.waitForTimeout(1000);
  await page.screenshot({ path: "e2e/screenshots/home-light.png", fullPage: true });
});

test("截图 - 深色模式首页", async ({ page }) => {
  await page.goto("/");
  await page.waitForTimeout(500);
  await page.locator('button[title*="暗色"]').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: "e2e/screenshots/home-dark.png", fullPage: true });
});

test("截图 - 亮色模式课程页", async ({ page }) => {
  await page.goto("/learn/01-basics/01_hello_world");
  await page.waitForSelector(".cm-editor", { timeout: 10000 });
  await page.screenshot({ path: "e2e/screenshots/lesson-light.png", fullPage: true });
});

test("截图 - 深色模式课程页", async ({ page }) => {
  await page.goto("/learn/01-basics/01_hello_world");
  await page.waitForSelector(".cm-editor", { timeout: 10000 });
  await page.locator('button[title*="暗色"]').click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: "e2e/screenshots/lesson-dark.png", fullPage: true });
});
