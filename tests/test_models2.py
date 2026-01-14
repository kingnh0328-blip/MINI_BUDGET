from datetime import datetime

class Transaction:
    def __init__(self, date, category, amount, transaction_type, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description

    def to_dict(self):
        """객체를 딕셔너리로 변환 (테스트의 기대 결과에 맞춤)"""
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'category': self.category,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리 데이터를 받아 객체 인스턴스 생성"""
        return cls(
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            category=data['category'],
            amount=data['amount'],
            transaction_type=data['transaction_type'],
            description=data['description']
        )