import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 스트림릿 앱 제목
st.title("글로벌 시총 TOP 10 기업의 최근 3년 주가 변화")

# 시총 상위 10개 기업의 티커 (2025 기준 예시, 필요 시 업데이트 가능)
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

# 기간 설정 (최근 3년)
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)

# 데이터 가져오기
st.write(f"데이터 기간: {start_date.date()} ~ {end_date.date()}")

fig = go.Figure()

for name, ticker in companies.items():
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            fig.add_trace(go.Scatter(x=data.index, y=data["Adj Close"], name=name))
    except Exception as e:
        st.warning(f"{name}의 데이터를 가져오지 못했습니다: {e}")

# 그래프 옵션 설정
fig.update_layout(
    title="글로벌 시가총액 상위 10개 기업의 주가 변화 (최근 3년)",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
