# 💰 나만의 미니 가계부 (Mini Ledger)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Streamlit 기반의 직관적이고 강력한 개인 재무 관리 웹 애플리케이션**

[빠른 시작](#-빠른-시작) • [주요 기능](#-주요-기능) • [스크린샷](#-스크린샷) • [설치 가이드](#-설치-가이드) • [사용법](#-사용법)

</div>

---

## 📖 소개

나만의 미니 가계부는 Python과 Streamlit으로 만든 개인 재무 관리 도구입니다. 
수입과 지출을 간편하게 기록하고, 아름다운 차트로 재무 현황을 한눈에 파악할 수 있습니다. 
추가로 실시간 주식 차트 기능까지 제공하여 자산 관리에 도움을 줍니다.

### ✨ 왜 미니 가계부인가?

- 🎯 **간단함**: 복잡한 설정 없이 바로 사용 가능
- 💾 **로컬 저장**: 민감한 재무 데이터를 내 컴퓨터에 안전하게 보관
- 📊 **시각화**: Plotly 기반의 인터랙티브한 차트
- 🔧 **확장 가능**: 모듈화된 코드로 기능 추가가 쉬움
- 🎓 **학습용**: 초보자도 이해하기 쉬운 깔끔한 코드 구조

---

## 🚀 빠른 시작

### Windows 사용자

```bash
# 1. 프로젝트 폴더로 이동
cd mini-ledger

# 2. 자동 설치 (최초 1회)
setup.bat

# 3. 앱 실행
run.bat
```

### Mac / Linux 사용자

```bash
# 1. 프로젝트 폴더로 이동
cd mini-ledger

# 2. 자동 설치 (최초 1회)
chmod +x setup.sh
./setup.sh

# 3. 앱 실행
chmod +x run.sh
./run.sh
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 앱을 사용할 수 있습니다!

---

## 🎯 주요 기능

### 1️⃣ 📝 거래 입력

<img src="https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Transaction+Input+Screenshot" alt="거래 입력 화면" width="100%">

**쉽고 빠른 수입/지출 기록**

- 📅 **날짜 선택**: 직관적인 캘린더 위젯
- 💵 **거래 유형**: 수입 또는 지출 선택
- 🏷️ **스마트 카테고리**: 
  - 수입: 급여, 보너스, 용돈, 기타
  - 지출: 식비, 교통비, 문화생활, 쇼핑, 공과금, 기타
- 💰 **금액 입력**: 1,000원 단위 자동 증감
- 📋 **메모 기능**: 거래에 대한 상세 설명 추가

**사용 예시**:
```
날짜: 2024-01-15
유형: 지출
카테고리: 식비
금액: 25,000원
설명: 저녁 회식
→ 저장 버튼 클릭 → ✅ 완료!
```

---

### 2️⃣ 📊 가계부 조회

<img src="https://via.placeholder.com/800x400/2ECC71/FFFFFF?text=Ledger+View+Screenshot" alt="가계부 조회 화면" width="100%">

**3가지 방식의 유연한 조회**

#### 📅 일별 조회
- 특정 날짜의 모든 거래 내역 확인
- 해당 날짜의 수입, 지출, 잔액 요약

#### 📆 기간별 조회
- 시작일과 종료일을 지정하여 조회
- 주간, 월간 재무 현황 파악에 유용

#### 📜 전체 조회
- 앱을 사용한 이후 모든 거래 내역
- 전체 재무 히스토리 한눈에 확인

**표시 정보**:
- 📈 총 수입
- 📉 총 지출
- 💵 잔액 (수입 - 지출)
- 📋 거래 내역 테이블 (날짜, 구분, 카테고리, 금액, 설명)

---

### 3️⃣ 📈 통계 및 분석

<img src="https://via.placeholder.com/800x400/E67E22/FFFFFF?text=Statistics+Screenshot" alt="통계 화면" width="100%">

**월별 재무 분석 대시보드**

#### 🎯 요약 지표
- 💰 **총 수입**: 해당 월의 모든 수입 합계
- 💸 **총 지출**: 해당 월의 모든 지출 합계
- 💵 **잔액**: 수입 - 지출
- 📊 **거래 건수**: 총 기록된 거래 수

#### 📊 시각화 차트

**수입 카테고리별 도넛 차트**
- 어떤 경로로 수입이 발생했는지 한눈에 파악
- 인터랙티브 Plotly 차트
- 카테고리별 금액과 비율 표시

**지출 카테고리별 도넛 차트**
- 어디에 가장 많이 지출했는지 분석
- 불필요한 지출 항목 발견
- 절약 계획 수립에 유용

#### 📋 상세 내역
- 각 카테고리별 정확한 금액 표시
- 금액이 큰 순서대로 정렬

**활용 예시**:
```
2024년 1월 통계
- 총 수입: 3,500,000원
- 총 지출: 1,850,000원
- 잔액: 1,650,000원
- 거래 건수: 42건

주요 지출:
- 식비: 450,000원 (24.3%)
- 교통비: 180,000원 (9.7%)
- 문화생활: 320,000원 (17.3%)
```

---

### 4️⃣ 📉 주식 차트

<img src="https://via.placeholder.com/800x400/9B59B6/FFFFFF?text=Stock+Chart+Screenshot" alt="주식 차트 화면" width="100%">

**실시간 주식 시장 데이터 조회**

#### 🔍 지원 기능
- 🌍 **미국 주식**: NASDAQ, NYSE 등 모든 미국 상장 주식
- 📊 **캔들스틱 차트**: 전문가급 주가 차트
- 📈 **거래량 차트**: 시장 활동성 파악
- 📋 **상세 데이터**: OHLCV 데이터 테이블

#### ⏱️ 조회 기간 옵션
- `1d` - 1일
- `5d` - 5일
- `1mo` - 1개월 (기본값)
- `3mo` - 3개월
- `6mo` - 6개월
- `1y` - 1년

#### 📊 차트 정보
- 📈 **캔들스틱 차트**: Open, High, Low, Close 한눈에
- 📊 **거래량 바 차트**: 일별 거래량 시각화
- 💰 **현재가**: 실시간 주가 정보
- 🏢 **기업 정보**: 회사명, 섹터, 통화

**사용 예시**:
```
티커 입력: AAPL
기간: 1mo
→ 차트 보기 클릭

결과:
✅ Apple Inc.
현재가: $185.92
섹터: Technology
통화: USD

+ 캔들스틱 차트
+ 거래량 차트
+ 상세 데이터 테이블
```

#### 💡 인기 티커 예시
- **AAPL** - Apple
- **TSLA** - Tesla
- **MSFT** - Microsoft
- **GOOGL** - Google (Alphabet)
- **AMZN** - Amazon
- **NVDA** - NVIDIA
- **META** - Meta (Facebook)

---

## 📸 스크린샷

> 실제 애플리케이션 화면 예시입니다.

<details>
<summary>🖼️ 더 많은 스크린샷 보기</summary>

### 메인 화면
![메인 화면](https://via.placeholder.com/800x450/34495E/FFFFFF?text=Main+Dashboard)

### 거래 입력
![거래 입력](https://via.placeholder.com/800x450/3498DB/FFFFFF?text=Transaction+Input)

### 통계 대시보드
![통계](https://via.placeholder.com/800x450/E74C3C/FFFFFF?text=Statistics+Dashboard)

### 주식 차트
![주식 차트](https://via.placeholder.com/800x450/1ABC9C/FFFFFF?text=Stock+Chart)

</details>

---

## 💻 설치 가이드

### 시스템 요구사항

- **Python**: 3.8 이상
- **운영체제**: Windows, macOS, Linux
- **인터넷**: 주식 차트 기능 사용 시 필요

### 방법 1: 자동 설치 스크립트 (권장)

#### Windows
```bash
setup.bat
```

#### Mac / Linux
```bash
chmod +x setup.sh
./setup.sh
```

### 방법 2: 수동 설치

```bash
# 1. Python 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. 필요한 라이브러리 설치
pip install -r requirements.txt

# 4. 애플리케이션 실행
streamlit run app.py
```

### 설치되는 라이브러리

| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| streamlit | 1.28+ | 웹 애플리케이션 프레임워크 |
| pandas | 2.0+ | 데이터 처리 및 분석 |
| yfinance | 0.2.28+ | 주식 데이터 조회 |
| plotly | 5.17+ | 인터랙티브 차트 |
| pytest | 7.4+ | 단위 테스트 |

---

## 📚 사용법

### 기본 워크플로우

```mermaid
graph LR
    A[앱 실행] --> B[거래 입력]
    B --> C[가계부 조회]
    C --> D[통계 분석]
    D --> E[주식 차트 확인]
    E --> B
```

### 1. 거래 기록하기

1. 좌측 사이드바에서 **"📝 거래 입력"** 선택
2. 날짜, 유형, 카테고리, 금액 입력
3. 필요시 설명 추가
4. **"💾 저장"** 버튼 클릭

### 2. 거래 내역 확인하기

1. 좌측 사이드바에서 **"📊 가계부 조회"** 선택
2. 조회 방법 선택:
   - 일별 조회: 특정 날짜 선택
   - 기간별 조회: 시작일/종료일 선택
   - 전체 조회: 바로 조회
3. 요약 정보와 테이블 확인

### 3. 통계 보기

1. 좌측 사이드바에서 **"📈 통계"** 선택
2. 연도와 월 선택
3. 요약 지표 및 차트 확인
4. 카테고리별 지출 분석

### 4. 주식 차트 보기

1. 좌측 사이드바에서 **"📉 주식 차트"** 선택
2. 티커 심볼 입력 (예: AAPL)
3. 조회 기간 선택
4. **"📊 차트 보기"** 버튼 클릭
5. 캔들스틱 차트와 거래량 확인

---

## 🏗️ 프로젝트 구조

```
mini-ledger/
├── 📄 app.py                      # Streamlit 메인 애플리케이션
├── 📄 requirements.txt            # Python 패키지 의존성
├── 📄 README.md                   # 프로젝트 문서 (이 파일)
├── 📄 .gitignore                  # Git 무시 파일 설정
├── 📄 setup.bat / setup.sh        # 자동 설치 스크립트
├── 📄 run.bat / run.sh            # 자동 실행 스크립트
│
├── 📁 ledger/                     # 핵심 비즈니스 로직
│   ├── 📄 __init__.py            # 패키지 초기화
│   ├── 📄 models.py              # Transaction 데이터 모델
│   ├── 📄 repository.py          # CSV 데이터 저장소 관리
│   ├── 📄 services.py            # 비즈니스 로직 (계산, 통계, 주식)
│   └── 📄 utils.py               # 유틸리티 함수 (날짜, 형식)
│
├── 📁 tests/                      # 단위 테스트
│   ├── 📄 __init__.py
│   ├── 📄 test_models.py         # 모델 테스트
│   └── 📄 test_services.py       # 서비스 테스트
│
└── 📁 data/                       # 데이터 저장소
    └── 📄 ledger.csv             # 거래 내역 CSV 파일
```

### 아키텍처 설명

#### 📄 app.py - 프레젠테이션 레이어
- Streamlit UI 구성
- 사용자 입력 처리
- 화면 렌더링

#### 📁 ledger/ - 비즈니스 로직 레이어

**models.py** - 데이터 모델
```python
class Transaction:
    - 거래 정보를 담는 클래스
    - 날짜, 카테고리, 금액, 유형, 설명
    - 유효성 검사 포함
```

**repository.py** - 데이터 액세스 레이어
```python
class LedgerRepository:
    - CSV 파일 읽기/쓰기
    - 거래 저장 및 조회
    - 날짜 범위 필터링
```

**services.py** - 비즈니스 로직
```python
class LedgerService:
    - 잔액 계산
    - 카테고리별 통계
    - 월별 요약

class StockService:
    - 주식 데이터 조회
    - 차트 데이터 가공
```

**utils.py** - 유틸리티
```python
- 날짜 변환 함수
- 금액 포맷팅
- 유효성 검사
```

---

## 🧪 테스트

프로젝트는 pytest를 사용한 단위 테스트를 포함합니다.

### 테스트 실행

```bash
# 가상환경 활성화 상태에서
pytest tests/

# 더 상세한 출력
pytest tests/ -v

# 특정 테스트 파일만
pytest tests/test_models.py

# 커버리지 확인
pytest tests/ --cov=ledger
```

### 테스트 커버리지

- ✅ Transaction 모델 생성 및 검증
- ✅ 잔액 계산 로직
- ✅ 카테고리별 통계 계산
- ✅ 날짜 변환 및 유효성 검사

---

## 🛠️ 기술 스택

### Frontend
- **Streamlit** - 웹 애플리케이션 프레임워크
- **Plotly** - 인터랙티브 차트 라이브러리

### Backend
- **Python 3.8+** - 프로그래밍 언어
- **Pandas** - 데이터 처리 및 분석
- **yfinance** - Yahoo Finance API 래퍼

### Data Storage
- **CSV** - 로컬 파일 기반 데이터베이스

### Testing
- **pytest** - 단위 테스트 프레임워크

### Development
- **Git** - 버전 관리
- **GitHub** - 소스 코드 호스팅

---

## 💡 주요 특징

### 🎨 깔끔한 코드 구조
- **모듈화**: 기능별로 파일 분리
- **주석**: 초보자도 이해하기 쉬운 한글 주석
- **타입 힌트**: Python Type Hints 사용
- **에러 처리**: 안정적인 예외 처리

### 📊 강력한 데이터 시각화
- **인터랙티브 차트**: Plotly 기반
- **반응형 레이아웃**: 화면 크기에 맞춰 조정
- **실시간 업데이트**: 데이터 변경 시 즉시 반영

### 🔒 데이터 보안
- **로컬 저장**: 개인 재무 데이터를 컴퓨터에 보관
- **외부 전송 없음**: 주식 데이터 외 외부 통신 없음

### 🚀 확장 가능성
- **플러그인 구조**: 새 기능 추가 용이
- **데이터베이스 교체 가능**: CSV → SQLite, PostgreSQL 등
- **API 연동 가능**: 은행 API, 카드 API 연동 가능

---

## 🎓 학습 자료

### Python 기초
- [점프 투 파이썬](https://wikidocs.net/book/1)
- [Python 공식 문서](https://docs.python.org/ko/3/)

### Streamlit
- [Streamlit 공식 문서](https://docs.streamlit.io)
- [Streamlit 30일 챌린지](https://30days.streamlit.app/)

### 데이터 분석
- [Pandas 10분 완성](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Plotly Python](https://plotly.com/python/)

### Git & GitHub
- [Git 입문](https://backlog.com/git-tutorial/kr/)
- [GitHub 가이드](https://guides.github.com/)

---

## 🔧 문제 해결

### 자주 발생하는 문제

#### 1. 가상환경 활성화 오류 (Windows PowerShell)

**증상**: `이 시스템에서 스크립트를 실행할 수 없으므로...`

**해결**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Streamlit 실행 오류

**증상**: `streamlit: command not found`

**해결**:
```bash
# 가상환경이 활성화되어 있는지 확인
# 프롬프트에 (venv)가 표시되어야 함

# 가상환경 활성화 후
pip install --upgrade streamlit
```

#### 3. 주식 데이터 조회 실패

**증상**: `티커에 대한 데이터를 찾을 수 없습니다`

**원인 및 해결**:
- ❌ 잘못된 티커 심볼 → 정확한 티커 확인
- ❌ 인터넷 연결 끊김 → 네트워크 확인
- ❌ yfinance 서버 문제 → 잠시 후 재시도

#### 4. CSV 파일 오류

**증상**: 데이터가 표시되지 않거나 오류 발생

**해결**:
```bash
# data 폴더 확인
ls data/

# 파일이 없다면 자동 생성됨
# 파일이 손상되었다면 삭제 후 재실행
rm data/ledger.csv
streamlit run app.py
```

#### 5. 한글 깨짐 (CSV)

**증상**: CSV 파일을 엑셀에서 열면 한글이 깨짐

**해결**:
- CSV 파일은 UTF-8-BOM 인코딩으로 저장됨
- 엑셀에서 "데이터 > 텍스트/CSV에서" 메뉴 사용
- 또는 Google 스프레드시트 사용

---

## 🚀 향후 개선 계획

### v2.0 계획 기능

- [ ] **예산 관리**: 카테고리별 월 예산 설정
- [ ] **알림 기능**: 예산 초과 시 경고
- [ ] **데이터 백업**: 자동 백업 및 복원
- [ ] **다중 계좌**: 여러 계좌 관리
- [ ] **영수증 스캔**: OCR 기술로 자동 입력
- [ ] **엑셀 내보내기**: 분석용 데이터 추출
- [ ] **반복 거래**: 정기 수입/지출 자동 입력
- [ ] **목표 설정**: 저축 목표 및 진행률
- [ ] **데이터베이스**: SQLite로 성능 개선
- [ ] **사용자 인증**: 다중 사용자 지원

### 기여하기

프로젝트 개선 아이디어가 있으신가요?

1. 이 저장소를 Fork
2. 새 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

---

## 📞 지원 및 문의

### 도움이 필요하신가요?

- 📖 **문서**: 이 README와 SETUP_GUIDE.md 참조
- 🐛 **버그 리포트**: GitHub Issues 활용
- 💡 **기능 제안**: GitHub Discussions 활용
- 📧 **이메일**: [이메일 주소 입력]

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자유롭게 사용, 수정, 배포할 수 있습니다.

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들을 사용합니다:

- [Streamlit](https://streamlit.io/) - 웹 앱 프레임워크
- [Pandas](https://pandas.pydata.org/) - 데이터 분석
- [Plotly](https://plotly.com/) - 데이터 시각화
- [yfinance](https://github.com/ranaroussi/yfinance) - 주식 데이터

---

## 📊 프로젝트 통계

![GitHub stars](https://img.shields.io/github/stars/yourusername/mini-ledger?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/mini-ledger?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/mini-ledger?style=social)

---

<div align="center">

**⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요! ⭐**

Made with ❤️ using Python & Streamlit

[맨 위로 이동](#-나만의-미니-가계부-mini-ledger)

</div>

#