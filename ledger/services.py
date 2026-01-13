"""
가계부의 비즈니스 로직을 처리하는 서비스 모듈
통계 계산, 주식 데이터 처리 등의 기능을 제공합니다.
"""

from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import requests
from ledger.models import Transaction
from ledger.repository import LedgerRepository

class LedgerService:
    """
    가계부 관련 비즈니스 로직을 처리하는 서비스 클래스
    """
    
    def __init__(self, repository: LedgerRepository):
        """
        LedgerService 초기화
        
        Args:
            repository: LedgerRepository 인스턴스
        """
        self.repository = repository
    
    def calculate_balance(self, transactions: List[Transaction]) -> Dict[str, float]:
        """
        총 수입, 총 지출, 잔액을 계산합니다.
        
        Args:
            transactions: Transaction 객체 리스트
        
        Returns:
            dict: {'income': 총수입, 'expense': 총지출, 'balance': 잔액}
        """
        total_income = 0.0
        total_expense = 0.0
        
        for transaction in transactions:
            if transaction.transaction_type == '수입':
                total_income += transaction.amount
            elif transaction.transaction_type == '지출':
                total_expense += transaction.amount
        
        balance = total_income - total_expense
        
        return {
            'income': total_income,
            'expense': total_expense,
            'balance': balance
        }
    def get_calendar_events(self, transactions: list) -> list[dict]:
        """거래 데이터를 달력 이벤트 형식으로 변환"""
        events = []
        for t in transactions:
            # 기본 색상 설정 (수입: 파랑, 지출: 빨강)
            color = "#1C83E1" if t.transaction_type == "수입" else "#FF4B4B"
            
            # 만약 카테고리에 '투자'라는 글자가 있으면 초록색으로!
            if "투자" in t.category:
                color = "#28A745"
            
            events.append({
                "title": f"[{t.category}] {int(t.amount):,}원",
                "start": t.date.strftime("%Y-%m-%d"),
                "backgroundColor": color,
                "borderColor": color,
                "allDay": True,
                "extendedProps": {
                    "description": t.description,
                    "type": t.transaction_type
                }
            })
        return events
    
    def get_category_statistics(
        self,
        transactions: List[Transaction],
        transaction_type: str = None
    ) -> Dict[str, float]:
        """
        카테고리별 금액 통계를 계산합니다.
        
        Args:
            transactions: Transaction 객체 리스트
            transaction_type: '수입' 또는 '지출' (None이면 전체)
        
        Returns:
            dict: {카테고리명: 총금액} 형태의 딕셔너리
        """
        category_stats = {}
        
        for transaction in transactions:
            # transaction_type이 지정되었으면 해당 타입만 필터링
            if transaction_type and transaction.transaction_type != transaction_type:
                continue
            
            category = transaction.category
            if category in category_stats:
                category_stats[category] += transaction.amount
            else:
                category_stats[category] = transaction.amount
        
        # 금액이 큰 순서로 정렬
        sorted_stats = dict(sorted(
            category_stats.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        return sorted_stats
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """
        특정 월의 요약 정보를 반환합니다.
        
        Args:
            year: 연도
            month: 월
        
        Returns:
            dict: 월별 요약 정보
        """
        transactions = self.repository.get_transactions_by_month(year, month)
        balance_info = self.calculate_balance(transactions)
        
        income_by_category = self.get_category_statistics(transactions, '수입')
        expense_by_category = self.get_category_statistics(transactions, '지출')
        
        return {
            'total_income': balance_info['income'],
            'total_expense': balance_info['expense'],
            'balance': balance_info['balance'],
            'income_by_category': income_by_category,
            'expense_by_category': expense_by_category,
            'transaction_count': len(transactions)
        }
    
    def get_calendar_events(self, transactions: List[Transaction]) -> List[Dict]:
        """
        거래 내역을 캘린더 이벤트 형식으로 변환합니다.

        Args:
        transactions: Transaction 객체 리스트
        
        Returns:
        List[Dict]: 캘린더 이벤트 리스트
        
        Examples:
        events = service.get_calendar_events(transactions)
        print(events[0])
        {'title': '[AAPL] 10주 매수', 'start': '2024-01-15', 
         'backgroundColor': '#FF6B6B', 'borderColor': '#FF6B6B', 
         'textColor': '#FFFFFF'}
        
        """
        events = []
    
        for transaction in transactions:
        # 주식 거래인지 확인
            is_stock = transaction.category in ["주식매수", "주식매도"]
        
        # 이벤트 제목 생성
        if is_stock:
            # 주식 거래: description 사용 (티커와 수량 정보 포함)
            title = transaction.description if transaction.description else f"{transaction.category}"
        else:
            # 일반 거래: 카테고리 + 금액
            title = f"{transaction.category} ₩{transaction.amount:,.0f}"
        
        # 이벤트 색상 설정
        if transaction.category == "주식매수":
            color = "#FF6B6B"  # 빨간색 (매수)
        elif transaction.category == "주식매도":
            color = "#4ECDC4"  # 청록색 (매도)
        elif transaction.transaction_type == "수입":
            color = "#51CF66"  # 초록색 (일반 수입)
        else:
            color = "#FFA94D"  # 주황색 (일반 지출)
        
        # 캘린더 이벤트 객체 생성
        event = {
            "title": title,
            "start": transaction.date.strftime("%Y-%m-%d"),
            "backgroundColor": color,
            "borderColor": color,
            "textColor": "#FFFFFF"
        }
   
        events.append(event)
        return events

    def get_daily_transactions(self, date: datetime) -> List[Transaction]:
        """
        특정 날짜의 모든 거래를 조회합니다.
        
        Args:
            date: 조회할 날짜
        
        Returns:
            List[Transaction]: 해당 날짜의 거래 리스트
        """
        # 해당 날짜 하루 범위로 조회
        start = datetime(date.year, date.month, date.day, 0, 0, 0)
        end = datetime(date.year, date.month, date.day, 23, 59, 59)
        
        return self.repository.get_transactions_by_date_range(start, end)


class StockService:
    """
    주식 데이터를 처리하는 서비스 클래스
    yfinance 라이브러리를 사용하여 주가 정보를 가져옵니다.
    """

class StockService:
    @staticmethod
    def get_stock_data(ticker: str, period: str = '1mo') -> Tuple[pd.DataFrame, bool, str]:
        # [해결 1] try 문을 시작합니다.
        try:
            ticker = ticker.upper().strip()
            if not ticker:
                return pd.DataFrame(), False, "티커 심볼을 입력해주세요."
            
            # 브라우저 세션 설정 (서버 차단 우회)
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            # 데이터 다운로드
            df = yf.download(
                ticker, 
                period=period, 
                auto_adjust=True, 
                progress=False, 
                session=session
            )
            
            if df is None or len(df) == 0:
                return pd.DataFrame(), False, f"'{ticker}' 데이터를 찾을 수 없습니다."
            
            # 다중 인덱스 평면화 및 정제
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
            
            df = df.reset_index()
            return df, True, f"'{ticker}' 데이터를 성공적으로 불러왔습니다."

        # [해결 1] try와 짝꿍인 except 절을 반드시 작성해야 합니다.
        except Exception as e:
            return pd.DataFrame(), False, f"주식 데이터 조회 중 오류 발생: {str(e)}"
   
    @staticmethod
    def get_stock_info(ticker: str) -> Dict:
        """
        주식의 기본 정보를 가져옵니다.
        
        Args:
            ticker: 주식 티커 심볼
        
        Returns:
            dict: 주식 정보 딕셔너리
        """
        try:
            ticker = ticker.upper().strip()
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'name': info.get('longName', ticker),
                'current_price': info.get('currentPrice', 'N/A'),
                'currency': info.get('currency', 'USD'),
                'market_cap': info.get('marketCap', 'N/A'),
                'sector': info.get('sector', 'N/A')
            }
        except Exception as e:
            return {
                'name': ticker,
                'error': str(e)
            }