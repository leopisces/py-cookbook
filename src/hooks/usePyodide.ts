import { useState, useCallback, useRef } from "react";

interface PyodideState {
  isLoaded: boolean;
  isLoading: boolean;
  isRunning: boolean;
  output: string;
  error: string;
}

// Pyodide 全局单例
let pyodideInstance: unknown = null;
let pyodidePromise: Promise<unknown> | null = null;

async function loadPyodideOnce(): Promise<unknown> {
  if (pyodideInstance) return pyodideInstance;
  if (pyodidePromise) return pyodidePromise;

  pyodidePromise = (async () => {
    // 动态加载 Pyodide 脚本
    if (!(window as Record<string, unknown>).loadPyodide) {
      await new Promise<void>((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js";
        script.onload = () => resolve();
        script.onerror = () => reject(new Error("Failed to load Pyodide"));
        document.head.appendChild(script);
      });
    }

    const loadFn = (window as Record<string, unknown>).loadPyodide as (opts: Record<string, unknown>) => Promise<unknown>;
    pyodideInstance = await loadFn({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/",
    });
    return pyodideInstance;
  })();

  return pyodidePromise;
}

export function usePyodide() {
  const [state, setState] = useState<PyodideState>({
    isLoaded: false,
    isLoading: false,
    isRunning: false,
    output: "",
    error: "",
  });

  const outputRef = useRef("");
  const errorRef = useRef("");

  const load = useCallback(async () => {
    if (pyodideInstance || state.isLoading) return;
    setState((s) => ({ ...s, isLoading: true }));
    try {
      await loadPyodideOnce();
      setState((s) => ({ ...s, isLoaded: true, isLoading: false }));
    } catch (err) {
      setState((s) => ({
        ...s,
        isLoading: false,
        error: `加载 Pyodide 失败: ${err instanceof Error ? err.message : String(err)}`,
      }));
    }
  }, [state.isLoading]);

  const runCode = useCallback(
    async (code: string) => {
      if (!pyodideInstance) {
        await load();
      }
      if (!pyodideInstance) return;

      setState((s) => ({ ...s, isRunning: true, output: "", error: "" }));
      outputRef.current = "";
      errorRef.current = "";

      try {
        const pyodide = pyodideInstance as {
          setStdout: (opts: { batched: (msg: string) => void }) => void;
          setStderr: (opts: { batched: (msg: string) => void }) => void;
          runPythonAsync: (code: string) => Promise<unknown>;
          globals: { get: (name: string) => unknown };
        };

        pyodide.setStdout({
          batched: (msg: string) => {
            outputRef.current += msg + "\n";
          },
        });
        pyodide.setStderr({
          batched: (msg: string) => {
            errorRef.current += msg + "\n";
          },
        });

        // 运行代码（重置全局变量避免跨课污染）
        await pyodide.runPythonAsync(code);

        setState((s) => ({
          ...s,
          isRunning: false,
          output: outputRef.current.trimEnd(),
          error: errorRef.current.trimEnd(),
        }));
      } catch (err) {
        const errMsg = err instanceof Error ? err.message : String(err);
        setState((s) => ({
          ...s,
          isRunning: false,
          error: (errorRef.current ? errorRef.current + "\n" : "") + errMsg,
        }));
      }
    },
    [load]
  );

  const reset = useCallback(() => {
    setState((s) => ({ ...s, output: "", error: "" }));
  }, []);

  return { ...state, load, runCode, reset };
}
