import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pyorbital.orbital import Orbital # pyorbital 대신 다른 천문 라이브러리도 고려 가능
import plotly.express as px

# 한국의 위도/경도 (서울 기준)
LATITUDE = 37.5665
LONGITUDE = 126.9780

def get_daylight_hours(date, lat, lon):
    # pyorbital을 사용한 일출/일몰 시간 계산 (대체 라이브러리 사용 가능)
    # 실제로는 pyorbital이 위성 궤도에 특화되어 있어, 다른 천문 라이브러리가 더 적합할 수 있습니다.
    # 예를 들어, `astral` 라이브러리가 일출/일몰 계산에 더 직관적입니다.
    # 여기서는 개념적인 예시를 위해 pyorbital을 언급했지만, astral을 더 추천합니다.

    # 임시 함수: 실제 일출/일몰 계산 로직을 여기에 구현
    # 예시: 12시간 낮 길이를 가정
    return 12

st.title("한국의 낮 길이 변화")

start_date = st.date_input("시작 날짜", datetime(2024, 1, 1))
end_date = st.date_input("종료 날짜", datetime(2024, 12, 31))

if start_date <= end_date:
    date_list = []
    daylight_hours_list = []

    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        # 실제 낮 길이 계산 로직을 여기에 넣습니다.
        # 예시: get_daylight_hours(current_date, LATITUDE, LONGITUDE)
        daylight_hours_list.append(get_daylight_hours(current_date, LATITUDE, LONGITUDE)) # 실제 계산된 값으로 대체

        current_date += timedelta(days=1)

    df = pd.DataFrame({
        '날짜': date_list,
        '낮 길이 (시간)': daylight_hours_list
    })

    fig = px.line(df, x='날짜', y='낮 길이 (시간)', title='한국의 낮 길이 변화')
    st.plotly_chart(fig)
else:
    st.error("시작 날짜는 종료 날짜보다 빠르거나 같아야 합니다.")
