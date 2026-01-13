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

