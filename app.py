"""
나만의 미니 가계부 (Mini Ledger)
Streamlit을 사용한 가계부 웹 애플리케이션
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly as go
from datetime import datetime, date
from ledger import (
    Transaction,
    LedgerRepository,
    LedgerService,
    StockService,
    format_currency
)

# 페이지 설정
st.set_page_config(
    page_title="나만의 미니 가계부",
    page_icon="💰",
    layout="wide"
)

# Repository와 Service 초기화
st.cache_resource
def get_services():
    """
    Repository와 Service 객체를 생성하고 캐싱합니다.
    @st.cache_resource 데코레이터로 앱이 재실행되어도 객체가 유지됩니다.
    """
    repo = LedgerRepository('data/ledger.csv')
    ledger_service = LedgerService(repo)
    return repo, ledger_service

repository, ledger_service = get_services()

# 앱 제목
st.title("💰 나만의 미니 가계부")
st.markdown("---")

# 사이드바: 메뉴 선택
menu = st.sidebar.selectbox(
    "메뉴",
    ["📝 거래 입력", "📊 가계부 조회", "📈 통계", "📉 주식 차트"]
)

# ========== 1. 거래 입력 메뉴 ==========
if menu == "📝 거래 입력":
    st.header("거래 입력")
    
    # 두 개의 컬럼으로 나누어 입력 폼 구성
    col1, col2 = st.columns(2)
    
    with col1:
        # 날짜 선택
        transaction_date = st.date_input(
            "날짜",
            value=date.today(),
            help="거래가 발생한 날짜를 선택하세요"
        )
        
        # 거래 유형 선택 (수입/지출)
        transaction_type = st.selectbox(
            "거래 유형",
            ["수입", "지출"]
        )
        
        # 카테고리 입력
        if transaction_type == "수입":
            default_categories = ["급여", "보너스", "용돈", "기타"]
        else:
            default_categories = ["식비", "교통비", "문화생활", "쇼핑", "공과금", "기타"]
        
        category = st.selectbox(
            "카테고리",
            default_categories
        )
    
    with col2:
        # 금액 입력
        amount = st.number_input(
            "금액 (원)",
            min_value=0,
            value=0,
            step=1000,
            help="거래 금액을 입력하세요"
        )
        
        # 설명 입력
        description = st.text_area(
            "설명 (선택사항)",
            height=100,
            placeholder="거래에 대한 추가 설명을 입력하세요"
        )
    
    # 저장 버튼
    if st.button("💾 저장", type="primary", use_container_width=True):
        if amount <= 0:
            st.error("금액은 0보다 커야 합니다.")
        else:
            try:
                # Transaction 객체 생성
                transaction = Transaction(
                    date=datetime.combine(transaction_date, datetime.min.time()),
                    category=category,
                    amount=amount,
                    transaction_type=transaction_type,
                    description=description
                )
                
                # 데이터베이스에 저장
                repository.save_transaction(transaction)
                
                st.success(f"✅ {transaction_type} {format_currency(amount)}이(가) 저장되었습니다!")
                
            except Exception as e:
                st.error(f"저장 중 오류가 발생했습니다: {str(e)}")

# ========== 2. 가계부 조회 메뉴 ==========
elif menu == "📊 가계부 조회":
    st.header("가계부 조회")
    
    # 조회 방법 선택
    view_type = st.radio(
        "조회 방법",
        ["일별 조회", "기간별 조회", "전체 조회"],
        horizontal=True
    )
    
    transactions = []
    
    # 일별 조회
    if view_type == "일별 조회":
        selected_date = st.date_input("날짜 선택", value=date.today())
        selected_datetime = datetime.combine(selected_date, datetime.min.time())
        transactions = ledger_service.get_daily_transactions(selected_datetime)
        st.subheader(f"📅 {selected_date} 거래 내역")
    
    # 기간별 조회
    elif view_type == "기간별 조회":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("시작 날짜", value=date.today().replace(day=1))
        with col2:
            end_date = st.date_input("종료 날짜", value=date.today())
        
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        transactions = repository.get_transactions_by_date_range(start_datetime, end_datetime)
        st.subheader(f"📅 {start_date} ~ {end_date} 거래 내역")
    
    # 전체 조회
    else:
        transactions = repository.get_all_transactions()
        st.subheader("📅 전체 거래 내역")
    
    # 거래 내역이 있는 경우
    if transactions:
        # 요약 정보 표시
        balance_info = ledger_service.calculate_balance(transactions)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 수입", format_currency(balance_info['income']))
        with col2:
            st.metric("총 지출", format_currency(balance_info['expense']))
        with col3:
            balance_color = "normal" if balance_info['balance'] >= 0 else "inverse"
            st.metric("잔액", format_currency(balance_info['balance']))
        
        st.markdown("---")
        
        # 거래 내역 테이블로 표시
        data = []
        for t in transactions:
            data.append({
                '날짜': t.date.strftime('%Y-%m-%d'),
                '구분': t.transaction_type,
                '카테고리': t.category,
                '금액': format_currency(t.amount),
                '설명': t.description
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    else:
        st.info("조회된 거래 내역이 없습니다.")

# ========== 3. 통계 메뉴 ==========
elif menu == "📈 통계":
    st.header("통계")
    
    # 월 선택
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox(
            "연도",
            range(datetime.now().year, 2020, -1),
            index=0
        )
    with col2:
        selected_month = st.selectbox(
            "월",
            range(1, 13),
            index=datetime.now().month - 1
        )
    
    # 월별 요약 정보 가져오기
    summary = ledger_service.get_monthly_summary(selected_year, selected_month)
    
    st.subheader(f"📊 {selected_year}년 {selected_month}월 통계")
    
    # 요약 정보 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 수입", format_currency(summary['total_income']))
    with col2:
        st.metric("총 지출", format_currency(summary['total_expense']))
    with col3:
        st.metric("잔액", format_currency(summary['balance']))
    with col4:
        st.metric("거래 건수", f"{summary['transaction_count']}건")
    
    st.markdown("---")
    
    # 카테고리별 통계를 그래프로 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 수입 카테고리별")
        if summary['income_by_category']:
            # 파이 차트 생성
            fig = go.Figure(data=[go.Pie(
                labels=list(summary['income_by_category'].keys()),
                values=list(summary['income_by_category'].values()),
                hole=0.3
            )])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # 상세 내역
            for category, amount in summary['income_by_category'].items():
                st.write(f"- {category}: {format_currency(amount)}")
        else:
            st.info("수입 데이터가 없습니다.")
    
    with col2:
        st.subheader("💸 지출 카테고리별")
        if summary['expense_by_category']:
            # 파이 차트 생성
            fig = go.Figure(data=[go.Pie(
                labels=list(summary['expense_by_category'].keys()),
                values=list(summary['expense_by_category'].values()),
                hole=0.3
            )])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # 상세 내역
            for category, amount in summary['expense_by_category'].items():
                st.write(f"- {category}: {format_currency(amount)}")
        else:
            st.info("지출 데이터가 없습니다.")

# ========== 4. 주식 차트 메뉴 ==========
elif menu == "📉 주식 차트":
    st.header("주식 차트")
    
    st.info("💡 미국 주식 티커를 입력하세요 (예: AAPL, TSLA, MSFT, GOOGL)")
    
    # 입력 폼
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker = st.text_input(
            "티커 심볼",
            placeholder="예: AAPL",
            help="주식 티커 심볼을 입력하세요"
        )
    with col2:
        period = st.selectbox(
            "기간",
            ["1d", "5d", "1mo", "3mo", "6mo", "1y"],
            index=2
        )
    
    if st.button("📊 차트 보기", type="primary"):
        if not ticker:
            st.warning("티커 심볼을 입력해주세요.")
        else:
            with st.spinner(f"{ticker} 데이터를 불러오는 중..."):
                # 주식 데이터 가져오기
                df, success, message = StockService.get_stock_data(ticker, period)
                
                if success:
                    st.success(message)
                    
                    # 주식 정보 표시
                    info = StockService.get_stock_info(ticker)
                    st.subheader(f"📈 {info.get('name', ticker)}")
                    
                    if 'current_price' in info and info['current_price'] != 'N/A':
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("현재가", f"${info['current_price']:.2f}")
                        with col2:
                            if info.get('sector') != 'N/A':
                                st.write(f"**섹터:** {info['sector']}")
                        with col3:
                            if info.get('currency'):
                                st.write(f"**통화:** {info['currency']}")
                    
                    st.markdown("---")
                    
                    # 캔들스틱 차트 생성
                    fig = go.Figure(data=[go.Candlestick(
                        x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name=ticker
                    )])
                    
                    fig.update_layout(
                        title=f"{ticker} 주가 차트",
                        yaxis_title="가격 (USD)",
                        xaxis_title="날짜",
                        height=500,
                        xaxis_rangeslider_visible=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 거래량 차트
                    fig_volume = go.Figure(data=[go.Bar(
                        x=df['Date'],
                        y=df['Volume'],
                        name='거래량'
                    )])
                    
                    fig_volume.update_layout(
                        title="거래량",
                        yaxis_title="거래량",
                        xaxis_title="날짜",
                        height=300
                    )
                    
                    st.plotly_chart(fig_volume, use_container_width=True)
                    
                    # 상세 데이터 테이블
                    with st.expander("📋 상세 데이터 보기"):
                        st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.error(message)

# 사이드바: 추가 정보
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ 정보")
st.sidebar.info(
    """
    **나만의 미니 가계부**
    
    - 📝 거래 입력: 수입/지출 기록
    - 📊 가계부 조회: 일별/기간별 조회
    - 📈 통계: 월별 통계 및 차트
    - 📉 주식 차트: 실시간 주가 조회
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")