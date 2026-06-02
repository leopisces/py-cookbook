import type { Section } from "../types/content";

interface DescriptionPanelProps {
  section: Section;
}

export default function DescriptionPanel({ section }: DescriptionPanelProps) {
  return (
    <div className="p-6 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 transition-colors">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{section.title}</h2>
      {section.description && (
        <p className="text-gray-600 dark:text-gray-300 mb-4">{section.description}</p>
      )}
      {section.goals.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">学习目标</h3>
          <ul className="space-y-1">
            {section.goals.map((goal, i) => (
              <li key={i} className="text-sm text-gray-600 dark:text-gray-300 flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">•</span>
                {goal}
              </li>
            ))}
          </ul>
        </div>
      )}
      {!section.runnable && (
        <div className="mt-4 px-3 py-2 bg-amber-50 dark:bg-amber-900/20 border border-amber-200
                        dark:border-amber-800 rounded-lg">
          <span className="text-sm text-amber-700 dark:text-amber-400">
            ⚠ 此示例需要完整 Python 环境运行（涉及系统级操作），当前仅展示代码
          </span>
        </div>
      )}
      {section.tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {section.tags.map((tag) => (
            <span
              key={tag}
              className="px-2 py-0.5 text-xs bg-gray-100 dark:bg-gray-700 text-gray-500
                         dark:text-gray-400 rounded"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
