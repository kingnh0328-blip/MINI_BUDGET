"""
LedgerService 클래스에 대한 단위 테스트
"""

import pytest
from datetime import datetime
from ledger.models import Transaction
from ledger.services import LedgerService
from ledger.repository import LedgerRepository
from unittest.mock import MagicMock

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
def test_update_transaction(sample_transactions):
    """거래 내역 수정 기능 테스트"""
    # 1. 가짜 저장소(Mock) 만들기
    mock_repo = MagicMock()
    
    # 중요! 테스트용 데이터를 변수에 따로 담아둔다냐
    test_data = sample_transactions[:] 
    mock_repo.get_all_transactions.return_value = test_data
    
    service = LedgerService(mock_repo)
    
    # 2. 수정할 데이터 준비
    updated_tx = Transaction(
        date=datetime(2024, 1, 15),
        category="보너스",
        amount=500000,
        transaction_type="수입",
        description="상반기 보너스"
    )
    
    # 3. 수정 실행
    service.update_transaction(0, updated_tx)
    
    # 4. 검증: 원본(sample_transactions)이 아니라 서비스가 사용한 test_data를 확인해야 한다냐!
    assert test_data[0].category == "보너스"
    assert test_data[0].amount == 500000
    
    # 저장 함수가 호출되었는지 확인
    mock_repo._save_all_to_csv.assert_called_once()

def test_delete_transaction(sample_transactions):
    """거래 내역 삭제 기능 테스트"""
    mock_repo = MagicMock()
    # 복사본을 전달해서 원본 보존
    current_data = sample_transactions[:]
    mock_repo.get_all_transactions.return_value = current_data
    service = LedgerService(mock_repo)
    
    initial_count = len(current_data)
    
    # 삭제 실행 (첫 번째 항목 삭제)
    service.delete_transaction(0)
    
    # 검증: 개수가 하나 줄었는지 확인
    assert len(current_data) == initial_count - 1
    # 저장 메서드가 호출되었는지 확인
    mock_repo._save_all_to_csv.assert_called_once()