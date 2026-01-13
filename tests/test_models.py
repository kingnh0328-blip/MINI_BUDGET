"""
Transaction 모델 클래스에 대한 단위 테스트
"""

import pytest
from datetime import datetime
from ledger.models import Transaction


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
    assert transaction.amount == 15000
    assert transaction.transaction_type == "지출"
    assert transaction.description == "점심 식사"


def test_transaction_negative_amount():
    """음수 금액으로 Transaction 생성 시 오류 발생 테스트"""
    with pytest.raises(ValueError, match="금액은 0 이상이어야 합니다"):
        Transaction(
            date=datetime.now(),
            category="식비",
            amount=-5000,
            transaction_type="지출"
        )


def test_transaction_invalid_type():
    """잘못된 거래 유형으로 Transaction 생성 시 오류 발생 테스트"""
    with pytest.raises(ValueError, match="거래 유형은"):
        Transaction(
            date=datetime.now(),
            category="식비",
            amount=5000,
            transaction_type="잘못된타입"
        )


def test_transaction_to_dict():
    """Transaction 객체가 딕셔너리로 올바르게 변환되는지 테스트"""
    date = datetime(2024, 1, 15)
    transaction = Transaction(
        date=date,
        category="급여",
        amount=3000000,
        transaction_type="수입",
        description="월급"
    )
    
    result = transaction.to_dict()
    
    assert result['date'] == '2024-01-15'
    assert result['category'] == "급여"
    assert result['amount'] == 3000000
    assert result['type'] == "수입"
    assert result['description'] == "월급"


def test_transaction_from_dict():
    """딕셔너리로부터 Transaction 객체가 올바르게 생성되는지 테스트"""
    data = {
        'date': '2024-01-15',
        'category': '교통비',
        'amount': 5000,
        'type': '지출',
        'description': '버스비'
    }
    
    transaction = Transaction.from_dict(data)
    
    assert transaction.date == datetime(2024, 1, 15)
    assert transaction.category == "교통비"
    assert transaction.amount == 5000
    assert transaction.transaction_type == "지출"
    assert transaction.description == "버스비"