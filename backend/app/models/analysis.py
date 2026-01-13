from pydantic import BaseModel
from typing import List, Literal


class TipsCategoryScore(BaseModel):
    category: str
    score: int  # 0-100


class Evaluations(BaseModel):
    technology: int  # 0-100
    business: int    # 0-100
    team: int        # 0-100
    tipsFit: int     # 0-100


class AnalysisResult(BaseModel):
    companySummary: str
    tipsCategories: List[TipsCategoryScore]
    evaluations: Evaluations
    overallScore: int  # 0-100
    recommendation: Literal["추천", "보류", "비추천"]
    strengths: List[str]  # TOP 3
    risks: List[str]      # TOP 3
    comments: str


class AnalysisRequest(BaseModel):
    file_id: str


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    file_size: int
