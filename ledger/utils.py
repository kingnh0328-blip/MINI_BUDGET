"""
유틸리티 함수 모듈
다른 ledger 모듈을 임포트하지 않아야 함!
"""

from datetime import datetime, timedelta
from typing import Tuple


def format_currency(amount: float) -> str:
    """
    금액을 원화 형식으로 포맷팅합니다.
    
    Args:
        amount: 금액
        
    Returns:
        str: 포맷팅된 금액 (예: "1,234,567원")
    """
    return f"{amount:,.0f}원"


def parse_date(date_str: str) -> datetime:
    """
    문자열을 datetime 객체로 변환합니다.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"올바르지 않은 날짜 형식입니다: {date_str}")


def get_month_range(year: int, month: int) -> Tuple[datetime, datetime]:
    """
    특정 월의 시작일과 종료일을 반환합니다.
    """
    from calendar import monthrange
    
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)
    
    return start_date, end_date