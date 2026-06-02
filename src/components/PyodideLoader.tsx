interface PyodideLoaderProps {
  isLoading: boolean;
  isLoaded: boolean;
  onLoad: () => void;
}

export default function PyodideLoader({ isLoading, isLoaded, onLoad }: PyodideLoaderProps) {
  if (isLoaded) return null;

  return (
    <div className="flex items-center gap-3 px-4 py-2 bg-blue-50 border-b border-blue-200">
      {isLoading ? (
        <>
          <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm text-blue-700">
            正在加载 Python 运行环境（首次约 5-10 秒）...
          </span>
        </>
      ) : (
        <button
          onClick={onLoad}
          className="text-sm text-blue-600 hover:text-blue-800 underline"
        >
          点击加载 Python 运行环境
        </button>
      )}
    </div>
  );
}
