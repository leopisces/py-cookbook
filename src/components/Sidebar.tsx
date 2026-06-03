import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";
import type { Chapter } from "../types/content";

interface SidebarProps {
  chapters: Chapter[];
  theme: "light" | "dark";
  toggleTheme: () => void;
}

export default function Sidebar({ chapters, theme, toggleTheme }: SidebarProps) {
  const { chapterId, sectionId } = useParams<{
    chapterId: string;
    sectionId: string;
  }>();
  const [expandedChapters, setExpandedChapters] = useState<Set<string>>(
    () => new Set(chapterId ? [chapterId] : [])
  );
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const toggleChapter = (id: string) => {
    setExpandedChapters((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2.5 bg-surface-800 dark:bg-surface-700
                   text-white rounded-xl shadow-lg active:scale-95
                   transition-all duration-150 ease-out"
      >
        {sidebarOpen ? "✕" : "☰"}
      </button>

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-40 w-72
          bg-surface-900 dark:bg-surface-950 text-surface-100
          border-r border-surface-800/60 dark:border-surface-800
          transform transition-transform duration-200 ease-out
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
          overflow-y-auto
        `}
      >
        {/* Header */}
        <div className="sticky top-0 z-10 glass-strong p-5 border-b border-surface-700/50 dark:border-surface-800/50">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2.5 group">
              <span className="text-2xl group-hover:scale-110 transition-transform duration-200 ease-out">🐍</span>
              <div>
                <span className="text-base font-bold text-white tracking-tight">Python Cookbook</span>
              </div>
            </Link>
            <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
          </div>
          <p className="text-[11px] text-surface-400 dark:text-surface-500 mt-1.5 tracking-wide uppercase">
            交互式 Python 学习平台
          </p>
        </div>

        {/* Navigation */}
        <nav className="p-3">
          {chapters.map((chapter) => {
            const isExpanded = expandedChapters.has(chapter.id);
            const isActiveChapter = chapter.id === chapterId;

            return (
              <div key={chapter.id} className="mb-0.5">
                <button
                  onClick={() => toggleChapter(chapter.id)}
                  className={`
                    w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm
                    transition-all duration-150 ease-out
                    ${isActiveChapter
                      ? "bg-primary-600/15 text-primary-300"
                      : "text-surface-300 hover:bg-surface-800/80 dark:hover:bg-surface-800 hover:text-white"
                    }
                  `}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <span className={`text-[10px] font-mono tracking-wider ${
                      isActiveChapter ? "text-primary-400" : "text-surface-500"
                    }`}>
                      {chapter.order.toString().padStart(2, "0")}
                    </span>
                    <span className="truncate font-medium">{chapter.title}</span>
                  </div>
                  <svg
                    className={`w-3.5 h-3.5 transition-transform duration-200 ease-out flex-shrink-0 ${
                      isExpanded ? "rotate-90" : ""
                    } ${isActiveChapter ? "text-primary-400" : "text-surface-500"}`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </button>

                {isExpanded && (
                  <div className="ml-4 mt-0.5 space-y-px">
                    {chapter.sections.map((section) => {
                      const isActive =
                        chapter.id === chapterId && section.id === sectionId;

                      return (
                        <Link
                          key={section.id}
                          to={`/learn/${chapter.id}/${section.id}`}
                          onClick={() => setSidebarOpen(false)}
                          className={`
                            block px-3 py-1.5 rounded-md text-[13px] transition-all duration-150 ease-out
                            ${isActive
                              ? "bg-primary-600 text-white font-semibold shadow-sm shadow-primary-600/25"
                              : "text-surface-400 hover:bg-surface-800/60 dark:hover:bg-surface-800 hover:text-surface-200"
                            }
                          `}
                        >
                          <div className="flex items-center gap-2">
                            {!section.runnable && (
                              <span className="text-amber-400 text-[11px]" title="需要完整 Python 环境">⚠</span>
                            )}
                            <span className="truncate">{section.title}</span>
                          </div>
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </aside>
    </>
  );
}
