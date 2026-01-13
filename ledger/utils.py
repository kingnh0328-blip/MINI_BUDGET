"""
날짜 변환 및 유효성 검사 등의 유틸리티 함수를 제공하는 모듈
"""

from datetime import datetime
from typing import Optional


def parse_date(date_str: str) -> Optional[datetime]:
    """
    문자열을 datetime 객체로 변환합니다.
    
    Args:
        date_str: 날짜 문자열 (예: '2024-01-15')
    
    Returns:
        datetime 객체 또는 None (변환 실패 시)
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None


def format_date(date: datetime) -> str:
    """
    datetime 객체를 문자열로 변환합니다.
    
    Args:
        date: datetime 객체
    
    Returns:
        str: 'YYYY-MM-DD' 형식의 날짜 문자열
    """
    return date.strftime('%Y-%m-%d')


def is_valid_amount(amount: str) -> bool:
    """
    입력된 금액이 유효한 숫자인지 검사합니다.
    
    Args:
        amount: 검사할 금액 문자열
    
    Returns:
        bool: 유효한 금액이면 True, 아니면 False
    """
    try:
        value = float(amount)
        return value >= 0
    except (ValueError, TypeError):
        return False


def format_currency(amount: float) -> str:
    """
    금액을 한국 원화 형식으로 포맷팅합니다.
    
    Args:
        amount: 금액
    
    Returns:
        str: 포맷팅된 금액 문자열 (예: '1,000,000원')
    """
    return f"{amount:,.0f}원"


def get_month_range(year: int, month: int) -> tuple[datetime, datetime]:
    """
    특정 년월의 시작일과 종료일을 반환합니다.
    
    Args:
        year: 연도
        month: 월 (1-12)
    
    Returns:
        tuple: (시작일, 종료일) datetime 객체 튜플
    """
    from calendar import monthrange
    
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day)
    
    return start_date, end_date