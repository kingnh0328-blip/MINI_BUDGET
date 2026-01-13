from datetime import datetime
from typing import Optional
from calendar import monthrange

def parse_date(date_str: str) -> Optional[datetime]:
    """문자열을 datetime으로 변환 (여러 형식 대응)"""
    for fmt in ('%Y-%m-%d', '%Y/%m/%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def format_date(date: datetime) -> str:
    """datetime 객체를 'YYYY-MM-DD' 문자열로 변환"""
    return date.strftime('%Y-%m-%d')

def is_valid_amount(amount: str) -> bool:
    """입력된 금액이 유효한 숫자인지 검사"""
    try:
        return float(amount) >= 0
    except (ValueError, TypeError):
        return False

def format_currency(amount: float) -> str:
    """금액을 한국 원화 형식으로 포맷팅 (예: 15,000원)"""
    return f"{int(amount):,}원"

def get_month_range(year: int, month: int) -> tuple[datetime, datetime]:
    """특정 년월의 시작일과 종료일을 반환"""
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    # 종료일은 해당 날짜의 마지막 순간(23:59:59)까지 포함하도록 설정
    end_date = datetime(year, month, last_day, 23, 59, 59)
    return start_date, end_date