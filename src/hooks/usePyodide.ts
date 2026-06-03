import { useState, useCallback, useRef, useEffect } from "react";

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
    if (!(window as unknown as Record<string, unknown>).loadPyodide) {
      await new Promise<void>((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js";
        script.onload = () => resolve();
        script.onerror = () => reject(new Error("Failed to load Pyodide"));
        document.head.appendChild(script);
      });
    }

    const loadFn = (window as unknown as Record<string, unknown>).loadPyodide as (opts: Record<string, unknown>) => Promise<unknown>;
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
  const streamQueueRef = useRef("");
  const streamDoneRef = useRef(false);
  const streamTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Push queued output to state progressively
  const flushStream = useCallback(() => {
    const queue = streamQueueRef.current;
    if (!queue) {
      // Queue empty — check if execution is done
      if (streamDoneRef.current) {
        clearInterval(streamTimerRef.current!);
        streamTimerRef.current = null;
        setState((s) => ({
          ...s,
          isRunning: false,
          output: outputRef.current.trimEnd(),
          error: errorRef.current.trimEnd(),
        }));
      }
      return;
    }

    const newlineIdx = queue.indexOf("\n");
    let chunk: string;
    if (newlineIdx !== -1) {
      chunk = queue.slice(0, newlineIdx + 1);
      streamQueueRef.current = queue.slice(newlineIdx + 1);
    } else {
      const take = Math.min(queue.length, 8);
      chunk = queue.slice(0, take);
      streamQueueRef.current = queue.slice(take);
    }

    outputRef.current += chunk;
    setState((s) => ({ ...s, output: outputRef.current }));
  }, []);

  const startStream = useCallback(() => {
    if (streamTimerRef.current) return;
    streamDoneRef.current = false;
    streamTimerRef.current = setInterval(flushStream, 30);
  }, [flushStream]);

  const stopStream = useCallback(() => {
    // Don't flush — just mark done so the timer drains the queue naturally
    streamDoneRef.current = true;
  }, []);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (streamTimerRef.current) {
        clearInterval(streamTimerRef.current);
        streamTimerRef.current = null;
      }
    };
  }, []);

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

  // Auto-load on mount
  useEffect(() => {
    if (!pyodideInstance && !state.isLoading && !state.isLoaded) {
      load();
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const runCode = useCallback(
    async (code: string) => {
      if (!pyodideInstance) {
        await load();
      }
      if (!pyodideInstance) {
        return;
      }

      // Reset
      outputRef.current = "";
      errorRef.current = "";
      streamQueueRef.current = "";
      stopStream();
      setState((s) => ({ ...s, isRunning: true, output: "", error: "" }));

      try {
        const pyodide = pyodideInstance as {
          setStdout: (opts: { batched: (msg: string) => void }) => void;
          setStderr: (opts: { batched: (msg: string) => void }) => void;
          runPythonAsync: (code: string) => Promise<unknown>;
          globals: { get: (name: string) => unknown };
        };

        // Queue output for streaming instead of pushing directly
        pyodide.setStdout({
          batched: (msg: string) => {
            streamQueueRef.current += msg + "\n";
          },
        });
        pyodide.setStderr({
          batched: (msg: string) => {
            errorRef.current += msg + "\n";
            setState((s) => ({ ...s, error: errorRef.current }));
          },
        });

        startStream();

        await pyodide.runPythonAsync(code);

        // Execution done — mark done, let timer drain queue naturally
        stopStream();
      } catch (err) {
        stopStream();
        // Force cleanup on error
        if (streamTimerRef.current) {
          clearInterval(streamTimerRef.current);
          streamTimerRef.current = null;
        }
        const errMsg = err instanceof Error ? err.message : String(err);
        outputRef.current = streamQueueRef.current + outputRef.current;
        streamQueueRef.current = "";
        setState((s) => ({
          ...s,
          isRunning: false,
          output: outputRef.current.trimEnd(),
          error: (errorRef.current ? errorRef.current + "\n" : "") + errMsg,
        }));
      }
    },
    [load, startStream, stopStream]
  );

  const reset = useCallback(() => {
    if (streamTimerRef.current) {
      clearInterval(streamTimerRef.current);
      streamTimerRef.current = null;
    }
    streamQueueRef.current = "";
    streamDoneRef.current = false;
    outputRef.current = "";
    errorRef.current = "";
    setState((s) => ({ ...s, output: "", error: "" }));
  }, []);

  return { ...state, load, runCode, reset };
}
