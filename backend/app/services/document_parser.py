"""
문서 파싱 서비스
PDF, DOCX, TXT 파일을 텍스트로 변환
"""

import os
from typing import Optional
import PyPDF2
import pdfplumber
from docx import Document


class DocumentParser:
    """문서 파싱 클래스"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """PDF 파일 파싱"""
        text = ""
        try:
            # pdfplumber로 먼저 시도 (더 정확함)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # PyPDF2로 폴백
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                raise Exception(f"PDF 파싱 실패: {str(e2)}")
        
        return text.strip()
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """DOCX 파일 파싱"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"DOCX 파싱 실패: {str(e)}")
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        """TXT 파일 파싱"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text.strip()
        except UnicodeDecodeError:
            # 다른 인코딩 시도
            try:
                with open(file_path, 'r', encoding='cp949') as file:
                    text = file.read()
                return text.strip()
            except Exception as e:
                raise Exception(f"TXT 파싱 실패: {str(e)}")
    
    @staticmethod
    def parse(file_path: str, file_extension: str) -> str:
        """파일 확장자에 따라 적절한 파서 호출"""
        ext = file_extension.lower().lstrip('.')
        
        if ext == 'pdf':
            return DocumentParser.parse_pdf(file_path)
        elif ext in ['docx', 'doc']:
            return DocumentParser.parse_docx(file_path)
        elif ext == 'txt':
            return DocumentParser.parse_txt(file_path)
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {ext}")
