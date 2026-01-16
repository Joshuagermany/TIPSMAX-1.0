"""
문서 파싱 서비스
PDF, DOCX, TXT 파일을 텍스트로 변환
"""

import os
from typing import Optional

import PyPDF2
import pdfplumber
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

# 윈도우 환경에서 Tesseract 실행 파일 경로를 명시적으로 지정
# (환경변수 PATH에 추가했더라도, 프로세스가 갱신된 PATH를 못 볼 수 있어서 예방 차원)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class DocumentParser:
    """문서 파싱 클래스"""

    @staticmethod
    def _ocr_pdf_with_tesseract(file_path: str, top_half_only: bool = False) -> str:
        """
        PyMuPDF로 PDF 페이지를 이미지로 렌더링한 뒤
        Tesseract OCR으로 텍스트 추출 (이미지 기반 PDF 대응).
        
        Args:
            top_half_only: True인 경우 상단 50%만 OCR 수행 (사업자등록증 등)
        """
        text_chunks: list[str] = []
        try:
            doc = fitz.open(file_path)
            for page_index in range(len(doc)):
                page = doc[page_index]
                # 해상도 조절 (dpi 비슷한 효과) - 2배 확대
                zoom = 2.0
                mat = fitz.Matrix(zoom, zoom)
                
                if top_half_only:
                    # 상단 50%만 추출
                    page_rect = page.rect
                    top_half_rect = fitz.Rect(
                        page_rect.x0,
                        page_rect.y0,
                        page_rect.x1,
                        page_rect.y0 + (page_rect.height * 0.5)
                    )
                    pix = page.get_pixmap(matrix=mat, clip=top_half_rect)
                    print(f"페이지 {page_index + 1}: 상단 50%만 OCR 수행")
                else:
                    pix = page.get_pixmap(matrix=mat)

                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # 한국어 + 영어 OCR
                ocr_text = pytesseract.image_to_string(img, lang="kor+eng")
                if ocr_text:
                    text_chunks.append(ocr_text)
        except Exception as e:
            # OCR 실패 시 조용히 무시하고 빈 문자열 반환
            print(f"OCR 파싱 실패: {e}")
            return ""

        full_text = "\n".join(text_chunks).strip()
        print(f"OCR로 추출한 텍스트 길이: {len(full_text)}")
        return full_text

    @staticmethod
    def parse_pdf(file_path: str, ocr_only: bool = False, top_half_only: bool = False) -> str:
        """
        PDF 파일 파싱
        
        Args:
            ocr_only: True인 경우 텍스트 기반 파싱을 건너뛰고 바로 OCR 사용
            top_half_only: True인 경우 상단 50%만 분석 (ocr_only와 함께 사용)
        """
        # OCR 전용 모드 (사업자등록증 등)
        if ocr_only:
            print("OCR 전용 모드로 파싱 시작...")
            ocr_text = DocumentParser._ocr_pdf_with_tesseract(file_path, top_half_only=top_half_only)
            if ocr_text:
                return ocr_text.strip()
            else:
                raise Exception("PDF 파싱 실패: OCR 실패")
        
        # 일반 모드: 텍스트 기반 파싱 먼저 시도
        text = ""
        try:
            # pdfplumber로 먼저 시도 (더 정확함)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber 파싱 실패: {e}")

        # pdfplumber 결과가 너무 짧으면 PyPDF2 시도
        if not text.strip() or len(text.strip()) < 10:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text() or ""
                        text += page_text + "\n"
            except Exception as e2:
                print(f"PyPDF2 파싱 실패: {e2}")

        # 여전히 텍스트가 없거나 너무 짧으면 OCR 시도
        if not text.strip() or len(text.strip()) < 10:
            print("텍스트 기반 파싱 결과가 부족하여 OCR 시도...")
            ocr_text = DocumentParser._ocr_pdf_with_tesseract(file_path, top_half_only=top_half_only)
            if ocr_text:
                return ocr_text.strip()
            else:
                raise Exception("PDF 파싱 실패: 텍스트 및 OCR 모두 실패")

        print(f"PDF 텍스트 길이: {len(text.strip())}")
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
    def parse(file_path: str, file_extension: str, ocr_only: bool = False, top_half_only: bool = False) -> str:
        """
        파일 확장자에 따라 적절한 파서 호출
        
        Args:
            file_path: 파일 경로
            file_extension: 파일 확장자
            ocr_only: True인 경우 텍스트 기반 파싱을 건너뛰고 바로 OCR 사용 (PDF만 지원)
            top_half_only: True인 경우 상단 50%만 분석 (PDF만 지원, ocr_only와 함께 사용)
        """
        ext = file_extension.lower().lstrip('.')

        if ext == 'pdf':
            return DocumentParser.parse_pdf(file_path, ocr_only=ocr_only, top_half_only=top_half_only)
        elif ext in ['docx', 'doc']:
            return DocumentParser.parse_docx(file_path)
        elif ext == 'txt':
            return DocumentParser.parse_txt(file_path)
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {ext}")
