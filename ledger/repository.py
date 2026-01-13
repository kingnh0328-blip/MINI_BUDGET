이것은 테스트

"""
CSV 파일을 통한 데이터 저장 및 조회 기능을 제공하는 모듈
ledger.csv 파일과의 모든 입출력을 담당합니다.
"""

import os
import pandas as pd
from typing import List
from datetime import datetime
from ledger.models import Transaction


class LedgerRepository:
    """
    가계부 데이터를 CSV 파일에 저장하고 불러오는 클래스
    """
    
    def __init__(self, csv_path: str = 'data/ledger.csv'):
        """
        LedgerRepository 초기화
        
        Args:
            csv_path: CSV 파일 경로
        """
        self.csv_path = csv_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """
        CSV 파일이 존재하지 않으면 빈 파일을 생성합니다.
        """
        # data 폴더가 없으면 생성
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        
        # CSV 파일이 없으면 헤더만 있는 빈 파일 생성
        if not os.path.exists(self.csv_path):
            df = pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'description'])
            df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
    
    def save_transaction(self, transaction: Transaction):
        """
        새로운 거래를 CSV 파일에 추가합니다.
        
        Args:
            transaction: 저장할 Transaction 객체
        """
        try:
            # 기존 데이터 읽기
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            
            # 새 거래를 DataFrame에 추가
            new_row = pd.DataFrame([transaction.to_dict()])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # CSV 파일에 저장
            df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            
        except Exception as e:
            raise Exception(f"거래 저장 중 오류 발생: {str(e)}")
    
    def get_all_transactions(self) -> List[Transaction]:
        """
        모든 거래 내역을 불러옵니다.
        
        Returns:
            List[Transaction]: Transaction 객체 리스트
        """
        try:
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            
            # 데이터가 비어있으면 빈 리스트 반환
            if df.empty:
                return []
            
            # DataFrame의 각 행을 Transaction 객체로 변환
            transactions = []
            for _, row in df.iterrows():
                try:
                    transaction = Transaction.from_dict(row.to_dict())
                    transactions.append(transaction)
                except Exception as e:
                    # 잘못된 데이터는 건너뛰고 계속 진행
                    print(f"데이터 변환 오류 (건너뜀): {str(e)}")
                    continue
            
            return transactions
            
        except FileNotFoundError:
            # 파일이 없으면 빈 리스트 반환
            return []
        except Exception as e:
            raise Exception(f"거래 조회 중 오류 발생: {str(e)}")
    
    def get_transactions_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Transaction]:
        """
        특정 날짜 범위의 거래 내역을 조회합니다.
        
        Args:
            start_date: 시작 날짜
            end_date: 종료 날짜
        
        Returns:
            List[Transaction]: 해당 기간의 Transaction 객체 리스트
        """
        all_transactions = self.get_all_transactions()
        
        # 날짜 범위에 해당하는 거래만 필터링
        filtered = [
            t for t in all_transactions
            if start_date <= t.date <= end_date
        ]
        
        # 날짜순으로 정렬
        filtered.sort(key=lambda x: x.date)
        
        return filtered
    
    def get_transactions_by_month(self, year: int, month: int) -> List[Transaction]:
        """
        특정 월의 거래 내역을 조회합니다.
        
        Args:
            year: 연도
            month: 월 (1-12)
        
        Returns:
            List[Transaction]: 해당 월의 Transaction 객체 리스트
        """
        from ledger.utils import get_month_range
        
        start_date, end_date = get_month_range(year, month)
        return self.get_transactions_by_date_range(start_date, end_date)
    
    def delete_all_transactions(self):
        """
        모든 거래 내역을 삭제합니다. (주의: 복구 불가능)
        """
        df = pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'description'])
        df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        전체 거래 내역을 DataFrame으로 반환합니다.
        데이터 분석 및 시각화에 유용합니다.
        
        Returns:
            pd.DataFrame: 거래 내역 DataFrame
        """
        try:
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            # 오류 발생 시 빈 DataFrame 반환
            return pd.DataFrame(columns=['date', 'category', 'amount', 'type', 'description'])
