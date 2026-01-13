"""
LLM 분석 서비스
OpenAI 또는 Anthropic API를 사용한 문서 분석
"""

import os
import json
from typing import Optional
from openai import OpenAI
from anthropic import Anthropic
from app.services.prompt_templates import get_analysis_prompt
from app.models.analysis import AnalysisResult, Evaluations, TipsCategoryScore


class LLMAnalyzer:
    """LLM 기반 문서 분석 클래스"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.anthropic_client = Anthropic(api_key=api_key)
    
    def analyze(self, document_text: str) -> AnalysisResult:
        """문서 분석 실행"""
        prompt = get_analysis_prompt(document_text)
        
        if self.provider == "openai" and self.openai_client:
            result = self._analyze_openai(prompt)
        elif self.provider == "anthropic" and self.anthropic_client:
            result = self._analyze_anthropic(prompt)
        else:
            # Mock 데이터 (API 키가 없을 때)
            result = self._get_mock_result()
        
        return result
    
    def _analyze_openai(self, prompt: str) -> AnalysisResult:
        """OpenAI API 사용"""
        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 COMMAX VENTURUS의 VC 심사역입니다. 제공된 JSON 형식으로만 응답하세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            # Evaluations와 TipsCategoryScore 객체로 변환
            if "evaluations" in data and isinstance(data["evaluations"], dict):
                data["evaluations"] = Evaluations(**data["evaluations"])
            if "tipsCategories" in data and isinstance(data["tipsCategories"], list):
                data["tipsCategories"] = [TipsCategoryScore(**item) for item in data["tipsCategories"]]
            return AnalysisResult(**data)
        except Exception as e:
            print(f"OpenAI 분석 오류: {str(e)}")
            return self._get_mock_result()
    
    def _analyze_anthropic(self, prompt: str) -> AnalysisResult:
        """Anthropic Claude API 사용"""
        try:
            response = self.anthropic_client.messages.create(
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
                max_tokens=4000,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text
            # JSON 추출 (마크다운 코드 블록 제거)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            data = json.loads(content)
            # Evaluations와 TipsCategoryScore 객체로 변환
            if "evaluations" in data and isinstance(data["evaluations"], dict):
                data["evaluations"] = Evaluations(**data["evaluations"])
            if "tipsCategories" in data and isinstance(data["tipsCategories"], list):
                data["tipsCategories"] = [TipsCategoryScore(**item) for item in data["tipsCategories"]]
            return AnalysisResult(**data)
        except Exception as e:
            print(f"Anthropic 분석 오류: {str(e)}")
            return self._get_mock_result()
    
    def _get_mock_result(self) -> AnalysisResult:
        """Mock 결과 (API 키가 없거나 오류 시)"""
        return AnalysisResult(
            companySummary="문서 분석을 위해 LLM API 키를 설정해주세요. .env 파일에 OPENAI_API_KEY 또는 ANTHROPIC_API_KEY를 추가하세요.",
            tipsCategories=[
                TipsCategoryScore(category="AI·빅데이터", score=0),
                TipsCategoryScore(category="시스템반도체 / 팹리스", score=0),
            ],
            evaluations=Evaluations(
                technology=0,
                business=0,
                team=0,
                tipsFit=0
            ),
            overallScore=0,
            recommendation="보류",
            strengths=["API 키 설정 필요"],
            risks=["LLM 서비스 미연결"],
            comments="LLM API 키를 설정하면 실제 분석이 가능합니다."
        )
