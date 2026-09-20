export interface UploadResponse {
  document_id: string;
  filename: string;
  file_type: string;
  page_count: number;
  status: string;
}

export interface LearningRequest {
  learner_id: number;
  topic: string;
  use_previous_material: boolean;
}

export interface RetrievedMaterial {
  document_id: string;
  page_number: number;
  text: string;
}

export interface ConceptKnowledge {
  concept: string;
  known: boolean;
}

export interface LearningGap {
  concept: string;
  importance: number;
  reason: string;
  known: boolean;
  evidence: string | null;
}

export interface TeachingSection {
  title: string;
  content: string;
}

export interface TeachingSource {
  document_id: string | null;
  page_number: number | null;
}

export interface TeachingLesson {
  topic: string;
  introduction: string;
  sections: TeachingSection[];
  summary: string;
  sources: TeachingSource[];
}

export interface LearningResponse {
  learner_id: number;
  topic: string;
  requirements: string[];
  gaps: LearningGap[];
  learning_plan: string[];
  retrieved_material: RetrievedMaterial[];
  lesson: TeachingLesson;
}

export interface HistoryEntry {
  id: number;
  activity_type: string;
  topic: string | null;
  document_id: string | null;
  concepts: string[];
  created_at: string;
}

export interface HistoryResponse {
  learner_id: number;
  history: HistoryEntry[];
}