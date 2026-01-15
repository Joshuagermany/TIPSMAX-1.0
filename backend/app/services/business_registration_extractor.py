"""
사업자등록증 전용 필드 추출 서비스

목표:
- 개업연월일
- 본점소재지

입력:
- PDF 등을 텍스트로 변환한 전체 문자열

출력 예:
{
    "opening_date_raw": "2020년 05월 01일",
    "opening_date_normalized": "2020-05-01",
    "head_office_address": "서울특별시 ○○구 ○○로 123, 4층 (○○동)",
}
"""

import re
from typing import Optional, Dict


def _normalize_korean_date(date_str: str) -> Optional[str]:
    """
    '2020년 5월 1일', '2020-05-01', '2020.05.01' 같은 문자열을 'YYYY-MM-DD' 로 정규화.
    실패 시 None 반환.
    """
    if not date_str:
        return None

    s = date_str.strip()

    # 한글 표기: 2020년 5월 1일
    m = re.search(r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일", s)
    if not m:
        # 구분자 표기: 2020-05-01, 2020.05.01, 2020/05/01
        m = re.search(r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})", s)
    if not m:
        return None

    year, month, day = m.groups()
    try:
        y = int(year)
        m_ = int(month)
        d_ = int(day)
        return f"{y:04d}-{m_:02d}-{d_:02d}"
    except ValueError:
        return None


def extract_business_registration_fields(text: str) -> Dict[str, Optional[str]]:
    """
    사업자등록증 텍스트에서 개업연월일과 본점소재지를 추출.

    규칙:
    - '개업연월일' 이라는 키워드가 있는 줄에서 날짜 부분을 추출
    - '본점소재지' 또는 '본점 소재지' 키워드가 있는 줄에서 주소 부분을 추출
    """
    opening_date_raw: Optional[str] = None
    head_office_address: Optional[str] = None

    # 줄 단위로 나누어 탐색
    lines = text.splitlines()

    for line in lines:
        line_stripped = line.strip()
        
        # 빈 줄은 스킵
        if not line_stripped:
            continue

        # 개업연월일 추출 (더 유연한 패턴)
        if opening_date_raw is None:
            # 패턴 1: "개업연월일 2020년 05월 01일" 또는 "개업연월일: 2020.05.01"
            if "개업연월일" in line_stripped:
                m = re.search(r"개업연월일\s*[:\-]?\s*(.+)", line_stripped)
                if m:
                    opening_date_raw = m.group(1).strip()
            
            # 패턴 2: OCR 결과가 공백으로 분리된 경우 "개업 연월일" 또는 "개업연 월일"
            if not opening_date_raw and ("개업" in line_stripped and ("연월일" in line_stripped or "월일" in line_stripped)):
                # 날짜 패턴 찾기 (년월일 형식)
                date_match = re.search(r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일", line_stripped)
                if date_match:
                    opening_date_raw = date_match.group(0)

        # 본점소재지 추출 (더 유연한 패턴)
        if head_office_address is None:
            # 패턴 1: "본점소재지 서울특별시..." 또는 "본점 소재지 서울특별시..."
            if "본점소재지" in line_stripped or "본점 소재지" in line_stripped:
                m = re.search(r"(본점\s*소재지|본점소재지)\s*[:\-]?\s*(.+)", line_stripped)
                if m:
                    head_office_address = m.group(2).strip()
            
            # 패턴 2: OCR 결과가 공백으로 분리된 경우 "본점 소재지" 또는 다음 줄에 주소
            if not head_office_address and ("본점" in line_stripped and "소재지" in line_stripped):
                # 다음 줄이나 같은 줄에서 주소 찾기
                address_match = re.search(r"(본점\s*소재지|본점소재지)\s*[:\-]?\s*(.+)", line_stripped)
                if address_match:
                    head_office_address = address_match.group(2).strip()
                else:
                    # 같은 줄에서 주소 패턴 찾기 (시/도, 구/군, 동/읍/면 등)
                    address_pattern = re.search(r"(서울|부산|대구|인천|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주|서울특별시|부산광역시|대구광역시|인천광역시|광주광역시|대전광역시|울산광역시|세종특별자치시|경기도|강원도|충청북도|충청남도|전라북도|전라남도|경상북도|경상남도|제주특별자치도).+", line_stripped)
                    if address_pattern:
                        head_office_address = address_pattern.group(0).strip()

        # 둘 다 찾았으면 조기 종료
        if opening_date_raw and head_office_address:
            break

    # 개업연월일이 없으면 날짜 패턴만으로 찾기 시도
    if not opening_date_raw:
        # 전체 텍스트에서 날짜 패턴 검색
        date_patterns = [
            r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일",  # 2020년 5월 1일
            r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})",  # 2020.05.01
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                if "년" in match.group(0):
                    opening_date_raw = match.group(0)
                else:
                    # 숫자만 있는 경우 한글 형식으로 변환
                    year, month, day = match.groups()
                    opening_date_raw = f"{year}년 {month}월 {day}일"
                break

    # 본점소재지가 없으면 주소 패턴만으로 찾기 시도
    if not head_office_address:
        # 전체 텍스트에서 주소 패턴 검색
        address_pattern = re.search(r"(서울|부산|대구|인천|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주|서울특별시|부산광역시|대구광역시|인천광역시|광주광역시|대전광역시|울산광역시|세종특별자치시|경기도|강원도|충청북도|충청남도|전라북도|전라남도|경상북도|경상남도|제주특별자치도)[^\n]{10,100}", text)
        if address_pattern:
            head_office_address = address_pattern.group(0).strip()

    opening_date_normalized = _normalize_korean_date(opening_date_raw) if opening_date_raw else None

    return {
        "opening_date_raw": opening_date_raw,
        "opening_date_normalized": opening_date_normalized,
        "head_office_address": head_office_address,
    }


__all__ = ["extract_business_registration_fields"]

