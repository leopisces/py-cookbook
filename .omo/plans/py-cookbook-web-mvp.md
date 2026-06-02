# Python Cookbook Web MVP Implementation Plan

## Overview

Build a web-based Python learning platform based on the existing `py-cookbook` project (69 demo files across 15 chapters). Users can browse knowledge points, read explanations, edit and run Python code directly in the browser using Pyodide.

## Architecture Decision

### Frontend: React + TypeScript + Vite
- Vite for fast HMR and build
- React 18 with hooks pattern
- TypeScript for type safety

### Code Editor: CodeMirror 6 (@uiw/react-codemirror)
- **Why NOT Monaco**: Monaco bundle is 5MB+, too heavy for a learning site; CodeMirror 6 is ~200KB with lazy loading
- @uiw/react-codemirror provides ready-made React integration
- Python language support via @codemirror/lang-python
- Theme: oneDark (popular, familiar to developers)

### Python Execution: Pyodide (browser-based)
- No backend needed for code execution
- Initial load ~5-10MB, takes ~5-10s → use lazy loading + loading indicator
- Some stdlib modules unavailable (subprocess, threading, multiprocessing, socket, os low-level)
- ~55 of 69 demo files can run in Pyodide; rest show as "view-only" with static output

### Styling: Tailwind CSS
- Rapid UI development
- Mobile-responsive by default
- Consistent design system

### Content Data: Static JSON (generated from .py files)
- Build script parses all 69 .py files → structured JSON
- Each entry: chapter, title, description (学习目标), code, demo functions
- No database needed for MVP

### Deployment: Vite static build
- Build once → deploy anywhere (GitHub Pages, Vercel, Netlify)
- SPA with client-side routing

## Project Structure

```
py-cookbook-web/
├── public/
│   └── favicon.svg
├── scripts/
│   └── build-content.ts          # Parse .py files → JSON
├── src/
│   ├── App.tsx                    # Root component + routing
│   ├── main.tsx                   # Entry point
│   ├── components/
│   │   ├── Layout.tsx             # Shell: sidebar + header + content
│   │   ├── Sidebar.tsx            # Chapter/section navigation tree
│   │   ├── CodeRunner.tsx         # Editor + run button + output
│   │   ├── CodeEditor.tsx         # CodeMirror wrapper
│   │   ├── PyodideLoader.tsx      # Lazy Pyodide load + progress indicator
│   │   ├── OutputPanel.tsx        # stdout/stderr display
│   │   ├── DescriptionPanel.tsx   # 学习目标 + explanation
│   │   └── SearchBar.tsx          # Quick search across chapters
│   ├── hooks/
│   │   ├── usePyodide.ts          # Pyodide init + runCode + getOutput
│   │   └── useContent.ts          # Load content JSON
│   ├── data/
│   │   └── content.json           # Generated from .py files
│   ├── types/
│   │   └ content.ts               # TypeScript interfaces
│   └── styles/
│       └ globals.css               # Tailwind base
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└ README.md
```

## Data Model (TypeScript Interfaces)

```typescript
interface Chapter {
  id: string;          // "01-basics"
  title: string;       // "基础语法"
  description: string; // Chapter overview
  order: number;       // Sort order
  sections: Section[];
}

interface Section {
  id: string;          // "01_hello_world"
  title: string;       // "第一个程序"
  chapterId: string;   // "01-basics"
  description: string; // 学习目标 (from docstring)
  goals: string[];     // Bullet list from docstring
  code: string;        // Full .py file content
  runnable: boolean;   // Can run in Pyodide?
  output?: string;     // Pre-computed output for non-runnable files
  tags: string[];      // ["print", "f-string", "中文"]
}
```

## Key Components Detail

### 1. CodeRunner.tsx (Core interaction component)
- Layout: DescriptionPanel (left/top) + CodeEditor (center) + OutputPanel (bottom)
- "Run" button triggers Pyodide execution
- "Reset" button restores original code
- Shows loading state while Pyodide initializes
- For non-runnable files: shows code as read-only + static output

### 2. PyodideLoader.tsx (Async loading strategy)
- Load Pyodide on first "Run" click (NOT on page load — saves initial bandwidth)
- Show progress bar during ~5-10s load
- After loaded, cache in memory for subsequent runs
- Handle load failure gracefully with fallback message

### 3. usePyodide.ts (Custom hook)
```
State: { isLoaded, isLoading, isRunning, output, error, loadProgress }
Actions: { loadPyodide(), runCode(code: string), reset() }

runCode flow:
1. If not loaded → trigger loadPyodide()
2. Redirect stdout/stderr to capture buffer
3. Execute code via pyodide.runPythonAsync()
4. Return captured output + any error
```

### 4. Sidebar.tsx (Navigation)
- Collapsible chapter tree
- Current section highlighted
- Responsive: collapsible on mobile
- Search filter for quick find

## Runnable Classification

