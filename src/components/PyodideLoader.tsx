interface PyodideLoaderProps {
  isLoading: boolean;
  isLoaded: boolean;
  onLoad: () => void;
}

export default function PyodideLoader({ isLoading, isLoaded, onLoad }: PyodideLoaderProps) {
  if (isLoaded) return null;

  return (
    <div className="flex items-center gap-3 px-5 py-2.5
                    bg-primary-50 dark:bg-primary-900/15
                    border-b border-primary-200/60 dark:border-primary-800/30
                    transition-colors duration-200 ease-out">
      {isLoading ? (
        <>
          <div className="w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm text-primary-700 dark:text-primary-300 font-medium">
            正在加载 Python 运行环境（首次约 5-10 秒）...
          </span>
        </>
      ) : (
        <button
          onClick={onLoad}
          className="text-sm text-primary-600 dark:text-primary-400
                     hover:text-primary-800 dark:hover:text-primary-200
                     underline decoration-primary-300 dark:decoration-primary-600
                     underline-offset-2 transition-colors duration-150 ease-out
                     font-medium"
        >
          点击加载 Python 运行环境
        </button>
      )}
    </div>
  );
}
