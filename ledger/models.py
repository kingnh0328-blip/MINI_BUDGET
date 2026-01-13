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


class Transaction:
    """
    가계부의 한 건의 거래를 나타내는 클래스
    
    이 클래스는 수입이나 지출 같은 개별 거래를 표현합니다.
    각 거래는 날짜, 카테고리, 금액, 유형, 설명 등의 속성을 가집니다.
    
    Attributes:
        date (datetime): 거래가 발생한 날짜
        category (str): 거래 카테고리 (예: 식비, 교통비, 급여 등)
        amount (float): 거래 금액 (항상 양수)
        transaction_type (str): 거래 유형 ('수입' 또는 '지출')
        description (str): 거래에 대한 추가 설명 (선택사항)
        
    Examples:
        >>> # 지출 거래 생성
        >>> expense = Transaction(
        ...     date=datetime(2024, 1, 15),
        ...     category="식비",
        ...     amount=25000,
        ...     transaction_type="지출",
        ...     description="회식"
        ... )
        
        >>> # 수입 거래 생성
        >>> income = Transaction(
        ...     date=datetime(2024, 1, 25),
        ...     category="급여",
        ...     amount=3000000,
        ...     transaction_type="수입"
        ... )
        
        >>> # 딕셔너리로 변환
        >>> data = expense.to_dict()
        >>> print(data)
        {'date': '2024-01-15', 'category': '식비', 'amount': 25000, 'type': '지출', 'description': '회식'}
    """
    
    # 카테고리 상수 정의 (기본 카테고리 목록)
    INCOME_CATEGORIES = ["급여", "보너스", "용돈", "사업소득", "이자소득", "기타"]
    EXPENSE_CATEGORIES = ["식비", "교통비", "문화생활", "쇼핑", "공과금", "의료비", 
                         "교육비", "통신비", "주거비", "보험", "저축", "기타"]
    
    def __init__(
        self,
        date: datetime,
        category: str,
        amount: float,
        transaction_type: Literal['수입', '지출'],
        description: str = ""
    ):
        """
        Transaction 객체를 초기화합니다.
        
        Args:
            date (datetime): 거래 날짜
            category (str): 카테고리명 (예: 식비, 급여)
            amount (float): 금액 (0 이상의 양수)
            transaction_type (str): '수입' 또는 '지출'
            description (str, optional): 추가 설명. 기본값은 빈 문자열
        
        Raises:
            ValueError: amount가 음수일 때
            ValueError: transaction_type이 '수입' 또는 '지출'이 아닐 때
            TypeError: 잘못된 타입의 인자가 전달될 때
            
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime.now(),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출",
            ...     description="점심"
            ... )
        """
        # 타입 검증
        if not isinstance(date, datetime):
            raise TypeError("date는 datetime 객체여야 합니다.")
        
        if not isinstance(category, str):
            raise TypeError("category는 문자열이어야 합니다.")
        
        if not isinstance(amount, (int, float)):
            raise TypeError("amount는 숫자여야 합니다.")
        
        # 값 검증
        if amount < 0:
            raise ValueError("금액은 0 이상이어야 합니다.")
        
        if transaction_type not in ['수입', '지출']:
            raise ValueError(f"거래 유형은 '수입' 또는 '지출'이어야 합니다. 입력값: {transaction_type}")
        
        if not category.strip():
            raise ValueError("카테고리는 비어있을 수 없습니다.")
        
        # 속성 할당
        self.date = date
        self.category = category.strip()
        self.amount = float(amount)  # int도 float으로 변환하여 일관성 유지
        self.transaction_type = transaction_type
        self.description = description.strip() if description else ""
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Transaction 객체를 딕셔너리 형태로 변환합니다.
        
        CSV 파일이나 JSON 형식으로 저장할 때 사용됩니다.
        날짜는 'YYYY-MM-DD' 형식의 문자열로 변환됩니다.
        
        Returns:
            dict: 다음 키를 포함하는 딕셔너리
                - date (str): 'YYYY-MM-DD' 형식의 날짜
                - category (str): 카테고리명
                - amount (float): 금액
                - type (str): 거래 유형
                - description (str): 설명
                
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime(2024, 1, 15),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출"
            ... )
            >>> transaction.to_dict()
            {'date': '2024-01-15', 'category': '식비', 'amount': 15000.0, 'type': '지출', 'description': ''}
        """
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'category': self.category,
            'amount': self.amount,
            'type': self.transaction_type,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        딕셔너리로부터 Transaction 객체를 생성합니다.
        
        CSV 파일이나 JSON에서 데이터를 읽어올 때 사용됩니다.
        누락된 필드나 잘못된 형식에 대한 처리를 포함합니다.
        
        Args:
            data (dict): 거래 정보를 담은 딕셔너리
                필수 키: date, category, amount, type
                선택 키: description
        
        Returns:
            Transaction: 생성된 Transaction 객체
            
        Raises:
            KeyError: 필수 키가 없을 때
            ValueError: 날짜 형식이 잘못되었을 때
            
        Examples:
            >>> data = {
            ...     'date': '2024-01-15',
            ...     'category': '식비',
            ...     'amount': 15000,
            ...     'type': '지출',
            ...     'description': '점심'
            ... }
            >>> transaction = Transaction.from_dict(data)
            >>> print(transaction.amount)
            15000.0
        """
        try:
            # 날짜 파싱 (여러 형식 지원)
            date_str = str(data['date'])
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                # 다른 형식도 시도
                try:
                    date = datetime.strptime(date_str, '%Y/%m/%d')
                except ValueError:
                    # ISO 8601 형식
                    date = datetime.fromisoformat(date_str.split('T')[0])
            
            return cls(
                date=date,
                category=str(data['category']),
                amount=float(data['amount']),
                transaction_type=str(data['type']),
                description=str(data.get('description', ''))
            )
        except KeyError as e:
            raise KeyError(f"필수 키가 누락되었습니다: {e}")
        except ValueError as e:
            raise ValueError(f"데이터 변환 중 오류 발생: {e}")
    
    def is_income(self) -> bool:
        """
        수입 거래인지 확인합니다.
        
        Returns:
            bool: 수입이면 True, 아니면 False
            
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime.now(),
            ...     category="급여",
            ...     amount=3000000,
            ...     transaction_type="수입"
            ... )
            >>> transaction.is_income()
            True
        """
        return self.transaction_type == "수입"
    
    def is_expense(self) -> bool:
        """
        지출 거래인지 확인합니다.
        
        Returns:
            bool: 지출이면 True, 아니면 False
            
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime.now(),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출"
            ... )
            >>> transaction.is_expense()
            True
        """
        return self.transaction_type == "지출"
    
    def get_signed_amount(self) -> float:
        """
        부호가 있는 금액을 반환합니다.
        
        수입은 양수, 지출은 음수로 반환되어 잔액 계산에 유용합니다.
        
        Returns:
            float: 수입이면 양수, 지출이면 음수 금액
            
        Examples:
            >>> income = Transaction(
            ...     date=datetime.now(),
            ...     category="급여",
            ...     amount=3000000,
            ...     transaction_type="수입"
            ... )
            >>> income.get_signed_amount()
            3000000.0
            
            >>> expense = Transaction(
            ...     date=datetime.now(),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출"
            ... )
            >>> expense.get_signed_amount()
            -15000.0
        """
        return self.amount if self.is_income() else -self.amount
    
    def matches_category(self, category: str) -> bool:
        """
        지정된 카테고리와 일치하는지 확인합니다.
        
        대소문자를 구분하지 않고, 공백을 제거하여 비교합니다.
        
        Args:
            category (str): 비교할 카테고리명
            
        Returns:
            bool: 일치하면 True, 아니면 False
            
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime.now(),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출"
            ... )
            >>> transaction.matches_category("식비")
            True
            >>> transaction.matches_category("교통비")
            False
        """
        return self.category.strip().lower() == category.strip().lower()
    
    def is_in_date_range(self, start_date: datetime, end_date: datetime) -> bool:
        """
        지정된 날짜 범위 내에 있는지 확인합니다.
        
        Args:
            start_date (datetime): 시작 날짜 (포함)
            end_date (datetime): 종료 날짜 (포함)
            
        Returns:
            bool: 범위 내에 있으면 True, 아니면 False
            
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime(2024, 1, 15),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출"
            ... )
            >>> transaction.is_in_date_range(
            ...     datetime(2024, 1, 1),
            ...     datetime(2024, 1, 31)
            ... )
            True
        """
        return start_date <= self.date <= end_date
    
    def __str__(self) -> str:
        """
        Transaction 객체를 사람이 읽기 쉬운 문자열로 변환합니다.
        
        print() 함수나 str() 함수 호출 시 사용됩니다.
        
        Returns:
            str: 거래 정보를 담은 문자열
            
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime(2024, 1, 15),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출",
            ...     description="점심"
            ... )
            >>> print(transaction)
            2024-01-15 | 지출 | 식비 | 15,000원 | 점심
        """
        return (f"{self.date.strftime('%Y-%m-%d')} | "
                f"{self.transaction_type} | "
                f"{self.category} | "
                f"{self.amount:,.0f}원 | "
                f"{self.description}")
    
    def __repr__(self) -> str:
        """
        Transaction 객체의 개발자 친화적인 표현을 반환합니다.
        
        디버깅이나 로깅에 유용합니다.
        
        Returns:
            str: 객체 생성을 재현할 수 있는 문자열
            
        Examples:
            >>> transaction = Transaction(
            ...     date=datetime(2024, 1, 15),
            ...     category="식비",
            ...     amount=15000,
            ...     transaction_type="지출"
            ... )
            >>> repr(transaction)
            "Transaction(date=datetime(2024, 1, 15, 0, 0), category='식비', amount=15000.0, transaction_type='지출', description='')"
        """
        return (f"Transaction(date={repr(self.date)}, "
                f"category={repr(self.category)}, "
                f"amount={self.amount}, "
                f"transaction_type={repr(self.transaction_type)}, "
                f"description={repr(self.description)})")
    
    def __eq__(self, other: object) -> bool:
        """
        두 Transaction 객체가 같은지 비교합니다.
        
        모든 속성이 동일하면 같은 것으로 간주합니다.
        
        Args:
            other: 비교할 다른 객체
            
        Returns:
            bool: 같으면 True, 아니면 False
            
        Examples:
            >>> t1 = Transaction(datetime(2024, 1, 15), "식비", 15000, "지출")
            >>> t2 = Transaction(datetime(2024, 1, 15), "식비", 15000, "지출")
            >>> t1 == t2
            True
        """
        if not isinstance(other, Transaction):
            return False
        return (self.date == other.date and
                self.category == other.category and
                self.amount == other.amount and
                self.transaction_type == other.transaction_type and
                self.description == other.description)
    
    def __hash__(self) -> int:
        """
        Transaction 객체의 해시값을 반환합니다.
        
        Set이나 Dict의 키로 사용할 수 있게 합니다.
        
        Returns:
            int: 해시값
        """
        return hash((
            self.date,
            self.category,
            self.amount,
            self.transaction_type,
            self.description
        ))
    
    @classmethod
    def get_income_categories(cls) -> list[str]:
        """
        수입 카테고리 목록을 반환합니다.
        
        Returns:
            list[str]: 수입 카테고리 리스트
            
        Examples:
            >>> categories = Transaction.get_income_categories()
            >>> print(categories)
            ['급여', '보너스', '용돈', '사업소득', '이자소득', '기타']
        """
        return cls.INCOME_CATEGORIES.copy()
    
    @classmethod
    def get_expense_categories(cls) -> list[str]:
        """
        지출 카테고리 목록을 반환합니다.
        
        Returns:
            list[str]: 지출 카테고리 리스트
            
        Examples:
            >>> categories = Transaction.get_expense_categories()
            >>> '식비' in categories
            True
        """
        return cls.EXPENSE_CATEGORIES.copy()
    
    @classmethod
    def validate_category(cls, category: str, transaction_type: str) -> bool:
        """
        카테고리가 해당 거래 유형에 적합한지 검증합니다.
        
        Args:
            category (str): 검증할 카테고리
            transaction_type (str): 거래 유형 ('수입' 또는 '지출')
            
        Returns:
            bool: 적합하면 True, 아니면 False
            
        Examples:
            >>> Transaction.validate_category("급여", "수입")
            True
            >>> Transaction.validate_category("식비", "수입")
            False
        """
        if transaction_type == "수입":
            return category in cls.INCOME_CATEGORIES
        elif transaction_type == "지출":
            return category in cls.EXPENSE_CATEGORIES
        return False


