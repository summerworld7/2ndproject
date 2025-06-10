import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.title("글로벌 시가총액 TOP 10 기업의 최근 3년 주가 변화")

companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Amazon": "AMZN",
    "Alphabet (Google)": "GOOGL",
    "Berkshire Hathaway": "BRK-B",
    "Meta Platforms": "META",
    "Eli Lilly": "LLY",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)

st.write(f"데이터 기간: {start_date.date()} ~ {end_date.date()}")

fig = go.Figure()

for name, ticker in companies.items():
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        if not data.empty:
            data = data.dropna()  # 결측치 제거
            price_col = "Adj Close" if "Adj Close" in data.columns else "Close"
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[price_col],
                mode="lines",
                name=name
            ))
    except Exception as e:
        st.warning(f"{name}의 데이터를 가져오지 못했습니다: {e}")

fig
