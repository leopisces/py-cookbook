interface PyodideLoaderProps {
  isLoading: boolean;
  isLoaded: boolean;
  onLoad: () => void;
}

export default function PyodideLoader({ isLoading, isLoaded, onLoad }: PyodideLoaderProps) {
  if (isLoaded) return null;

  if (isLoading) {
    return (
      <div className="flex items-center gap-2">
        <div className="w-3.5 h-3.5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
        <span className="text-xs text-primary-600 dark:text-primary-400 font-medium">
          加载中...
        </span>
      </div>
    );
  }

  return (
    <button
      onClick={onLoad}
      className="px-3 py-1.5 text-xs font-medium
                 text-primary-600 dark:text-primary-400
                 hover:text-primary-700 dark:hover:text-primary-300
                 bg-primary-50 dark:bg-primary-900/30
                 hover:bg-primary-100 dark:hover:bg-primary-900/50
                 rounded-lg transition-all duration-150 ease-out
                 active:scale-95"
    >
      加载环境
    </button>
  );
}
