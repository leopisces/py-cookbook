import { test, expect } from "@playwright/test";

test.describe("首页", () => {
  test("页面加载并显示标题", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("h1")).toContainText("Python Cookbook");
    await expect(page.getByRole("heading", { name: "基础语法" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "数据类型" })).toBeVisible();
  });

  test("点击开始学习跳转到课程页", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("link", { name: "开始学习" }).click();
    await expect(page).toHaveURL(/\/learn\//);
  });
});

test.describe("课程页", () => {
  test("显示代码编辑器和学习目标", async ({ page }) => {
    await page.goto("/learn/01-basics/01_hello_world");
    await page.waitForSelector(".cm-editor", { timeout: 10000 });
    await expect(page.locator(".cm-editor")).toBeVisible();
    await expect(page.getByRole("heading", { name: "学习目标" })).toBeVisible();
  });

  test("侧边栏高亮当前章节", async ({ page }) => {
    await page.goto("/learn/01-basics/01_hello_world");
    await page.waitForSelector("aside", { timeout: 10000 });
    const activeLink = page.locator('a[href="/learn/01-basics/01_hello_world"]');
    await expect(activeLink).toHaveClass(/bg-blue-600/);
  });

  test("点击侧边栏切换章节", async ({ page }) => {
    await page.goto("/learn/01-basics/01_hello_world");
    await page.waitForSelector(".cm-editor", { timeout: 10000 });
    await page.locator('a[href="/learn/01-basics/02_syntax"]').click();
    await expect(page).toHaveURL(/\/learn\/01-basics\/02_syntax/);
  });

  test("运行按钮和重置按钮存在", async ({ page }) => {
    await page.goto("/learn/01-basics/01_hello_world");
    await page.waitForSelector(".cm-editor", { timeout: 10000 });
    await expect(page.getByRole("button", { name: "▶ 运行" })).toBeVisible();
    await expect(page.getByRole("button", { name: "重置" })).toBeVisible();
  });

  test("只读示例显示警告", async ({ page }) => {
    await page.goto("/learn/10-advanced/04_socket");
    await page.waitForSelector(".cm-editor", { timeout: 10000 });
    await expect(page.getByText("此示例需要完整 Python 环境运行")).toBeVisible();
  });
});

test.describe("深色模式", () => {
  test("点击切换按钮启用深色模式", async ({ page }) => {
    await page.goto("/learn/01-basics/01_hello_world");
    await page.waitForSelector(".cm-editor", { timeout: 10000 });

    // 找到深色模式切换按钮
    const toggleButton = page.locator('button[title*="暗色"]');
    await expect(toggleButton).toBeVisible();

    // 点击切换到深色模式
    await toggleButton.click();

    // 验证 html 元素添加了 dark class
    await expect(page.locator("html")).toHaveClass(/dark/);

    // 验证侧边栏背景变为深色
    const sidebar = page.locator("aside");
    await expect(sidebar).toHaveClass(/bg-gray-950/);
  });

  test("深色模式下首页样式正确", async ({ page }) => {
    await page.goto("/");

    // 点击深色模式按钮
    const toggleButton = page.locator('button[title*="暗色"]');
    await toggleButton.click();

    // 验证页面背景为深色
    const mainDiv = page.locator("div.min-h-screen");
    await expect(mainDiv).toHaveClass(/dark:from-gray-900/);
  });
});

test.describe("Pyodide 代码执行", () => {
  test("运行 Python 代码并显示输出", async ({ page }) => {
    test.setTimeout(60000);
    await page.goto("/learn/01-basics/01_hello_world");
    await page.waitForSelector(".cm-editor", { timeout: 10000 });
    await page.getByRole("button", { name: "▶ 运行" }).click();
    await page.waitForSelector("pre.text-green-400", { timeout: 30000 });
    const output = await page.locator("pre.text-green-400").textContent();
    expect(output!.length).toBeGreaterThan(0);
  });
});
