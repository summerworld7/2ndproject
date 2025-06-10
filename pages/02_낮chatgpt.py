import streamlit as st
import pandas as pd
import plotly.express as px
from astral.sun import sun
from astral import LocationInfo
import datetime

# 한국 서울 위치
city = LocationInfo("Seoul", "South Korea", "Asia/Seoul", 37.5665, 126.9780)

# 날짜 생성
dates = pd.date_range("2025-01-01", "2025-12-31")
day_lengths = []
formatted_lengths = []

for date in dates:
    s = sun(city.observer, date=date)
    daylight = (s["sunset"] - s["sunrise"]).total_seconds() / 3600  # 시간 (소수)
    day_lengths.append(daylight)

    # 시:분 포맷으로 변환
    hours = int(daylight)
    minutes = int((daylight - hours) * 60)
    formatted = f"{hours:02d}:{minutes:02d}"
    formatted_lengths.append(formatted)

# 데이터프레임 구성
df = pd.DataFrame({
    "Date": dates,
    "Daylight Hours": day_lengths,
    "Daylight (hh:mm)": formatted_lengths
})

# Plotly 그래프 생성
fig = px.line(
    df,
    x="Date",
    y="Daylight Hours",
    hover_data={"Daylight (hh:mm)": True, "Daylight Hours": False},
    title="서울 낮 길이 변화 (2025)"
)
fig.update_yaxes(title_text="낮 길이 (시간)")  # y축 라벨

st.plotly_chart(fig)
