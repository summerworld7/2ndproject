import streamlit as st
import pandas as pd
import plotly.express as px
from astral.sun import sun
from astral import LocationInfo
import datetime

# 한국(서울) 위치 정보
city = LocationInfo("Seoul", "South Korea", "Asia/Seoul", 37.5665, 126.9780)

# 1년치 낮 길이 계산
dates = pd.date_range("2025-01-01", "2025-12-31")
day_lengths = []

for date in dates:
    s = sun(city.observer, date=date)
    daylight = (s["sunset"] - s["sunrise"]).total_seconds() / 3600  # 시간 단위
    day_lengths.append(daylight)

df = pd.DataFrame({"Date": dates, "Daylight Hours": day_lengths})

# 그래프 출력
fig = px.line(df, x="Date", y="Daylight Hours", title="서울 낮 길이 변화 (2025)")
st.plotly_chart(fig)
