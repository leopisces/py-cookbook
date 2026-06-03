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
      <DescriptionPanel section={section} />

      <PyodideLoader
        isLoading={pyodide.isLoading}
        isLoaded={pyodide.isLoaded}
        onLoad={pyodide.load}
      />

      <div className="flex-1 flex flex-col min-h-0">
        {/* Toolbar */}
        <div className="flex items-center justify-between px-4 py-2.5
                        bg-surface-800 dark:bg-surface-900
                        border-b border-surface-700/60 dark:border-surface-800/60
                        transition-colors duration-200 ease-out">
          <span className="text-xs text-surface-400 dark:text-surface-500 font-mono tracking-wide">
            {section.chapterId}/{section.id}.py
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={handleReset}
              className="px-3 py-1.5 text-xs font-medium text-surface-400 dark:text-surface-500
                         hover:text-white bg-surface-700/80 dark:bg-surface-800
                         hover:bg-surface-600 dark:hover:bg-surface-700
                         rounded-lg transition-all duration-150 ease-out
                         active:scale-95"
            >
              重置
            </button>
            <button
              onClick={handleRun}
              disabled={pyodide.isRunning || pyodide.isLoading}
              className={`
                px-4 py-1.5 text-xs font-semibold rounded-lg
                transition-all duration-150 ease-out active:scale-95
                ${pyodide.isRunning || pyodide.isLoading
                  ? "bg-surface-600 dark:bg-surface-700 text-surface-400 dark:text-surface-500 cursor-not-allowed"
                  : "bg-primary-600 hover:bg-primary-500 text-white shadow-sm shadow-primary-600/25 hover:shadow-md hover:shadow-primary-500/30"
                }
              `}
            >
              {pyodide.isRunning ? "运行中..." : "▶ 运行"}
            </button>
          </div>
        </div>

        {/* Code editor */}
        <div className="flex-[2] min-h-0 overflow-auto">
          <CodeEditor
            value={code}
            onChange={setCode}
            readOnly={!section.runnable}
          />
        </div>

        {/* Output panel */}
        <div className="flex-1 min-h-[120px] max-h-[250px] overflow-auto
                        border-t border-surface-700/60 dark:border-surface-800/60">
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
