import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from typing import Dict, List
import yfinance as yf

# 페이지 설정
st.set_page_config(
    page_title="스마트 가계부",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 스테이트 초기화
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'stocks' not in st.session_state:
    st.session_state.stocks = []
if 'real_estate' not in st.session_state:
    st.session_state.real_estate = []
if 'fixed_expenses' not in st.session_state:
    st.session_state.fixed_expenses = []

# 데이터 저장/로드 함수
def save_data():
    """데이터를 JSON 파일로 저장"""
    data = {
        'expenses': st.session_state.expenses,
        'stocks': st.session_state.stocks,
        'real_estate': st.session_state.real_estate,
        'fixed_expenses': st.session_state.fixed_expenses
    }
    with open('budget_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data():
    """JSON 파일에서 데이터 로드"""
    if os.path.exists('budget_data.json'):
        with open('budget_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            st.session_state.expenses = data.get('expenses', [])
            st.session_state.stocks = data.get('stocks', [])
            st.session_state.real_estate = data.get('real_estate', [])
            st.session_state.fixed_expenses = data.get('fixed_expenses', [])

# 주식 가격 조회 함수
def get_stock_price(ticker: str, start_date: str = None):
    """Yahoo Finance에서 주식 가격 조회"""
    try:
        stock = yf.Ticker(ticker)
        if start_date:
            hist = stock.history(start=start_date)
        else:
            hist = stock.history(period="1mo")
        
        if len(hist) > 0:
            current_price = hist['Close'].iloc[-1]
            start_price = hist['Close'].iloc[0]
            return {
                'current_price': current_price,
                'start_price': start_price,
                'change_percent': ((current_price - start_price) / start_price) * 100,
                'history': hist
            }
    except Exception as e:
        st.error(f"주식 가격 조회 실패: {e}")
    return None

# 총 자산 계산 함수
def calculate_total_assets():
    """총 자산 계산"""
    total = 0
    
    # 주식 자산
    for stock in st.session_state.stocks:
        ticker = stock['ticker']
        quantity = stock['quantity']
        purchase_date = stock['purchase_date']
        
        price_data = get_stock_price(ticker, purchase_date)
        if price_data:
            total += price_data['current_price'] * quantity
    
    # 부동산 자산
    for estate in st.session_state.real_estate:
        total += estate['current_value']
    
    return total

# 메인 앱
def main():
    # 데이터 로드
    load_data()
    
    st.title("💰 스마트 가계부")
    st.markdown("---")
    
    # 사이드바 메뉴
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["📊 대시보드", "📈 주식 투자", "🏠 부동산", "📅 일별 지출", "⚙️ 고정지출 관리"]
    )
    
    if menu == "📊 대시보드":
        show_dashboard()
    elif menu == "📈 주식 투자":
        show_stock_management()
    elif menu == "🏠 부동산":
        show_real_estate_management()
    elif menu == "📅 일별 지출":
        show_daily_expenses()
    elif menu == "⚙️ 고정지출 관리":
        show_fixed_expenses()

def show_dashboard():
    """대시보드 페이지"""
    st.header("📊 자산 현황 대시보드")
    
    col1, col2, col3 = st.columns(3)
    
    # 총 자산
    total_assets = calculate_total_assets()
    with col1:
        st.metric("총 자산", f"₩{total_assets:,.0f}")
    
    # 주식 자산
    stock_value = 0
    for stock in st.session_state.stocks:
        price_data = get_stock_price(stock['ticker'], stock['purchase_date'])
        if price_data:
            stock_value += price_data['current_price'] * stock['quantity']
    
    with col2:
        st.metric("주식 자산", f"₩{stock_value:,.0f}")
    
    # 부동산 자산
    estate_value = sum([e['current_value'] for e in st.session_state.real_estate])
    with col3:
        st.metric("부동산 자산", f"₩{estate_value:,.0f}")
    
    st.markdown("---")
    
    # 자산 구성 파이 차트
    if stock_value > 0 or estate_value > 0:
        st.subheader("자산 구성")
        fig = go.Figure(data=[go.Pie(
            labels=['주식', '부동산'],
            values=[stock_value, estate_value],
            hole=.3
        )])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # 월별 지출 그래프
    if st.session_state.expenses:
        st.subheader("월별 지출 추이")
        df_expenses = pd.DataFrame(st.session_state.expenses)
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
        df_expenses['month'] = df_expenses['date'].dt.to_period('M').astype(str)
        
        monthly_expenses = df_expenses.groupby('month')['amount'].sum().reset_index()
        
        fig = px.bar(monthly_expenses, x='month', y='amount', 
                     labels={'month': '월', 'amount': '지출액'},
                     color='amount')
        st.plotly_chart(fig, use_container_width=True)

def show_stock_management():
    """주식 투자 관리 페이지"""
    st.header("📈 주식 투자 관리")
    
    tab1, tab2 = st.tabs(["주식 추가", "포트폴리오"])
    
    with tab1:
        st.subheader("새 주식 추가")
        
        col1, col2 = st.columns(2)
        with col1:
            ticker = st.text_input("티커 심볼 (예: 005930.KS for 삼성전자)", 
                                   help="미국 주식은 AAPL, GOOGL 등, 한국 주식은 005930.KS 형식")
            quantity = st.number_input("수량", min_value=1, value=1)
        
        with col2:
            purchase_date = st.date_input("매수일", value=datetime.now())
            purchase_price = st.number_input("매수가", min_value=0.0, value=0.0)
        
        if st.button("주식 추가"):
            if ticker:
                new_stock = {
                    'ticker': ticker,
                    'quantity': quantity,
                    'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                    'purchase_price': purchase_price
                }
                st.session_state.stocks.append(new_stock)
                save_data()
                st.success(f"{ticker} 주식이 추가되었습니다!")
                st.rerun()
    
    with tab2:
        st.subheader("보유 주식 포트폴리오")
        
        if not st.session_state.stocks:
            st.info("보유 중인 주식이 없습니다.")
        else:
            for idx, stock in enumerate(st.session_state.stocks):
                with st.expander(f"{stock['ticker']} - {stock['quantity']}주"):
                    price_data = get_stock_price(stock['ticker'], stock['purchase_date'])
                    
                    if price_data:
                        col1, col2, col3, col4 = st.columns(4)
                        
                        current_value = price_data['current_price'] * stock['quantity']
                        purchase_value = stock['purchase_price'] * stock['quantity']
                        profit_loss = current_value - purchase_value
                        profit_loss_percent = (profit_loss / purchase_value) * 100 if purchase_value > 0 else 0
                        
                        with col1:
                            st.metric("현재가", f"₩{price_data['current_price']:,.2f}")
                        with col2:
                            st.metric("평가금액", f"₩{current_value:,.0f}")
                        with col3:
                            st.metric("수익/손실", f"₩{profit_loss:,.0f}", 
                                     delta=f"{profit_loss_percent:.2f}%")
                        with col4:
                            st.metric("수익률", f"{price_data['change_percent']:.2f}%")
                        
                        # 가격 추이 그래프
                        if not price_data['history'].empty:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=price_data['history'].index,
                                y=price_data['history']['Close'],
                                mode='lines',
                                name='종가'
                            ))
                            fig.update_layout(
                                title=f"{stock['ticker']} 가격 추이",
                                xaxis_title="날짜",
                                yaxis_title="가격",
                                height=300
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    if st.button(f"삭제", key=f"delete_stock_{idx}"):
                        st.session_state.stocks.pop(idx)
                        save_data()
                        st.rerun()

def show_real_estate_management():
    """부동산 관리 페이지"""
    st.header("🏠 부동산 관리")
    
    tab1, tab2 = st.tabs(["부동산 추가", "보유 부동산"])
    
    with tab1:
        st.subheader("새 부동산 추가")
        
        col1, col2 = st.columns(2)
        with col1:
            property_name = st.text_input("부동산 이름")
            property_type = st.selectbox("유형", ["아파트", "오피스텔", "빌라", "단독주택", "상가", "토지"])
            purchase_date = st.date_input("취득일")
        
        with col2:
            purchase_price = st.number_input("취득가", min_value=0, value=0)
            current_value = st.number_input("현재 시세", min_value=0, value=0)
            location = st.text_input("위치")
        
        if st.button("부동산 추가"):
            if property_name:
                new_estate = {
                    'name': property_name,
                    'type': property_type,
                    'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                    'purchase_price': purchase_price,
                    'current_value': current_value,
                    'location': location
                }
                st.session_state.real_estate.append(new_estate)
                save_data()
                st.success(f"{property_name} 부동산이 추가되었습니다!")
                st.rerun()
    
    with tab2:
        st.subheader("보유 부동산 목록")
        
        if not st.session_state.real_estate:
            st.info("보유 중인 부동산이 없습니다.")
        else:
            for idx, estate in enumerate(st.session_state.real_estate):
                with st.expander(f"{estate['name']} ({estate['type']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    profit_loss = estate['current_value'] - estate['purchase_price']
                    profit_loss_percent = (profit_loss / estate['purchase_price']) * 100 if estate['purchase_price'] > 0 else 0
                    
                    with col1:
                        st.metric("취득가", f"₩{estate['purchase_price']:,.0f}")
                    with col2:
                        st.metric("현재 시세", f"₩{estate['current_value']:,.0f}")
                    with col3:
                        st.metric("평가손익", f"₩{profit_loss:,.0f}", 
                                 delta=f"{profit_loss_percent:.2f}%")
                    
                    st.write(f"**위치:** {estate['location']}")
                    st.write(f"**취득일:** {estate['purchase_date']}")
                    
                    if st.button(f"삭제", key=f"delete_estate_{idx}"):
                        st.session_state.real_estate.pop(idx)
                        save_data()
                        st.rerun()

def show_daily_expenses():
    """일별 지출 기록 페이지"""
    st.header("📅 일별 지출 기록")
    
    tab1, tab2 = st.tabs(["지출 추가", "달력 보기"])
    
    with tab1:
        st.subheader("새 지출 추가")
        
        col1, col2 = st.columns(2)
        with col1:
            expense_date = st.date_input("날짜", value=datetime.now())
            category = st.selectbox("카테고리", 
                                   ["식비", "교통비", "쇼핑", "문화생활", "의료", "교육", "기타"])
        
        with col2:
            amount = st.number_input("금액", min_value=0, value=0)
            expense_type = st.radio("지출 유형", ["변동지출", "고정지출"])
        
        description = st.text_input("설명")
        
        if st.button("지출 추가"):
            new_expense = {
                'date': expense_date.strftime('%Y-%m-%d'),
                'category': category,
                'amount': amount,
                'type': expense_type,
                'description': description
            }
            st.session_state.expenses.append(new_expense)
            save_data()
            st.success("지출이 추가되었습니다!")
            st.rerun()
    
    with tab2:
        st.subheader("월별 지출 달력")
        
        # 월 선택
        selected_month = st.date_input("조회할 월", value=datetime.now())
        
        if st.session_state.expenses:
            df_expenses = pd.DataFrame(st.session_state.expenses)
            df_expenses['date'] = pd.to_datetime(df_expenses['date'])
            
            # 선택한 월의 지출만 필터링
            month_expenses = df_expenses[
                (df_expenses['date'].dt.year == selected_month.year) &
                (df_expenses['date'].dt.month == selected_month.month)
            ]
            
            if not month_expenses.empty:
                # 일별 총액
                daily_total = month_expenses.groupby('date')['amount'].sum().reset_index()
                
                st.subheader(f"{selected_month.strftime('%Y년 %m월')} 지출 내역")
                
                for _, row in daily_total.iterrows():
                    date_str = row['date'].strftime('%Y-%m-%d')
                    day_expenses = month_expenses[month_expenses['date'] == row['date']]
                    
                    with st.expander(f"{date_str} - 총 ₩{row['amount']:,.0f}"):
                        for _, expense in day_expenses.iterrows():
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                st.write(f"**{expense['category']}** - {expense['description']}")
                            with col2:
                                st.write(f"₩{expense['amount']:,.0f}")
                            with col3:
                                badge_color = "🔴" if expense['type'] == "고정지출" else "🟢"
                                st.write(f"{badge_color} {expense['type']}")
                
                # 카테고리별 지출
                st.markdown("---")
                st.subheader("카테고리별 지출")
                category_total = month_expenses.groupby('category')['amount'].sum().reset_index()
                
                fig = px.pie(category_total, values='amount', names='category', 
                            title='카테고리별 지출 비중')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"{selected_month.strftime('%Y년 %m월')}에는 지출 내역이 없습니다.")

def show_fixed_expenses():
    """고정지출 관리 페이지"""
    st.header("⚙️ 고정지출 관리")
    
    tab1, tab2 = st.tabs(["고정지출 설정", "지출 분석"])
    
    with tab1:
        st.subheader("고정지출 항목 추가")
        
        col1, col2 = st.columns(2)
        with col1:
            expense_name = st.text_input("항목명 (예: 월세, 통신비)")
            amount = st.number_input("금액", min_value=0, value=0)
        
        with col2:
            category = st.selectbox("카테고리", 
                                   ["주거비", "통신비", "보험료", "구독료", "기타"])
            due_day = st.number_input("납부일", min_value=1, max_value=31, value=1)
        
        if st.button("고정지출 추가"):
            new_fixed = {
                'name': expense_name,
                'amount': amount,
                'category': category,
                'due_day': due_day
            }
            st.session_state.fixed_expenses.append(new_fixed)
            save_data()
            st.success("고정지출이 추가되었습니다!")
            st.rerun()
        
        st.markdown("---")
        st.subheader("등록된 고정지출")
        
        if st.session_state.fixed_expenses:
            total_fixed = sum([f['amount'] for f in st.session_state.fixed_expenses])
            st.metric("월 고정지출 합계", f"₩{total_fixed:,.0f}")
            
            for idx, fixed in enumerate(st.session_state.fixed_expenses):
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                with col1:
                    st.write(f"**{fixed['name']}**")
                with col2:
                    st.write(f"₩{fixed['amount']:,.0f}")
                with col3:
                    st.write(f"매월 {fixed['due_day']}일")
                with col4:
                    if st.button("삭제", key=f"delete_fixed_{idx}"):
                        st.session_state.fixed_expenses.pop(idx)
                        save_data()
                        st.rerun()
        else:
            st.info("등록된 고정지출이 없습니다.")
    
    with tab2:
        st.subheader("지출 분석 및 절약 제안")
        
        if st.session_state.expenses:
            df_expenses = pd.DataFrame(st.session_state.expenses)
            
            # 최근 3개월 데이터
            three_months_ago = datetime.now() - timedelta(days=90)
            df_expenses['date'] = pd.to_datetime(df_expenses['date'])
            recent_expenses = df_expenses[df_expenses['date'] >= three_months_ago]
            
            # 고정지출 vs 변동지출
            type_summary = recent_expenses.groupby('type')['amount'].sum().reset_index()
            
            col1, col2 = st.columns(2)
            with col1:
                fixed_total = type_summary[type_summary['type'] == '고정지출']['amount'].sum() if not type_summary.empty else 0
                st.metric("고정지출 (최근 3개월)", f"₩{fixed_total:,.0f}")
            
            with col2:
                variable_total = type_summary[type_summary['type'] == '변동지출']['amount'].sum() if not type_summary.empty else 0
                st.metric("변동지출 (최근 3개월)", f"₩{variable_total:,.0f}")
            
            # 절약 제안
            st.markdown("---")
            st.subheader("💡 절약 제안")
            
            # 변동지출 카테고리별 분석
            variable_expenses = recent_expenses[recent_expenses['type'] == '변동지출']
            if not variable_expenses.empty:
                category_avg = variable_expenses.groupby('category')['amount'].mean().reset_index()
                category_avg = category_avg.sort_values('amount', ascending=False)
                
                st.write("**변동지출이 많은 카테고리:**")
                for _, row in category_avg.head(3).iterrows():
                    st.warning(f"📌 **{row['category']}**: 평균 ₩{row['amount']:,.0f} - 절약 가능한 항목을 검토해보세요!")
            
            # 월평균 지출
            monthly_avg = recent_expenses.groupby(recent_expenses['date'].dt.to_period('M'))['amount'].sum().mean()
            st.info(f"📊 최근 3개월 월평균 지출: ₩{monthly_avg:,.0f}")
            
        else:
            st.info("지출 데이터가 없습니다. 지출을 기록해주세요!")

if __name__ == "__main__":
    main()
