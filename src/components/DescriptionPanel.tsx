import type { Section } from "../types/content";

interface DescriptionPanelProps {
  section: Section;
}

export default function DescriptionPanel({ section }: DescriptionPanelProps) {
  return (
    <div className="px-6 py-5 bg-white dark:bg-surface-800/90
                    border-b border-surface-200/80 dark:border-surface-700/50
                    transition-colors duration-200 ease-out">
      <h2 className="text-xl font-bold text-surface-900 dark:text-white mb-2 tracking-tight">
        {section.title}
      </h2>
      {section.description && (
        <p className="text-surface-500 dark:text-surface-400 mb-4 leading-relaxed">{section.description}</p>
      )}
      {section.goals.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold text-surface-400 dark:text-surface-500 mb-2.5 uppercase tracking-wider">
            学习目标
          </h3>
          <ul className="space-y-1.5">
            {section.goals.map((goal, i) => (
              <li key={i} className="text-sm text-surface-600 dark:text-surface-300 flex items-start gap-2.5">
                <span className="text-primary-500 mt-1 text-[8px]">●</span>
                <span className="leading-relaxed">{goal}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {!section.runnable && (
        <div className="mt-4 px-4 py-3 bg-amber-50 dark:bg-amber-900/15
                        border border-amber-200/80 dark:border-amber-800/40
                        rounded-xl">
          <span className="text-sm text-amber-700 dark:text-amber-400">
            ⚠ 此示例需要完整 Python 环境运行（涉及系统级操作），当前仅展示代码
          </span>
        </div>
      )}
      {section.tags.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-1.5">
          {section.tags.map((tag) => (
            <span
              key={tag}
              className="px-2.5 py-0.5 text-[11px] font-medium bg-surface-100 dark:bg-surface-700/50
                         text-surface-500 dark:text-surface-400 rounded-md
                         border border-surface-200/60 dark:border-surface-600/30"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
