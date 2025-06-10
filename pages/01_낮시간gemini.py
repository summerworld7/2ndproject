import streamlit as st
import pandas as pd
import plotly.express as px
from astral.sun import sun
from astral import LocationInfo
import datetime

st.set_page_config(layout="wide") # 페이지 전체 너비 사용

st.title("☀️ 한국(서울)의 낮 길이 변화 시각화")
st.write("원하는 기간을 선택하여 서울의 낮 길이 변화를 확인해보세요.")

# 한국(서울) 위치 정보
city = LocationInfo("Seoul", "South Korea", "Asia/Seoul", 37.5665, 126.9780)

# 날짜 선택 위젯
col1, col2 = st.columns(2)
with col1:
    # Default to current year for more relevance
    current_year = datetime.date.today().year
    start_date = st.date_input("시작 날짜", datetime.date(current_year, 1, 1))
with col2:
    end_date = st.date_input("종료 날짜", datetime.date(current_year, 12, 31))

# 날짜 유효성 검사
if start_date > end_date:
    st.error("⚠️ 시작 날짜는 종료 날짜보다 빠르거나 같아야 합니다.")
else:
    # 선택된 기간의 낮 길이 계산
    dates = pd.date_range(start_date, end_date)
    day_lengths = []

    for date in dates:
        s = sun(city.observer, date=date)
        # Ensure both sunrise and sunset exist and are valid for the calculation
        if s["sunrise"] and s["sunset"]:
            # Calculate the absolute difference to guarantee a positive duration
            daylight_seconds = abs((s["sunset"] - s["sunrise"]).total_seconds())
            daylight_hours = daylight_seconds / 3600  # Convert to hours
            day_lengths.append(daylight_hours)
        else:
            # Handle cases where sunrise or sunset might not occur (e.g., polar regions)
            day_lengths.append(None)

    df = pd.DataFrame({"Date": dates, "Daylight Hours": day_lengths})
    df.dropna(inplace=True) # Remove rows where daylight hours couldn't be calculated

    # 그래프 출력
    if not df.empty:
        # Dynamically adjust title based on selected dates
        title_text = f"서울 낮 길이 변화 ({start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')})"
        fig = px.line(df, x="Date", y="Daylight Hours",
                      title=title_text,
                      labels={"Daylight Hours": "낮 길이 (시간)", "Date": "날짜"},
                      hover_data={"Date": "|%Y년 %m월 %d일"}) # Customize hover tooltip date format
        fig.update_traces(mode='lines+markers', marker_size=3) # Add lines and small markers
        fig.update_layout(xaxis_title="날짜", yaxis_title="낮 길이 (시간)",
                          hovermode="x unified") # Unify hover tooltips along the x-axis
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("선택된 기간 동안 낮 길이 데이터를 계산할 수 없습니다. 날짜를 다시 확인해주세요.")

st.markdown("---")
st.info("이 앱은 'astral' 라이브러리를 사용하여 천문학적인 낮 길이를 계산하며, **항상 양수 값으로 표시**됩니다.")
