"""
가계부의 비즈니스 로직을 처리하는 서비스 모듈
"""

from typing import Dict, List, Tuple
from datetime import datetime
import pandas as pd
import yfinance as yf
import requests
from ledger.models import Transaction
from ledger.repository import LedgerRepository

class LedgerService:
    def __init__(self, repository: LedgerRepository):
        self.repository = repository
    
    def update_transaction(self, index: int, updated_transaction: Transaction):
        """지정된 인덱스의 거래 내역을 수정합니다."""
        transactions = self.repository.get_all_transactions()
        if 0 <= index < len(transactions):
            transactions[index] = updated_transaction
            # Repository의 전체 저장 메서드를 호출합니다.
            return self.repository._save_all_to_csv(transactions)
        return False

    def delete_transaction(self, index: int):
        """지정된 인덱스의 거래 내역을 삭제합니다."""
        transactions = self.repository.get_all_transactions()
        if 0 <= index < len(transactions):
            transactions.pop(index)
            return self.repository._save_all_to_csv(transactions)
        return False

    def calculate_balance(self, transactions: List[Transaction]) -> Dict[str, float]:
        total_income = 0.0
        total_expense = 0.0
        for t in transactions:
            if t.transaction_type == '수입':
                total_income += t.amount
            else:
                total_expense += t.amount
        return {'income': total_income, 'expense': total_expense, 'balance': total_income - total_expense}

    def get_calendar_events(self, transactions: List[Transaction]) -> List[Dict]:
        events = []
        for t in transactions:
            is_stock = t.category in ["주식매수", "주식매도"]
            title = t.description if is_stock and t.description else f"[{t.category}] {int(t.amount):,}원"
            
            if t.category == "주식매수": color = "#FF6B6B"
            elif t.category == "주식매도": color = "#4ECDC4"
            elif t.transaction_type == "수입": color = "#51CF66"
            else: color = "#FFA94D"

            events.append({
                "title": title,
                "start": t.date.strftime("%Y-%m-%d"),
                "backgroundColor": color,
                "borderColor": color,
                "textColor": "#FFFFFF"
            })
        return events

    def get_monthly_summary(self, year: int, month: int) -> Dict:
        transactions = self.repository.get_transactions_by_month(year, month)
        balance_info = self.calculate_balance(transactions)
        return {
            'total_income': balance_info['income'],
            'total_expense': balance_info['expense'],
            'balance': balance_info['balance'],
            'income_by_category': self.get_category_statistics(transactions, '수입'),
            'expense_by_category': self.get_category_statistics(transactions, '지출'),
            'transaction_count': len(transactions)
        }

    def get_category_statistics(self, transactions: List[Transaction], t_type: str = None) -> Dict[str, float]:
        stats = {}
        for t in transactions:
            if t_type and t.transaction_type != t_type: continue
            stats[t.category] = stats.get(t.category, 0) + t.amount
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    def get_daily_transactions(self, date: datetime) -> List[Transaction]:
        start = datetime(date.year, date.month, date.day, 0, 0, 0)
        end = datetime(date.year, date.month, date.day, 23, 59, 59)
        return self.repository.get_transactions_by_date_range(start, end)

class StockService:
# services.py의 StockService 부분을 이렇게 수정해라냐!

    @staticmethod
    def get_stock_data(ticker: str, period: str = '1mo') -> Tuple[pd.DataFrame, bool, str]:
        try:
            ticker = ticker.upper().strip()
            if not ticker:
                return pd.DataFrame(), False, "티커 심볼을 입력해주세요."
            
            # [수정] 세션(requests.Session) 설정 코드를 싹 다 지우고 아래처럼 호출해라냐!
            df = yf.download(
                ticker, 
                period=period, 
                auto_adjust=True, 
                progress=False
                # session=session 이 부분을 지워야 한다냐!
            )
            
            if df is None or len(df) == 0:
                return pd.DataFrame(), False, f"'{ticker}' 데이터를 찾을 수 없습니다."
            
            # 컬럼 정리 로직 (기존과 동일)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
            
            df = df.reset_index()
            return df, True, f"'{ticker}' 데이터를 성공적으로 불러왔습니다."

        except Exception as e:
            return pd.DataFrame(), False, f"주식 데이터 조회 중 오류 발생: {str(e)}"
   
    @staticmethod
    def get_stock_info(ticker: str) -> Dict:
        try:
            stock = yf.Ticker(ticker.upper().strip())
            info = stock.info
            return {
                'name': info.get('longName', ticker),
                'current_price': info.get('currentPrice', 'N/A'),
                'currency': info.get('currency', 'USD'),
                'sector': info.get('sector', 'N/A')
            }
        except:
            return {'name': ticker, 'current_price': 'N/A'}