"""
재무제표 전용 필드 추출 서비스

목표:
- 각 페이지를 다음 4가지 중 하나로 분류:
  1. 표준재무제표증명
  2. 표준재무상태표
  3. 표준손익계산서
  4. 부속명세서

입력:
- PDF 파일 경로

출력 예:
{
    "pages": [
        {"page_number": 1, "type": "표준재무제표증명"},
        {"page_number": 2, "type": "표준재무상태표"},
        {"page_number": 3, "type": "표준손익계산서"},
        ...
    ]
}
"""

import re
from typing import List, Dict, Optional


class FinancialStatementExtractor:
    """재무제표 추출 클래스"""

    # 분류할 문서 타입 키워드
    DOCUMENT_TYPES = {
        "표준재무제표증명": ["표준재무제표증명", "재무제표증명", "재무제표 증명"],
        "표준재무상태표": ["표준재무상태표", "재무상태표", "재무 상태표"],
        "표준손익계산서": ["표준손익계산서", "손익계산서", "손익 계산서"],
        "부속명세서": ["부속명세서", "부속 명세서", "명세서"]
    }

    @staticmethod
    def _classify_page_text(text: str) -> Optional[str]:
        """
        페이지 텍스트에서 문서 타입을 분류.
        상단 부분에서 큰 글씨나 명확한 키워드를 찾음.
        """
        if not text:
            return None

        # 공백 제거하여 비교 (띄어쓰기 무시)
        text_no_spaces = text.replace(' ', '').replace('\n', '').replace('\t', '')
        
        # 각 문서 타입별로 키워드 검색
        for doc_type, keywords in FinancialStatementExtractor.DOCUMENT_TYPES.items():
            for keyword in keywords:
                # 원본 텍스트에서 검색
                if keyword in text:
                    return doc_type
                # 공백 제거한 텍스트에서도 검색 (띄어쓰기 무시)
                keyword_no_spaces = keyword.replace(' ', '')
                if keyword_no_spaces in text_no_spaces:
                    return doc_type
        
        return None

    @staticmethod
    def _extract_revenue(text: str) -> Optional[str]:
        """
        표준손익계산서 텍스트에서 매출액을 추출.
        '매출액' 키워드 근처의 금액을 찾음.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 60)
        logger.info("매출액 추출 함수 호출됨!")
        print("=" * 60)
        print("매출액 추출 함수 호출됨!")
        print(f"텍스트 길이: {len(text) if text else 0}")
        logger.info(f"텍스트 길이: {len(text) if text else 0}")
        
        if not text:
            logger.warning("텍스트가 비어있음")
            print("텍스트가 비어있음")
            return None
        
        # 텍스트의 일부를 로그로 출력 (처음 500자)
        logger.info(f"텍스트 앞 500자:\n{text[:500]}")
        print(f"텍스트 앞 500자:\n{text[:500]}")
        
        # 매출액 키워드 찾기
        revenue_keywords = ['매출액', '매출', '수익', '영업수익']
        
        lines = text.split('\n')
        logger.info(f"총 줄 수: {len(lines)}")
        print(f"총 줄 수: {len(lines)}")
        
        for line_idx, line in enumerate(lines):
            line_clean = line.strip()
            
            # 매출액 키워드가 있는 줄 찾기
            for keyword in revenue_keywords:
                if keyword in line_clean:
                    logger.info(f"매출액 키워드 발견: '{keyword}' (줄 {line_idx + 1})")
                    print(f"매출액 키워드 발견: '{keyword}' (줄 {line_idx + 1})")
                    
                    logger.info(f"키워드 '{keyword}'가 포함된 줄: {line_clean}")
                    print(f"키워드 '{keyword}'가 포함된 줄: {line_clean}")
                    
                    # 같은 줄에서 금액 찾기
                    # 패턴: 숫자, 쉼표, 점 포함 (예: 1,000,000원, 1,000,000, 1000000)
                    # 금액 패턴: 숫자와 쉼표, 점으로 구성된 큰 숫자
                    amount_patterns = [
                        r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*원',  # 1,000,000원
                        r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)',  # 1,000,000
                        r'(\d{4,})',  # 1000000 (4자리 이상)
                    ]
                    
                    logger.info(f"금액 패턴 검색 시작 (줄: {line_clean})")
                    print(f"금액 패턴 검색 시작 (줄: {line_clean})")
                    
                    for pattern_idx, pattern in enumerate(amount_patterns):
                        matches = list(re.finditer(pattern, line_clean))
                        logger.info(f"패턴 {pattern_idx + 1} 매칭 수: {len(matches)}")
                        print(f"패턴 {pattern_idx + 1} 매칭 수: {len(matches)}")
                        
                        for match in matches:
                            amount_str = match.group(1)
                            logger.info(f"매칭된 금액 후보: {amount_str}")
                            print(f"매칭된 금액 후보: {amount_str}")
                            
                            # 쉼표 제거하고 숫자로 변환 가능한지 확인
                            amount_clean = amount_str.replace(',', '').replace('.', '')
                            logger.info(f"정리된 금액: {amount_clean}, 길이: {len(amount_clean)}, 숫자 여부: {amount_clean.isdigit()}")
                            print(f"정리된 금액: {amount_clean}, 길이: {len(amount_clean)}, 숫자 여부: {amount_clean.isdigit()}")
                            
                            if amount_clean.isdigit() and len(amount_clean) >= 4:
                                logger.info(f"✅ 매출액 추출 성공: {amount_str}")
                                print(f"✅ 매출액 추출 성공: {amount_str}")
                                return amount_str
                            else:
                                logger.info(f"금액 후보 제외 (길이 부족 또는 숫자 아님): {amount_str}")
                                print(f"금액 후보 제외 (길이 부족 또는 숫자 아님): {amount_str}")
                    
                    # 같은 줄에서 못 찾으면 다음 줄 확인
                    if line_idx + 1 < len(lines):
                        next_line = lines[line_idx + 1].strip()
                        for pattern in amount_patterns:
                            matches = re.finditer(pattern, next_line)
                            for match in matches:
                                amount_str = match.group(1)
                                amount_clean = amount_str.replace(',', '').replace('.', '')
                                if amount_clean.isdigit() and len(amount_clean) >= 4:
                                    logger.info(f"매출액 추출 (다음 줄): {amount_str}")
                                    print(f"매출액 추출 (다음 줄): {amount_str}")
                                    return amount_str
                    
                    break
        
        logger.warning("매출액을 찾을 수 없음")
        print("매출액을 찾을 수 없음")
        return None

    @staticmethod
    def extract_from_pdf(file_path: str) -> Dict[str, List[Dict[str, str]]]:
        """
        PDF 파일에서 각 페이지를 분석하여 문서 타입을 분류.
        각 페이지의 상단 텍스트만 빠르게 확인 (처음 10줄 정도만).
        배경 이미지가 있어도 텍스트는 추출 가능.
        """
        pages: List[Dict[str, str]] = []
        import logging
        logger = logging.getLogger(__name__)

        try:
            # OCR만 사용 (pdfplumber, PyPDF2 제거)
            import fitz
            from PIL import Image
            import pytesseract
            
            # Tesseract 경로 설정
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            
            logger.info(f"PDF 파일 열기: {file_path}")
            print(f"PDF 파일 열기: {file_path}")
            doc = fitz.open(file_path)
            total_pages = len(doc)
            logger.info(f"재무제표 PDF 총 페이지 수: {total_pages}")
            print(f"재무제표 PDF 총 페이지 수: {total_pages}")
            
            # 역순으로 분석 (마지막 페이지부터)
            # 표준손익계산서와 표준재무상태표를 찾으면 중단
            found_income_statement = False
            found_balance_sheet = False
            result_pages: List[Dict[str, str]] = []
            
            logger.info("역순으로 페이지 분석 시작 (마지막 페이지부터)")
            print("역순으로 페이지 분석 시작 (마지막 페이지부터)")
            
            for page_idx in range(len(doc) - 1, -1, -1):  # 역순
                try:
                    logger.info(f"=== 페이지 {page_idx + 1} 처리 시작 ===")
                    print(f"=== 페이지 {page_idx + 1} 처리 시작 ===")
                    
                    # OCR로 텍스트 추출
                    logger.info(f"페이지 {page_idx + 1}: 이미지 렌더링 중...")
                    print(f"페이지 {page_idx + 1}: 이미지 렌더링 중...")
                    page_obj = doc[page_idx]
                    zoom = 2.0
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page_obj.get_pixmap(matrix=mat)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    
                    logger.info(f"페이지 {page_idx + 1}: OCR 실행 중...")
                    print(f"페이지 {page_idx + 1}: OCR 실행 중...")
                    page_text = pytesseract.image_to_string(img, lang="kor+eng")
                    logger.info(f"페이지 {page_idx + 1}: OCR 텍스트 길이 = {len(page_text) if page_text else 0}")
                    print(f"페이지 {page_idx + 1}: OCR 텍스트 길이 = {len(page_text) if page_text else 0}")
                    
                    if not page_text or len(page_text.strip()) < 10:
                        logger.warning(f"페이지 {page_idx + 1}: OCR 텍스트 추출 실패")
                        pages.append({
                            "page_number": page_idx + 1,
                            "type": "분류 불가"
                        })
                        continue

                    # 상단 부분만 확인 (처음 10줄)
                    lines = page_text.split('\n')
                    top_lines = lines[:10]  # 처음 10줄만
                    top_text = '\n'.join(top_lines)
                    
                    # 디버깅: 추출된 상단 텍스트 로그 출력
                    page_num = page_idx + 1
                    logger.info(f"페이지 {page_num} 상단 텍스트 (처음 10줄):\n{top_text}")
                    logger.info(f"페이지 {page_num} 전체 텍스트 길이: {len(page_text)}")
                    
                    # 키워드 검색 (상단 텍스트)
                    doc_type = FinancialStatementExtractor._classify_page_text(top_text)
                    
                    # 상단에서 못 찾으면 전체 텍스트에서 검색
                    if not doc_type:
                        doc_type = FinancialStatementExtractor._classify_page_text(page_text[:500])
                    
                    if doc_type:
                        logger.info(f"페이지 {page_num}: '{doc_type}'로 분류됨")
                        print(f"페이지 {page_num}: '{doc_type}'로 분류됨")
                        
                        # 표준손익계산서 또는 표준재무상태표를 처음 발견한 경우
                        if doc_type == "표준손익계산서" and not found_income_statement:
                            found_income_statement = True
                            
                            # 표준손익계산서에서 매출액 추출
                            logger.info(f"✅ 표준손익계산서 발견! 페이지 {page_num}, 매출액 추출 시도...")
                            print(f"✅ 표준손익계산서 발견! 페이지 {page_num}, 매출액 추출 시도...")
                            print(f"페이지 {page_num} 전체 텍스트 길이: {len(page_text)}")
                            logger.info(f"페이지 {page_num} 전체 텍스트 길이: {len(page_text)}")
                            
                            revenue = FinancialStatementExtractor._extract_revenue(page_text)
                            
                            logger.info(f"매출액 추출 결과: {revenue}")
                            print(f"매출액 추출 결과: {revenue}")
                            
                            result_pages.append({
                                "page_number": page_num,
                                "type": doc_type,
                                "revenue": revenue  # 매출액 추가
                            })
                            logger.info(f"✅ 표준손익계산서 저장 완료 (매출액: {revenue})")
                            print(f"✅ 표준손익계산서 저장 완료 (매출액: {revenue})")
                        
                        elif doc_type == "표준재무상태표" and not found_balance_sheet:
                            found_balance_sheet = True
                            result_pages.append({
                                "page_number": page_num,
                                "type": doc_type
                            })
                            logger.info(f"✅ 표준재무상태표 발견! 페이지 {page_num}")
                            print(f"✅ 표준재무상태표 발견! 페이지 {page_num}")
                        
                        # 둘 다 찾았으면 분석 중단
                        if found_income_statement and found_balance_sheet:
                            logger.info("표준손익계산서와 표준재무상태표를 모두 찾았으므로 분석 중단")
                            print("표준손익계산서와 표준재무상태표를 모두 찾았으므로 분석 중단")
                            break
                    else:
                        logger.warning(f"페이지 {page_num}: 문서 타입을 찾을 수 없음 (확인한 상단 텍스트: {top_text[:200]})")
                    
                    logger.info(f"=== 페이지 {page_num} 처리 완료 ===")
                
                except Exception as e:
                    logger.error(f"페이지 {page_idx + 1} 처리 중 오류: {e}", exc_info=True)
            
            doc.close()
            
            # 결과를 페이지 번호 순으로 정렬
            result_pages.sort(key=lambda x: x["page_number"])
            pages = result_pages
            
            logger.info(f"최종 결과: {len(pages)}개 페이지 발견")
            print(f"최종 결과: {len(pages)}개 페이지 발견")

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"재무제표 PDF 추출 실패: {e}", exc_info=True)
            if 'doc' in locals():
                doc.close()
            raise Exception(f"재무제표 추출 실패: {str(e)}")

        # 매출액 추출 (표준손익계산서 페이지에서)
        revenue = None
        for page in pages:
            if page.get("type") == "표준손익계산서" and "revenue" in page:
                revenue = page.get("revenue")
                break
        
        return {
            "pages": pages,
            "revenue": revenue
        }


def extract_financial_statement_fields(file_path: str, file_ext: str, text: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    """
    파일 경로와 확장자로부터 재무제표 정보를 추출.
    
    우선순위:
    1. PDF인 경우: pdfplumber로 각 페이지 분석
    2. 실패 시 빈 리스트 반환
    """
    extractor = FinancialStatementExtractor()

    # PDF인 경우 페이지별 분석
    if file_ext.lower() == '.pdf':
        try:
            result = extractor.extract_from_pdf(file_path)
            return result
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"PDF 페이지 분석 실패: {e}")
            return {"pages": []}

    return {"pages": []}


__all__ = ["extract_financial_statement_fields", "FinancialStatementExtractor"]