Files that **CAN** run in Pyodide (~55):
- 01-basics (all 7)
- 02-datatypes (all 7)
- 03-control-flow (all 4)
- 04-functions (all 5)
- 05-oop (all 3)
- 06-modules (01, 02 — skip 03 pip)
- 07-io (01, 02, 04 — skip 03 os)
- 08-errors (all 4)
- 09-stdlib (01-14, 17-19 — skip 15 subprocess, 16 queue limited)
- 11-builtin (all 3)
- 12-pattern-matching (1)
- 13-dataclass_enum (2)
- 14-typing (2)

Files that **CANNOT** run in Pyodide (~14):
- 10-advanced (all 5 — threading, asyncio, socket, multiprocessing)
- 09-stdlib/15_subprocess (subprocess module unavailable)
- 09-stdlib/16_queue (threading-based, limited)
- 06-modules/03_pip_package (pip unavailable)
- 07-io/03_os_module (os low-level unavailable)

For non-runnable files: show code + static pre-computed output, mark as "此示例需要完整Python环境"

## Build Content Script (scripts/build-content.ts)

Parse each .py file:
1. Extract module-level docstring → title + description + goals
2. Read full file content → code field
3. Check for Pyodide-incompatible imports (subprocess, threading, socket, os, multiprocessing)
4. Run original file via subprocess → capture output for non-runnable fallback
5. Generate content.json with all structured data

## UI Design

### Color Theme
- Background: dark slate (#0f172a) or light mode (#f8fafc)
- Primary accent: Python blue (#306998) + yellow (#ffd43b)
- Code editor: oneDark theme
- Sidebar: slightly darker/different background

### Layout
- Desktop: Sidebar (280px) + Content area
- Mobile: Collapsible sidebar + full-width content
- Code editor: min 60% width, resizable
- Output panel: below editor, collapsible

## MVP Feature Scope

### Must Have (Phase 1)
- [x] Chapter/section navigation sidebar
- [x] Code display with syntax highlighting (CodeMirror)
- [x] In-browser Python execution (Pyodide)
- [x] Run button + output display
- [x] Editable code (user can modify before running)
- [x] Reset to original code
- [x] Description/学习目标 display
- [x] Responsive layout (desktop + mobile)
- [x] Non-runnable file fallback (static output)
- [x] Pyodide lazy loading with progress indicator

### Nice to Have (Phase 2 - defer)
- [ ] Search across all content
- [ ] Dark/light theme toggle
- [ ] Code sharing (copy URL with code state)
- [ ] Progress tracking (localStorage)
- [ ] Bookmark/favorite sections
- [ ] Mobile PWA support

### Not in MVP
- [ ] User accounts / authentication
- [ ] Database / backend server
- [ ] Comments / discussion
- [ ] Content management system

## Implementation Timeline

### Step 1: Project Setup (1 task)
- Initialize Vite + React + TypeScript project
- Install dependencies: @uiw/react-codemirror, @codemirror/lang-python, tailwindcss
- Configure Tailwind, Vite, TypeScript

### Step 2: Content Build Script (1 task)
- Write scripts/build-content.ts to parse all 69 .py files
- Generate src/data/content.json
- Handle Pyodide compatibility classification
- Pre-compute static output for non-runnable files

### Step 3: Core Components (3 parallel tasks)
- Layout + Sidebar + Routing (visual-engineering)
- CodeEditor + CodeRunner (visual-engineering)
- Pyodide hook + Loader (deep)

### Step 4: Integration & Polish (1 task)
- Wire all components together
- Responsive design tweaks
- Handle edge cases (non-runnable, errors, timeout)
- Final testing

## Risk Mitigation

1. **Pyodide load time**: Lazy load on first "Run" click, show progress bar, provide fallback message
2. **Non-runnable files**: Pre-compute output during build, mark clearly, don't show Run button
3. **Content extraction reliability**: AST-based parser for docstrings, fallback to regex
4. **CodeMirror bundle size**: Lazy load editor component, only load when section is opened
5. **Mobile responsiveness**: Tailwind responsive classes, collapsible sidebar

## Dependencies

```json
{
  "dependencies": {
    "react": "^18.3",
    "react-dom": "^18.3",
    "react-router-dom": "^6.23",
    "@uiw/react-codemirror": "^4.21",
    "@codemirror/lang-python": "^6.1",
    "@codemirror/theme-one-dark": "^6.1"
  },
  "devDependencies": {
    "vite": "^5.4",
    "@types/react": "^18.3",
    "@types/react-dom": "^18.3",
    "typescript": "^5.5",
    "tailwindcss": "^3.4",
    "postcss": "^8.4",
    "autoprefixer": "^10.4",
    "@vitejs/plugin-react": "^4.3"
  }
}
```

Pyodide loaded from CDN at runtime (not bundled):
```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
```
Or dynamically loaded via usePyodide hook.