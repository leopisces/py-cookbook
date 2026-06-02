export interface Chapter {
  id: string;
  title: string;
  description: string;
  order: number;
  sections: Section[];
}

export interface Section {
  id: string;
  title: string;
  chapterId: string;
  description: string;
  goals: string[];
  code: string;
  runnable: boolean;
  output?: string;
  tags: string[];
}

export interface ContentData {
  chapters: Chapter[];
  generatedAt: string;
}
