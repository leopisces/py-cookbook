import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import type { Chapter } from "../types/content";

interface SidebarProps {
  chapters: Chapter[];
}

export default function Sidebar({ chapters }: SidebarProps) {
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
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-gray-800 text-white rounded-lg shadow-lg"
      >
        {sidebarOpen ? "✕" : "☰"}
      </button>

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-40 w-72 bg-gray-900 text-gray-100
          transform transition-transform duration-200 ease-in-out
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
          overflow-y-auto
        `}
      >
        <div className="sticky top-0 bg-gray-900 p-4 border-b border-gray-700">
          <Link to="/" className="flex items-center gap-2 hover:opacity-80">
            <span className="text-2xl">🐍</span>
            <span className="text-lg font-bold text-white">Python Cookbook</span>
          </Link>
          <p className="text-xs text-gray-400 mt-1">交互式 Python 学习平台</p>
        </div>

        <nav className="p-2">
          {chapters.map((chapter) => {
            const isExpanded = expandedChapters.has(chapter.id);
            const isActiveChapter = chapter.id === chapterId;

            return (
              <div key={chapter.id} className="mb-1">
                <button
                  onClick={() => toggleChapter(chapter.id)}
                  className={`
                    w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm
                    transition-colors duration-150
                    ${isActiveChapter
                      ? "bg-blue-600/20 text-blue-300"
                      : "text-gray-300 hover:bg-gray-800 hover:text-white"
                    }
                  `}
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="text-xs font-mono opacity-50">
                      {chapter.order.toString().padStart(2, "0")}
                    </span>
                    <span className="truncate">{chapter.title}</span>
                  </div>
                  <svg
                    className={`w-4 h-4 transition-transform duration-150 flex-shrink-0 ${
                      isExpanded ? "rotate-90" : ""
                    }`}
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
                  <div className="ml-4 mt-1 space-y-0.5">
                    {chapter.sections.map((section) => {
                      const isActive =
                        chapter.id === chapterId && section.id === sectionId;

                      return (
                        <Link
                          key={section.id}
                          to={`/learn/${chapter.id}/${section.id}`}
                          onClick={() => setSidebarOpen(false)}
                          className={`
                            block px-3 py-1.5 rounded text-sm transition-colors duration-150
                            ${isActive
                              ? "bg-blue-600 text-white font-medium"
                              : "text-gray-400 hover:bg-gray-800 hover:text-gray-200"
                            }
                          `}
                        >
                          <div className="flex items-center gap-2">
                            {!section.runnable && (
                              <span className="text-amber-400 text-xs" title="需要完整 Python 环境">⚠</span>
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
