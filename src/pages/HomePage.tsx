import { Link } from "react-router-dom";
import ThemeToggle from "../components/ThemeToggle";
import type { ContentData } from "../types/content";

interface HomePageProps {
  data: ContentData;
  theme: "light" | "dark";
  toggleTheme: () => void;
}

export default function HomePage({ data, theme, toggleTheme }: HomePageProps) {
  const firstChapter = data.chapters[0];
  const firstSection = firstChapter?.sections[0];
  const totalSections = data.chapters.reduce((sum, ch) => sum + ch.sections.length, 0);
  const runnableSections = data.chapters.reduce(
    (sum, ch) => sum + ch.sections.filter((s) => s.runnable).length,
    0
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50
                    dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors">
      {/* Header with theme toggle */}
      <div className="absolute top-4 right-4">
        <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
      </div>

      {/* Hero */}
      <header className="max-w-4xl mx-auto px-6 pt-20 pb-12 text-center">
        <div className="text-6xl mb-6">🐍</div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Python Cookbook
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
          交互式 Python 学习平台 · {data.chapters.length} 个章节 · {totalSections} 个知识点 ·
          浏览器内直接运行代码
        </p>
        {firstChapter && firstSection && (
          <Link
            to={`/learn/${firstChapter.id}/${firstSection.id}`}
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white
                       rounded-lg hover:bg-blue-500 transition-colors text-lg font-medium
                       shadow-lg shadow-blue-500/25"
          >
            开始学习 →
          </Link>
        )}
        <div className="mt-6 flex items-center justify-center gap-6 text-sm text-gray-500 dark:text-gray-400">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            {runnableSections} 个可运行示例
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 bg-amber-500 rounded-full"></span>
            {totalSections - runnableSections} 个只读示例
          </span>
        </div>
      </header>

      {/* 章节列表 */}
      <main className="max-w-4xl mx-auto px-6 pb-20">
        <div className="grid gap-4">
          {data.chapters.map((chapter) => (
            <div
              key={chapter.id}
              className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200
                         dark:border-gray-700 p-6 hover:shadow-md dark:hover:shadow-lg
                         dark:hover:shadow-gray-900/50 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <span className="text-xs font-mono text-gray-400 dark:text-gray-500 mr-2">
                    {chapter.order.toString().padStart(2, "0")}
                  </span>
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white inline">
                    {chapter.title}
                  </h2>
                </div>
                <span className="text-xs text-gray-400 dark:text-gray-500 bg-gray-50
                                 dark:bg-gray-700 px-2 py-1 rounded">
                  {chapter.sections.filter((s) => s.runnable).length}/{chapter.sections.length} 可运行
                </span>
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{chapter.description}</p>
              <div className="flex flex-wrap gap-2">
                {chapter.sections.map((section) => (
                  <Link
                    key={section.id}
                    to={`/learn/${chapter.id}/${section.id}`}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm
                               bg-gray-50 dark:bg-gray-700 hover:bg-blue-50 dark:hover:bg-blue-900/30
                               text-gray-700 dark:text-gray-300 hover:text-blue-700 dark:hover:text-blue-300
                               rounded-lg transition-colors border border-transparent
                               hover:border-blue-200 dark:hover:border-blue-700"
                  >
                    {!section.runnable && (
                      <span className="text-amber-400 text-xs">⚠</span>
                    )}
                    {section.title}
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