# 모듈 레벨 헬퍼 함수들

def create_income(
    date: datetime,
    category: str,
    amount: float,
    description: str = ""
) -> Transaction:
    """
    수입 거래를 생성하는 헬퍼 함수입니다.
    
    Args:
        date: 거래 날짜
        category: 카테고리
        amount: 금액
        description: 설명 (선택)
        
    Returns:
        Transaction: 수입 거래 객체
        
    Examples:
        >>> income = create_income(
        ...     date=datetime(2024, 1, 25),
        ...     category="급여",
        ...     amount=3000000,
        ...     description="1월 급여"
        ... )
        >>> income.is_income()
        True
    """
    return Transaction(
        date=date,
        category=category,
        amount=amount,
        transaction_type="수입",
        description=description
    )


def create_expense(
    date: datetime,
    category: str,
    amount: float,
    description: str = ""
) -> Transaction:
    """
    지출 거래를 생성하는 헬퍼 함수입니다.
    
    Args:
        date: 거래 날짜
        category: 카테고리
        amount: 금액
        description: 설명 (선택)
        
    Returns:
        Transaction: 지출 거래 객체
        
    Examples:
        >>> expense = create_expense(
        ...     date=datetime(2024, 1, 15),
        ...     category="식비",
        ...     amount=25000,
        ...     description="저녁 회식"
        ... )
        >>> expense.is_expense()
        True
    """
    return Transaction(
        date=date,
        category=category,
        amount=amount,
        transaction_type="지출",
        description=description
    )