interface OutputPanelProps {
  output: string;
  error: string;
  isRunning: boolean;
}

export default function OutputPanel({ output, error, isRunning }: OutputPanelProps) {
  return (
    <div className="h-full flex flex-col bg-gray-900">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
        <span className="text-sm font-medium text-gray-300">输出</span>
        {isRunning && (
          <span className="text-xs text-yellow-400 animate-pulse">运行中...</span>
        )}
      </div>
      <div className="flex-1 overflow-auto p-4 font-mono text-sm">
        {!output && !error && !isRunning && (
          <div className="text-gray-500 italic">点击「运行」按钮执行代码</div>
        )}
        {output && (
          <pre className="text-green-400 whitespace-pre-wrap mb-2">{output}</pre>
        )}
        {error && (
          <pre className="text-red-400 whitespace-pre-wrap">{error}</pre>
        )}
      </div>
    </div>
  );
}
