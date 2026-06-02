import { useState, useCallback } from "react";
import CodeEditor from "./CodeEditor";
import OutputPanel from "./OutputPanel";
import DescriptionPanel from "./DescriptionPanel";
import PyodideLoader from "./PyodideLoader";
import { usePyodide } from "../hooks/usePyodide";
import type { Section } from "../types/content";

interface CodeRunnerProps {
  section: Section;
}

export default function CodeRunner({ section }: CodeRunnerProps) {
  const [code, setCode] = useState(section.code);
  const pyodide = usePyodide();

  // 当 section 变化时重置代码
  const [prevSection, setPrevSection] = useState(section.id);
  if (prevSection !== section.id) {
    setCode(section.code);
    setPrevSection(section.id);
    pyodide.reset();
  }

  const handleRun = useCallback(() => {
    pyodide.runCode(code);
  }, [code, pyodide]);

  const handleReset = useCallback(() => {
    setCode(section.code);
    pyodide.reset();
  }, [section.code, pyodide]);

  return (
    <div className="flex flex-col h-full">
      {/* 描述面板 */}
      <DescriptionPanel section={section} />

      {/* Pyodide 加载状态 */}
      <PyodideLoader
        isLoading={pyodide.isLoading}
        isLoaded={pyodide.isLoaded}
        onLoad={pyodide.load}
      />

      {/* 代码编辑器 + 输出 */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* 工具栏 */}
        <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
          <span className="text-sm text-gray-400 font-mono">
            {section.chapterId}/{section.id}.py
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={handleReset}
              className="px-3 py-1 text-sm text-gray-400 hover:text-white
                         bg-gray-700 hover:bg-gray-600 rounded transition-colors"
            >
              重置
            </button>
            <button
              onClick={handleRun}
              disabled={pyodide.isRunning || pyodide.isLoading}
              className={`
                px-4 py-1 text-sm font-medium rounded transition-colors
                ${pyodide.isRunning || pyodide.isLoading
                  ? "bg-gray-600 text-gray-400 cursor-not-allowed"
                  : "bg-green-600 hover:bg-green-500 text-white"
                }
              `}
            >
              {pyodide.isRunning ? "运行中..." : "▶ 运行"}
            </button>
          </div>
        </div>

        {/* 代码编辑器区域 */}
        <div className="flex-1 min-h-0" style={{ minHeight: "300px" }}>
          <CodeEditor
            value={code}
            onChange={setCode}
            readOnly={!section.runnable}
          />
        </div>

        {/* 输出面板 */}
        <div style={{ height: "200px", minHeight: "120px" }}>
          <OutputPanel
            output={pyodide.output}
            error={pyodide.error}
            isRunning={pyodide.isRunning}
          />
        </div>
      </div>
    </div>
  );
}
