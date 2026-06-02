import { Outlet, useParams, Navigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import type { Chapter } from "../types/content";

interface LayoutProps {
  chapters: Chapter[];
}

export default function Layout({ chapters }: LayoutProps) {
  const { chapterId, sectionId } = useParams<{
    chapterId: string;
    sectionId: string;
  }>();

  // 如果没有指定章节，重定向到第一个
  if (!chapterId || !sectionId) {
    const firstChapter = chapters[0];
    const firstSection = firstChapter?.sections[0];
    if (firstChapter && firstSection) {
      return <Navigate to={`/learn/${firstChapter.id}/${firstSection.id}`} replace />;
    }
    return <Navigate to="/" replace />;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar chapters={chapters} />
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
