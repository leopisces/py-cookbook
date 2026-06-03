/**
 * build-content.ts
 * 解析 demos/ 目录下所有 .py demo 文件，生成 content.json 供前端使用。
 * 运行: npx tsx scripts/build-content.ts
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// ESM 兼容的 __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================================
// 类型定义
// ============================================================

interface Chapter {
  id: string;
  title: string;
  description: string;
  order: number;
  sections: Section[];
}

interface Section {
  id: string;
  title: string;
  chapterId: string;
  description: string;
  goals: string[];
  code: string;
  runnable: boolean;
  output?: string;
  tags: string[];
}

interface ContentData {
  chapters: Chapter[];
  generatedAt: string;
}

// ============================================================
// 章节元数据
// ============================================================

const CHAPTER_META: Record<string, { title: string; description: string }> = {
  "01-basics": { title: "基础语法", description: "Python 入门基础：Hello World、语法、注释、运算符、类型转换、数字、字符串" },
  "02-datatypes": { title: "数据类型", description: "Python 核心数据类型：列表、元组、字典、集合、bytes、数据结构" },
  "03-control-flow": { title: "流程控制", description: "条件判断、for 循环、while 循环、推导式" },
  "04-functions": { title: "函数", description: "函数定义、lambda、装饰器、迭代器与生成器、作用域" },
  "05-oop": { title: "面向对象", description: "类与对象、继承与多态、魔术方法与类型注解" },
  "06-modules": { title: "模块与包", description: "import 机制、__name__ 与 __main__、pip 包管理" },
  "07-io": { title: "输入输出", description: "print 格式化、文件读写、OS 模块、with 语句" },
  "08-errors": { title: "异常处理", description: "try/except、自定义异常、异常链、warnings 警告" },
  "09-stdlib": { title: "标准库", description: "math/random/datetime/re/json/csv/sys/hashlib/pickle/logging/itertools/collections/functools 等" },
  "10-advanced": { title: "高级特性", description: "多线程、异步编程、XML 解析、网络编程、多进程" },
  "11-builtin": { title: "内置函数", description: "类型与对象、数学与迭代、输入输出与执行相关内置函数" },
  "12-pattern-matching": { title: "模式匹配", description: "Python 3.10+ match/case 结构化模式匹配" },
  "13-dataclass_enum": { title: "数据类与枚举", description: "dataclass 数据类、enum 枚举类型" },
  "14-typing": { title: "类型注解", description: "Python 类型系统：基础注解、TypeVar、Generic、Protocol、高级类型" },
  "15-testing": { title: "单元测试", description: "pytest 基础与高级功能" },
};

// Pyodide 不支持的模块
const PYODIDE_INCOMPATIBLE_IMPORTS = new Set([
  "subprocess",
  "socket",
  "multiprocessing",
  "threading",
  "pip",
  "shutil",
]);

// 文件级别的不可运行标记（相对于 demos/ 的路径）
const FILE_OVERRIDES: Record<string, boolean> = {
  "06-modules/03_pip_package.py": false,
  "07-io/03_os_module.py": false,
  "09-stdlib/15_subprocess.py": false,
  "10-advanced/01_threading.py": false,
  "10-advanced/02_asyncio.py": false,
  "10-advanced/04_socket.py": false,
  "10-advanced/05_multiprocessing.py": false,
};

// ============================================================
// 解析函数
// ============================================================

const DEMOS_ROOT = path.resolve(__dirname, "..", "demos");

function extractDocstring(source: string): string {
  const match = source.match(/^"""([\s\S]*?)"""/);
  if (match) return match[1].trim();
  const match2 = source.match(/^'''([\s\S]*?)'''/);
  if (match2) return match2[1].trim();
  return "";
}

function parseTitle(docstring: string): string {
  const lines = docstring.split("\n").filter((l) => l.trim());
  return lines[0]?.trim() || "";
}

function parseGoals(docstring: string): string[] {
  const goals: string[] = [];
  const lines = docstring.split("\n");
  let inGoals = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.includes("学习目标") || trimmed.includes("涵盖内容") || trimmed.includes("核心知识点")) {
      inGoals = true;
      continue;
    }
    if (inGoals) {
      if (trimmed.startsWith("-")) {
        goals.push(trimmed.slice(2).trim());
      } else if (trimmed === "" && goals.length > 0) {
        continue;
      } else if (
        trimmed &&
        !trimmed.startsWith("=") &&
        !trimmed.startsWith("参考") &&
        !trimmed.startsWith("Python") &&
        !trimmed.startsWith("运行")
      ) {
        if (goals.length > 0 && !trimmed.startsWith("·")) {
          break;
        }
      }
    }
  }
  return goals;
}

function parseDescription(docstring: string): string {
  const lines = docstring.split("\n");
  const descLines: string[] = [];
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.includes("学习目标") || trimmed.includes("涵盖内容")) break;
    if (trimmed && !trimmed.startsWith("=")) {
      descLines.push(trimmed);
    }
  }
  return descLines.join(" ").trim();
}

function isRunnable(relPath: string, source: string): boolean {
  // 文件级别覆盖
  if (relPath in FILE_OVERRIDES) {
    return FILE_OVERRIDES[relPath];
  }

  // 检查 import 语句
  const lines = source.split("\n");
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    if (
      !trimmed.startsWith("import ") &&
      !trimmed.startsWith("from ") &&
      !trimmed.startsWith('"""') &&
      !trimmed.startsWith("'''") &&
      !trimmed.startsWith("# -*-")
    ) {
      if (
        trimmed.startsWith("class ") ||
        trimmed.startsWith("def ") ||
        trimmed.startsWith("@")
      ) {
        break;
      }
      continue;
    }

    const fromMatch = trimmed.match(/^from\s+(\w+)/);
    if (fromMatch && PYODIDE_INCOMPATIBLE_IMPORTS.has(fromMatch[1])) {
      return false;
    }

    const importMatch = trimmed.match(/^import\s+(\w+)/);
    if (importMatch && PYODIDE_INCOMPATIBLE_IMPORTS.has(importMatch[1])) {
      return false;
    }
  }

  return true;
}

function extractTags(source: string): string[] {
  const tags = new Set<string>();
  const importRegex = /^(?:from\s+(\w+)|import\s+(\w+))/gm;
  let match;
  while ((match = importRegex.exec(source)) !== null) {
    const mod = match[1] || match[2];
    if (mod && !["os", "sys", "__future__"].includes(mod)) {
      tags.add(mod);
    }
  }
  return Array.from(tags).slice(0, 8);
}

function scanChapterDir(chapterDir: string, chapterId: string): Section[] {
  const sections: Section[] = [];
  const files = fs
    .readdirSync(chapterDir)
    .filter((f: string) => f.endsWith(".py") && !f.startsWith("__"))
    .sort();

  for (const file of files) {
    const filePath = path.join(chapterDir, file);
    const source = fs.readFileSync(filePath, "utf-8");
    const docstring = extractDocstring(source);
    const id = file.replace(".py", "");
    const title = parseTitle(docstring) || id;
    const goals = parseGoals(docstring);
    const description = parseDescription(docstring) || goals.join("；");
    const relPath = `${chapterId}/${file}`;
    const runnable = isRunnable(relPath, source);
    const tags = extractTags(source);

    sections.push({
      id,
      title,
      chapterId,
      description,
      goals,
      code: source,
      runnable,
      tags,
    });
  }

  return sections;
}

// ============================================================
// 主函数
// ============================================================

function main() {
  console.log("Building content.json from demos/...");
  console.log(`Source: ${DEMOS_ROOT}`);

  if (!fs.existsSync(DEMOS_ROOT)) {
    console.error(`Error: demos/ directory not found at ${DEMOS_ROOT}`);
    process.exit(1);
  }

  const chapterDirs = fs
    .readdirSync(DEMOS_ROOT)
    .filter((d: string) => /^\d{2}-/.test(d) && fs.statSync(path.join(DEMOS_ROOT, d)).isDirectory())
    .sort();

  const chapters: Chapter[] = [];
  let totalSections = 0;
  let runnableCount = 0;

  for (const dirName of chapterDirs) {
    const chapterDir = path.join(DEMOS_ROOT, dirName);
    const meta = CHAPTER_META[dirName] || { title: dirName, description: "" };
    const sections = scanChapterDir(chapterDir, dirName);

    const chapter: Chapter = {
      id: dirName,
      title: meta.title,
      description: meta.description,
      order: chapters.length + 1,
      sections,
    };

    chapters.push(chapter);
    totalSections += sections.length;
    runnableCount += sections.filter((s) => s.runnable).length;

    console.log(`  ${dirName}: ${sections.length} sections (${sections.filter((s) => s.runnable).length} runnable)`);
  }

  const content: ContentData = {
    chapters,
    generatedAt: new Date().toISOString(),
  };

  const outDir = path.resolve(__dirname, "..", "src", "data");
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const outPath = path.join(outDir, "content.json");
  fs.writeFileSync(outPath, JSON.stringify(content, null, 2), "utf-8");

  console.log(`\nGenerated: ${outPath}`);
  console.log(`Total: ${chapters.length} chapters, ${totalSections} sections`);
  console.log(`Runnable: ${runnableCount}, View-only: ${totalSections - runnableCount}`);
}

main();
