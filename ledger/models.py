"""
거래(Transaction) 데이터 모델을 정의하는 모듈

이 모듈은 가계부 애플리케이션의 핵심 데이터 구조인 Transaction 클래스를 정의합니다.
각 거래는 날짜, 카테고리, 금액, 유형(수입/지출), 설명 등의 정보를 포함합니다.

Classes:
    Transaction: 개별 거래 항목을 표현하는 클래스
    
Example:
    >>> from datetime import datetime
    >>> transaction = Transaction(
    ...     date=datetime(2024, 1, 15),
    ...     category="식비",
    ...     amount=15000,
    ...     transaction_type="지출",
    ...     description="점심 식사"
    ... )
    >>> print(transaction)
    2024-01-15 | 지출 | 식비 | 15,000원 | 점심 식사
"""

from datetime import datetime
from typing import Literal, Optional, Dict, Any, List
from enum import Enum

class TransactionType(Enum):
    """
    거래 유형을 정의하는 Enum 클래스
    
    코드의 안정성을 높이고 오타를 방지하기 위해 Enum을 사용합니다.
    """
    INCOME = "수입"
    EXPENSE = "지출"
    
    @classmethod
    def from_string(cls, value: str) -> 'TransactionType':
        """
        문자열로부터 TransactionType을 생성합니다.
        
        Args:
            value: '수입' 또는 '지출' 문자열
            
        Returns:
            TransactionType: 해당하는 Enum 값
            
        Raises:
            ValueError: 올바르지 않은 거래 유형일 때
        """
        for transaction_type in cls:
            if transaction_type.value == value:
                return transaction_type
        raise ValueError(f"올바르지 않은 거래 유형입니다: {value}")

#거래 한 건이 어떤 필드를 가지는지 결정
#클래스
class Transaction:
    def __init__(self,date,type,amount):
        self.date = date
        self.type = type 
        self.amount = amount
 #함수    
    def to_list(self):
        return [self.date, self.type, self.amount]
      
 
class Transaction:
    def __init__(self, date, ttype, amount):
        self.date = date
        self.ttype = ttype      # type은 파이썬 예약어라 ttype으로 이름 변경
        self.amount = int(amount) # 숫자로 변환해서 저장

    def to_list(self):
        return [self.date, self.ttype, self.amount]

# =========================================================
# 👇 실행 코드 (여기서 바로 입력하고 엔터 쳐서 확인)
# =========================================================
if __name__ == "__main__":
    print("=== 초간단 Transaction 테스트 ===")
    
    while True:
        print("\n⬇️ 데이터를 입력하세요 ('q' 누르면 종료)")
        
        # 1. 입력 받기
        date = input("날짜: ")
        if date == 'q': break
        
        ttype = input("구분: ")
        amount = input("금액: ")

        try:
            # 2. 객체 생성 (Class 사용)
            t = Transaction(date, ttype, amount)
            
            # 3. 결과 확인 (리스트로 잘 변환되는지)
            print(f"👉 결과: {t.to_list()}")
            
        except ValueError:
            print("❌ 에러: 금액은 숫자로 입력해주세요.")

