import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import LessonPage from "./pages/LessonPage";
import { useContent, getFirstSection } from "./hooks/useContent";

export default function App() {
  const { data, loading, error } = useContent();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500">加载内容...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="text-4xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">加载失败</h2>
          <p className="text-gray-500">{error || "无法加载内容数据"}</p>
        </div>
      </div>
    );
  }

  const firstSection = getFirstSection(data);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage data={data} />} />
        <Route path="/learn" element={<Layout chapters={data.chapters} />}>
          <Route index element={
            firstSection
              ? <Navigate to={`/learn/${firstSection.chapterId}/${firstSection.sectionId}`} replace />
              : <Navigate to="/" replace />
          } />
          <Route path=":chapterId/:sectionId" element={<LessonPage data={data} />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
