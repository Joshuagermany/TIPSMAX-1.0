export interface TipsCategoryScore {
  category: string;
  score: number; // 0-100
}

export interface Evaluations {
  technology: number; // 0-100
  business: number;   // 0-100
  team: number;       // 0-100
  tipsFit: number;    // 0-100
}

export interface AnalysisResult {
  companySummary: string;
  tipsCategories: TipsCategoryScore[];
  evaluations: Evaluations;
  overallScore: number; // 0-100
  recommendation: "추천" | "보류" | "비추천";
  strengths: string[];
  risks: string[];
  comments: string;
}

export interface UploadResponse {
  file_id: string;
  filename: string;
  file_size: number;
}
