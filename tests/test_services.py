"""
LedgerService 클래스에 대한 단위 테스트
"""

import pytest
from datetime import datetime
from ledger.models import Transaction
from ledger.services import LedgerService
from ledger.repository import LedgerRepository


@pytest.fixture
def sample_transactions():
    """테스트용 샘플 거래 데이터를 생성하는 fixture"""
    return [
        Transaction(
            date=datetime(2024, 1, 15),
            category="급여",
            amount=3000000,
            transaction_type="수입",
            description="월급"
        ),
        Transaction(
            date=datetime(2024, 1, 16),
            category="식비",
            amount=15000,
            transaction_type="지출",
            description="점심"
        ),
        Transaction(
            date=datetime(2024, 1, 17),
            category="교통비",
            amount=5000,
            transaction_type="지출",
            description="버스"
        ),
        Transaction(
            date=datetime(2024, 1, 20),
            category="용돈",
            amount=100000,
            transaction_type="수입",
            description="용돈"
        )
    ]


def test_calculate_balance(sample_transactions):
    """잔액 계산이 올바르게 되는지 테스트"""
    # Repository는 실제로 사용하지 않으므로 None으로 설정
    service = LedgerService(None)
    
    result = service.calculate_balance(sample_transactions)
    
    # 총 수입: 3,000,000 + 100,000 = 3,100,000
    assert result['income'] == 3100000
    
    # 총 지출: 15,000 + 5,000 = 20,000
    assert result['expense'] == 20000
    
    # 잔액: 3,100,000 - 20,000 = 3,080,000
    assert result['balance'] == 3080000


def test_calculate_balance_empty_list():
    """빈 거래 리스트에 대한 잔액 계산 테스트"""
    service = LedgerService(None)
    
    result = service.calculate_balance([])
    
    assert result['income'] == 0
    assert result['expense'] == 0
    assert result['balance'] == 0


def test_get_category_statistics_expense(sample_transactions):
    """지출 카테고리별 통계가 올바르게 계산되는지 테스트"""
    service = LedgerService(None)
    
    result = service.get_category_statistics(sample_transactions, '지출')
    
    assert result['식비'] == 15000
    assert result['교통비'] == 5000
    assert '급여' not in result  # 수입 카테고리는 제외되어야 함
    assert '용돈' not in result


def test_get_category_statistics_income(sample_transactions):
    """수입 카테고리별 통계가 올바르게 계산되는지 테스트"""
    service = LedgerService(None)
    
    result = service.get_category_statistics(sample_transactions, '수입')
    
    assert result['급여'] == 3000000
    assert result['용돈'] == 100000
    assert '식비' not in result  # 지출 카테고리는 제외되어야 함


def test_get_category_statistics_all(sample_transactions):
    """전체 카테고리 통계가 올바르게 계산되는지 테스트"""
    service = LedgerService(None)
    
    result = service.get_category_statistics(sample_transactions)
    
    # 모든 카테고리가 포함되어야 함
    assert len(result) == 4
    assert result['급여'] == 3000000
    assert result['식비'] == 15000


def test_get_category_statistics_sorting(sample_transactions):
    """카테고리 통계가 금액 순으로 정렬되는지 테스트"""
    service = LedgerService(None)
    
    result = service.get_category_statistics(sample_transactions)
    
    # 딕셔너리를 리스트로 변환하여 순서 확인
    amounts = list(result.values())
    
    # 금액이 큰 순서대로 정렬되어 있어야 함
    assert amounts == sorted(amounts, reverse=True)