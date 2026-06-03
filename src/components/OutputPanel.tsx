interface OutputPanelProps {
  output: string;
  error: string;
  isRunning: boolean;
}

export default function OutputPanel({ output, error, isRunning }: OutputPanelProps) {
  return (
    <div className="h-full flex flex-col bg-surface-900 dark:bg-surface-950 transition-colors duration-200 ease-out">
      <div className="flex items-center justify-between px-4 py-2.5
                      bg-surface-800/80 dark:bg-surface-900/80
                      border-b border-surface-700/40 dark:border-surface-800/40">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500/60"></span>
            <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/60"></span>
            <span className="w-2.5 h-2.5 rounded-full bg-green-500/60"></span>
          </div>
          <span className="text-xs font-medium text-surface-300 dark:text-surface-400 tracking-wide">输出</span>
        </div>
        {isRunning && (
          <span className="text-[11px] text-primary-400 animate-pulse font-medium">运行中...</span>
        )}
      </div>
      <div className="flex-1 overflow-auto p-4 font-mono text-sm leading-relaxed">
        {!output && !error && !isRunning && (
          <div className="flex flex-col items-center justify-center h-full text-surface-500 dark:text-surface-600">
            <svg className="w-8 h-8 mb-2 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className="text-xs italic">点击「运行」按钮执行代码</span>
          </div>
        )}
        {output && (
          <pre className="text-primary-300 dark:text-primary-300 whitespace-pre-wrap mb-2">{output}</pre>
        )}
        {error && (
          <pre className="text-red-400 dark:text-red-300 whitespace-pre-wrap">{error}</pre>
        )}
      </div>
    </div>
  );
}
