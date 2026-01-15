"""
주주명부 전용 필드 추출 서비스

목표:
- 주주명
- 주식비율

입력:
- PDF 파일 경로

출력 예:
{
    "shareholders": [
        {"name": "홍길동", "share_ratio": "30.5"},
        {"name": "김철수", "share_ratio": "25.0"},
        ...
    ]
}
"""

import re
from typing import List, Dict, Optional
import pdfplumber


class ShareholderExtractor:
    """주주명부 추출 클래스"""

    @staticmethod
    def _normalize_share_ratio(ratio_str: str) -> Optional[str]:
        """
        주식비율 문자열을 정규화 (예: '30.50%', '30.5', '30%' -> '30.50')
        소수점 2째자리까지 정확하게 추출
        """
        if not ratio_str:
            return None

        # 공백 제거
        s = ratio_str.strip()

        # % 제거
        s = re.sub(r'%', '', s)

        # 숫자와 소수점 추출 (소수점 포함)
        # 패턴: 정수부.소수부 또는 정수부만
        match = re.search(r'(\d+\.?\d*)', s)
        if match:
            try:
                ratio = float(match.group(1))
                # 소수점 2째자리까지 정확하게 표시
                return f"{ratio:.2f}"
            except ValueError:
                return None

        return None

    @staticmethod
    def _find_column_indices(headers: List[str]) -> Dict[str, int]:
        """
        테이블 헤더에서 '주주명'과 '주식비율' 열 인덱스를 찾음.
        '주식수'는 제외하고 '주식비율'만 정확히 찾음.
        """
        name_idx = None
        ratio_idx = None

        # 주주명 키워드 (더 정확한 매칭)
        name_keywords = ['주주명', '주주성명', '성명', '이름']
        
        # 주식비율 키워드 (주식수는 제외)
        ratio_keywords = ['주식비율', '비율', '지분율', '지분비율', '비율(%)', '지분(%)']
        # 주식수는 명시적으로 제외
        exclude_keywords = ['주식수', '주식 수', '보유주식수', '보유주식']

        for i, header in enumerate(headers):
            if header:
                header_clean = header.strip().replace(' ', '').replace('(', '').replace(')', '')
                
                # 주주명 열 찾기
                if name_idx is None:
                    for keyword in name_keywords:
                        if keyword in header_clean:
                            name_idx = i
                            break

                # 주식비율 열 찾기 (주식수는 제외)
                if ratio_idx is None:
                    # 먼저 제외 키워드 체크
                    is_excluded = False
                    for exclude_kw in exclude_keywords:
                        if exclude_kw in header_clean:
                            is_excluded = True
                            break
                    
                    if not is_excluded:
                        for keyword in ratio_keywords:
                            if keyword in header_clean:
                                ratio_idx = i
                                break

        return {"name": name_idx, "ratio": ratio_idx}

    @staticmethod
    def extract_from_pdf(file_path: str) -> Dict[str, List[Dict[str, str]]]:
        """
        PDF 파일에서 주주명부 표를 추출하여 주주명과 주식비율 리스트를 반환.
        """
        shareholders: List[Dict[str, str]] = []
        import logging
        logger = logging.getLogger(__name__)

        try:
            with pdfplumber.open(file_path) as pdf:
                # 모든 페이지에서 표 추출 시도
                for page_idx, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    logger.info(f"페이지 {page_idx + 1}에서 {len(tables)}개의 표 발견")

                    for table_idx, table in enumerate(tables):
                        if not table or len(table) < 2:
                            continue

                        logger.info(f"표 {table_idx + 1} 분석 시작 (총 {len(table)}행)")
                        
                        # 표 전체 구조 로깅 (디버깅용)
                        logger.info(f"표 구조 (처음 5행):")
                        for i, row in enumerate(table[:5]):
                            logger.info(f"  행 {i}: {row}")

                        # 헤더 행 찾기 (첫 번째부터 최대 3번째 행까지 확인)
                        header_row_idx = None
                        name_idx = None
                        ratio_idx = None

                        for row_idx in range(min(3, len(table))):
                            row = table[row_idx]
                            if not row:
                                continue
                            
                            # None 값을 빈 문자열로 변환
                            header_row = [str(cell).strip() if cell is not None else "" for cell in row]
                            
                            logger.info(f"  헤더 후보 행 {row_idx}: {header_row}")
                            
                            indices = ShareholderExtractor._find_column_indices(header_row)
                            if indices["name"] is not None and indices["ratio"] is not None:
                                name_idx = indices["name"]
                                ratio_idx = indices["ratio"]
                                header_row_idx = row_idx
                                logger.info(f"  ✓ 헤더 발견! 행 {row_idx}, 주주명 열: {name_idx}, 주식비율 열: {ratio_idx}")
                                break

                        # 헤더 행을 찾지 못했으면 다음 표로
                        if name_idx is None or ratio_idx is None or header_row_idx is None:
                            logger.warning(f"  ✗ 헤더를 찾지 못함 (주주명: {name_idx}, 주식비율: {ratio_idx})")
                            continue

                        # 헤더 바로 다음 행부터 데이터 추출 (첫 번째 데이터 행 포함)
                        data_start_idx = header_row_idx + 1
                        logger.info(f"  데이터 추출 시작 인덱스: {data_start_idx}")

                        for row_idx in range(data_start_idx, len(table)):
                            row = table[row_idx]
                            
                            if not row:
                                continue

                            # 열 인덱스 범위 체크
                            if name_idx >= len(row) or ratio_idx >= len(row):
                                logger.warning(f"  행 {row_idx}: 열 인덱스 범위 초과 (행 길이: {len(row)})")
                                continue

                            name_cell = row[name_idx]
                            ratio_cell = row[ratio_idx]

                            # None 값 처리
                            name = str(name_cell).strip() if name_cell is not None else ""
                            ratio = str(ratio_cell).strip() if ratio_cell is not None else ""

                            logger.info(f"  행 {row_idx}: 주주명='{name}', 주식비율='{ratio}'")

                            # 빈 행은 스킵
                            if not name and not ratio:
                                logger.info(f"  행 {row_idx}: 빈 행 스킵")
                                continue

                            # 주주명 유효성 검사 (숫자만 있거나 너무 짧으면 스킵)
                            if len(name) < 1:
                                logger.info(f"  행 {row_idx}: 주주명이 너무 짧음")
                                continue
                            
                            # 숫자만 있는 경우는 스킵 (헤더나 구분선일 수 있음)
                            if name.isdigit() or (name.replace('.', '').replace(',', '').isdigit()):
                                logger.info(f"  행 {row_idx}: 주주명이 숫자만 있음, 스킵")
                                continue

                            # 주식비율 정규화 (정확한 숫자 추출)
                            normalized_ratio = ShareholderExtractor._normalize_share_ratio(ratio)
                            if not normalized_ratio:
                                # 비율이 없으면 "-"로 표시
                                normalized_ratio = "-"
                                logger.warning(f"  행 {row_idx}: 주식비율 추출 실패, 원본: '{ratio}'")
                            else:
                                logger.info(f"  행 {row_idx}: 주식비율 정규화 완료: '{ratio}' -> '{normalized_ratio}'")

                            shareholders.append({
                                "name": name,
                                "share_ratio": normalized_ratio
                            })

                        logger.info(f"  총 {len(shareholders)}명의 주주 추출 완료")

                        # 한 페이지에서 한 표만 처리 (첫 번째로 찾은 표)
                        if shareholders:
                            break

                    # 한 페이지에서 표를 찾았으면 다음 페이지는 스킵
                    if shareholders:
                        break

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"주주명부 PDF 추출 실패: {e}", exc_info=True)
            raise Exception(f"주주명부 추출 실패: {str(e)}")

        return {"shareholders": shareholders}

    @staticmethod
    def extract_from_text(text: str) -> Dict[str, List[Dict[str, str]]]:
        """
        텍스트에서 주주명과 주식비율을 추출 (OCR 결과 등에 대응).
        표 형식이 아닌 경우 줄 단위로 파싱 시도.
        """
        shareholders: List[Dict[str, str]] = []
        lines = text.splitlines()

        # 표 헤더 찾기
        header_line_idx = None
        for i, line in enumerate(lines):
            if "주주명" in line and ("주식비율" in line or "비율" in line):
                header_line_idx = i
                break

        if header_line_idx is None:
            return {"shareholders": []}

        # 헤더 다음 줄부터 데이터 파싱
        for i in range(header_line_idx + 1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            # 탭이나 공백으로 구분된 열 찾기
            parts = re.split(r'\s{2,}|\t', line)
            
            if len(parts) < 2:
                continue

            # 첫 번째와 두 번째 열을 주주명과 비율로 추정
            # (더 정확한 파싱을 위해서는 실제 OCR 결과를 확인해야 함)
            name = parts[0].strip()
            ratio = parts[1].strip() if len(parts) > 1 else ""

            if len(name) < 1:
                continue

            # 주식비율 정규화 (정확한 숫자 추출, 소수점 2째자리까지)
            normalized_ratio = ShareholderExtractor._normalize_share_ratio(ratio)
            if not normalized_ratio:
                normalized_ratio = "-"

            shareholders.append({
                "name": name,
                "share_ratio": normalized_ratio
            })

        return {"shareholders": shareholders}

    @staticmethod
    def extract_from_text_fallback(text: str) -> Dict[str, List[Dict[str, str]]]:
        """
        텍스트에서 주식비율 패턴을 찾는 fallback 추출 방법.
        '주주명' 열을 찾아서 그 열의 데이터를 가져오고, 주식비율 패턴을 찾아서 매칭.
        """
        shareholders: List[Dict[str, str]] = []
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info("Fallback 추출 방법 시도: 주주명 열 찾기 + 주식비율 패턴 검색")
        
        # 주식비율 패턴: 소수점 둘째자리까지 있고 %가 붙어있는 값
        # 예: "30.50%", "25.75%", "(30.50%)", " 30.50% "
        ratio_pattern = re.compile(r'\(?\s*(\d+\.\d{1,2})\s*%\s*\)?')
        
        lines = text.splitlines()
        
        # 1단계: '주주명' 헤더 찾기
        header_line_idx = None
        name_column_idx = None
        
        for i, line in enumerate(lines):
            line_clean = line.strip().replace(' ', '')
            # '주주명' 키워드 찾기
            if '주주명' in line_clean:
                header_line_idx = i
                logger.info(f"'주주명' 헤더 발견: 행 {i}")
                
                # 헤더 행을 공백/탭으로 분리하여 열 인덱스 찾기
                header_parts = re.split(r'[\s\t]{2,}|\t', line.strip())
                for idx, part in enumerate(header_parts):
                    if '주주명' in part.replace(' ', ''):
                        name_column_idx = idx
                        logger.info(f"'주주명' 열 인덱스: {idx}")
                        break
                
                if name_column_idx is not None:
                    break
        
        if header_line_idx is None or name_column_idx is None:
            logger.warning("'주주명' 헤더를 찾을 수 없음")
            return {"shareholders": []}
        
        # 2단계: 헤더 다음 행부터 데이터 추출
        for line_idx in range(header_line_idx + 1, len(lines)):
            line = lines[line_idx].strip()
            if not line:
                continue
            
            # 주식비율 패턴이 있는지 확인
            ratio_matches = list(ratio_pattern.finditer(line))
            if not ratio_matches:
                continue
            
            # 주식비율 추출 (첫 번째 매칭만 사용)
            ratio_match = ratio_matches[0]
            ratio_str = ratio_match.group(1)
            
            try:
                ratio_float = float(ratio_str)
                normalized_ratio = f"{ratio_float:.2f}"
            except ValueError:
                continue
            
            # 주주명 열에서 데이터 추출
            # 줄을 공백/탭으로 분리
            line_parts = re.split(r'[\s\t]{2,}|\t', line)
            
            # 주주명 열 인덱스 범위 체크
            if name_column_idx < len(line_parts):
                shareholder_name = line_parts[name_column_idx].strip()
                
                # 띄어쓰기, 괄호, 특수문자가 있으면 그 앞까지만 추출
                # 예: "홍길동 (30.50%)" → "홍길동"
                # 예: "김철수 25.75%" → "김철수"
                if ' ' in shareholder_name:
                    shareholder_name = shareholder_name.split(' ')[0].strip()
                if '(' in shareholder_name:
                    shareholder_name = shareholder_name.split('(')[0].strip()
                if '（' in shareholder_name:  # 전각 괄호
                    shareholder_name = shareholder_name.split('（')[0].strip()
                
                # 주주명 정리 (특수문자 제거, 하지만 기본적인 한글/영문/숫자는 유지)
                shareholder_name = re.sub(r'[^\w가-힣]', '', shareholder_name).strip()
                
                # 빈 주주명이거나 숫자만 있으면 '주주명 인식 불가'로 설정
                if not shareholder_name or len(shareholder_name) < 1:
                    shareholder_name = "주주명 인식 불가"
                elif shareholder_name.replace('.', '').replace(',', '').isdigit():
                    shareholder_name = "주주명 인식 불가"
                
                logger.info(f"Fallback 추출: 주주명='{shareholder_name}', 주식비율='{normalized_ratio}%'")
                
                shareholders.append({
                    "name": shareholder_name,
                    "share_ratio": normalized_ratio
                })
            else:
                # 주주명 열이 범위를 벗어났지만 주식비율은 있으면 '주주명 인식 불가'로 표시
                logger.warning(f"행 {line_idx}: 주주명 열 인덱스({name_column_idx})가 범위를 벗어남 (열 수: {len(line_parts)})")
                logger.info(f"Fallback 추출: 주주명='주주명 인식 불가', 주식비율='{normalized_ratio}%'")
                
                shareholders.append({
                    "name": "주주명 인식 불가",
                    "share_ratio": normalized_ratio
                })
        
        logger.info(f"Fallback 추출 완료: 총 {len(shareholders)}명의 주주 추출")
        return {"shareholders": shareholders}


def extract_shareholder_fields(file_path: str, file_ext: str, text: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    """
    파일 경로와 확장자로부터 주주명부 정보를 추출.
    
    우선순위:
    1. PDF인 경우: pdfplumber로 표 추출
    2. 텍스트가 제공된 경우: 텍스트 기반 추출
    3. 실패 시 빈 리스트 반환
    """
    extractor = ShareholderExtractor()

    # PDF인 경우 표 추출 시도
    if file_ext.lower() == '.pdf':
        try:
            result = extractor.extract_from_pdf(file_path)
            if result["shareholders"]:
                return result
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"PDF 표 추출 실패, 텍스트 기반 추출 시도: {e}")

    # 텍스트 기반 추출 (OCR 결과 등)
    if text:
        try:
            result = extractor.extract_from_text(text)
            # 결과가 있으면 반환
            if result["shareholders"]:
                return result
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"텍스트 기반 추출 실패: {e}")
    
    # 기존 추출 방법이 모두 실패했고 텍스트가 있는 경우, fallback 방법 시도
    if text:
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("기존 추출 방법 실패, fallback 방법 시도 (주식비율 패턴 검색)")
            result = ShareholderExtractor.extract_from_text_fallback(text)
            if result["shareholders"]:
                return result
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Fallback 추출 실패: {e}")

    return {"shareholders": []}


__all__ = ["extract_shareholder_fields", "ShareholderExtractor"]
