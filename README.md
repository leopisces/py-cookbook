# Python Cookbook - 交互式学习平台

基于 React + TypeScript + Vite + Pyodide 的浏览器内 Python 交互式学习平台。

## 特性

- 🐍 浏览器内直接运行 Python 代码（Pyodide）
- 🌗 亮色/暗色主题切换
- 📐 设计令牌系统（emerald primary + slate surface）
- 🖥️ 代码编辑器 + 右侧输出抽屉面板
- 🔄 流式输出展示，模拟终端运行效果
- 📱 响应式布局

## 快速开始

```bash
# 安装依赖
npm install

# 开发模式（自动扫描 demos/ 生成内容）
npm run dev

# 构建
npm run build
```

## 添加新的 Demo

在 `demos/` 目录下按约定结构添加 `.py` 文件即可，无需手动编辑 JSON。

### 文件组织

```
demos/
├── 01-basics/           # 章节（文件夹名 = 章节 ID）
│   ├── 01_hello_world.py  # 小节（文件名 = 小节 ID）
│   ├── 02_syntax.py
│   └── ...
├── 02-datatypes/
│   └── ...
└── 16-my-topic/         # 新增章节
    └── 01_my_demo.py    # 新增示例
```

### .py 文件格式

文件开头写 docstring，脚本会自动解析标题和学习目标：

```python
"""
你的标题 - 副标题

学习目标：
  - 目标一
  - 目标二
  - 目标三
"""

def main():
    print("Hello!")
    # ... 你的代码
```

### 可运行性检测

脚本会自动检测 `import` 语句判断是否可在 Pyodide 中运行。以下模块会被标记为不可运行：

`subprocess`、`socket`、`multiprocessing`、`threading`、`pip`、`shutil`

也可在 `scripts/build-content.ts` 的 `FILE_OVERRIDES` 中手动指定：

```ts
const FILE_OVERRIDES: Record<string, boolean> = {
  "06-modules/03_pip_package.py": false,
};
```

### 新增章节

新增章节文件夹后，需在 `scripts/build-content.ts` 的 `CHAPTER_META` 中补上中文标题和描述：

```ts
const CHAPTER_META: Record<string, { title: string; description: string }> = {
  // ...existing...
  "16-my-topic": { title: "我的主题", description: "主题简介" },
};
```

### 自动化

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动开发服务器（自动先扫描 demos/） |
| `npm run build` | 构建生产版本（自动先扫描 demos/） |
| `npm run generate` | 单独重新生成 content.json |

开发模式下修改 `demos/` 里的 `.py` 文件，Vite 会自动重新生成 `content.json` 并热更新浏览器。

## 技术栈

- **React 19** + **TypeScript 6**
- **Vite 8** + **Tailwind CSS v4**
- **CodeMirror** (Python 语法高亮 + oneDark 主题)
- **Pyodide 0.24** (浏览器内 Python 运行时)
- **React Router 7**

## 项目结构

```
src/
├── components/
│   ├── CodeEditor.tsx      # 代码编辑器（主题自适应）
│   ├── CodeRunner.tsx      # 主编辑器容器 + 输出抽屉
│   ├── OutputPanel.tsx     # 输出面板（流式展示+闪烁光标）
│   ├── Sidebar.tsx         # 侧边栏导航
│   ├── ThemeToggle.tsx     # 主题切换
│   └── Layout.tsx          # 页面布局
├── hooks/
│   ├── useContent.ts       # 内容数据加载
│   ├── usePyodide.ts       # Pyodide 运行时（自动加载+流式输出）
│   └── useTheme.ts         # 主题管理
├── data/
│   └── content.json        # 自动生成，勿手动编辑
├── pages/
│   ├── HomePage.tsx        # 首页
│   └── LessonPage.tsx      # 课程页
├── types/
│   └── content.ts          # 类型定义
└── index.css               # 全局样式 + 设计令牌
demos/                       # Python demo 源文件
scripts/
└── build-content.ts        # demos/ → content.json 构建脚本
```
