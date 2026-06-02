import { useParams, Navigate } from "react-router-dom";
import CodeRunner from "../components/CodeRunner";
import type { ContentData } from "../types/content";
import { findSection } from "../hooks/useContent";

interface LessonPageProps {
  data: ContentData;
}

export default function LessonPage({ data }: LessonPageProps) {
  const { chapterId, sectionId } = useParams<{
    chapterId: string;
    sectionId: string;
  }>();

  if (!chapterId || !sectionId) {
    return <Navigate to="/" replace />;
  }

  const result = findSection(data, chapterId, sectionId);

  if (!result) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="text-4xl mb-4">😕</div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">页面未找到</h2>
          <p className="text-gray-500">
            章节 {chapterId}/{sectionId} 不存在
          </p>
        </div>
      </div>
    );
  }

  return <CodeRunner section={result.section} />;
}
