import { Outlet, useParams, Navigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import type { Chapter } from "../types/content";

interface LayoutProps {
  chapters: Chapter[];
  theme: "light" | "dark";
  toggleTheme: () => void;
}

export default function Layout({ chapters, theme, toggleTheme }: LayoutProps) {
  const { chapterId, sectionId } = useParams<{
    chapterId: string;
    sectionId: string;
  }>();

  if (!chapterId || !sectionId) {
    const firstChapter = chapters[0];
    const firstSection = firstChapter?.sections[0];
    if (firstChapter && firstSection) {
      return <Navigate to={`/learn/${firstChapter.id}/${firstSection.id}`} replace />;
    }
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      <Sidebar chapters={chapters} theme={theme} toggleTheme={toggleTheme} />
      <main className="flex-1 overflow-auto bg-white dark:bg-gray-800 transition-colors">
        <Outlet />
      </main>
    </div>
  );
}
