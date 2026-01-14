"""
Transaction 모델 클래스에 대한 단위 테스트
"""

import pytest
from datetime import datetime
from ledger.models import Transaction, TransactionType, create_income, create_expense


def test_transaction_creation():
    """Transaction 객체가 올바르게 생성되는지 테스트"""
    date = datetime(2024, 1, 15)
    transaction = Transaction(
        date=date,
        category="식비",
        amount=15000,
        transaction_type="지출",
        description="점심 식사"
    )
    
    assert transaction.date == date
    assert transaction.category == "식비"
    assert transaction.amount == 15000.0
    assert transaction.transaction_type == "지출"
    assert transaction.description == "점심 식사"


def test_transaction_validation_errors():
    """잘못된 입력값에 대한 예외 발생 테스트"""
    # 1. 음수 금액
    with pytest.raises(ValueError, match="금액은 0 이상이어야 합니다"):
        Transaction(datetime.now(), "식비", -5000, "지출")
    
    # 2. 잘못된 거래 유형
    with pytest.raises(ValueError, match="거래 유형은"):
        Transaction(datetime.now(), "식비", 5000, "선물")
        
    # 3. 비어있는 카테고리
    with pytest.raises(ValueError, match="카테고리는 비어있을 수 없습니다"):
        Transaction(datetime.now(), "  ", 5000, "지출")


def test_transaction_to_dict():
    """객체 -> 딕셔너리 변환 테스트"""
    date = datetime(2024, 1, 15)
    transaction = Transaction(date, "급여", 3000000, "수입", "월급")
    
    result = transaction.to_dict()
    assert result['date'] == '2024-01-15'
    assert result['category'] == "급여"
    assert result['amount'] == 3000000.0
    assert result['type'] == "수입"


def test_transaction_from_dict():
    """딕셔너리 -> 객체 생성 테스트 (다양한 날짜 형식 포함)"""
    # 표준 형식
    data1 = {'date': '2024-01-15', 'category': '교통비', 'amount': 5000, 'type': '지출'}
    t1 = Transaction.from_dict(data1)
    assert t1.date == datetime(2024, 1, 15)
    
    # 슬래시(/) 형식
    data2 = {'date': '2024/02/20', 'category': '식비', 'amount': 10000, 'type': '지출'}
    t2 = Transaction.from_dict(data2)
    assert t2.date == datetime(2024, 2, 20)


def test_get_signed_amount():
    """부호가 있는 금액 반환 테스트 (수입은 +, 지출은 -)"""
    income = Transaction(datetime.now(), "급여", 1000, "수입")
    expense = Transaction(datetime.now(), "식비", 500, "지출")
    
    assert income.get_signed_amount() == 1000.0
    assert expense.get_signed_amount() == -500.0


def test_is_in_date_range():
    """날짜 범위 확인 기능 테스트"""
    tx = Transaction(datetime(2024, 1, 15), "식비", 1000, "지출")
    
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 31)
    
    assert tx.is_in_date_range(start, end) is True
    assert tx.is_in_date_range(datetime(2024, 2, 1), datetime(2024, 2, 28)) is False


def test_helper_functions():
    """create_income, create_expense 헬퍼 함수 테스트"""
    income = create_income(datetime.now(), "보너스", 50000)
    expense = create_expense(datetime.now(), "쇼핑", 30000)
    
    assert income.is_income() is True
    assert expense.is_expense() is True
    assert income.category == "보너스"
    assert expense.category == "쇼핑"


def test_transaction_equality():
    """두 객체의 동등성 비교(__eq__) 테스트"""
    date = datetime(2024, 1, 1)
    t1 = Transaction(date, "식비", 1000, "지출", "점심")
    t2 = Transaction(date, "식비", 1000, "지출", "점심")
    t3 = Transaction(date, "식비", 2000, "지출", "저녁")
    
    assert t1 == t2
    assert t1 != t3


def test_category_validation():
    """카테고리 유효성 검사 클래스 메서드 테스트"""
    assert Transaction.validate_category("급여", "수입") is True
    assert Transaction.validate_category("식비", "수입") is False
    assert Transaction.validate_category("식비", "지출") is True