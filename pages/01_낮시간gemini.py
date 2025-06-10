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
    dates = []
    day_lengths = []

    current_date = start_date
    while current_date <= end_date:
        s = sun(city.observer, date=current_date)
        
        # 일출/일몰 시간이 모두 유효한지 확인
        if s["sunrise"] and s["sunset"]:
            # sunset이 sunrise보다 늦으면 양수, 빠르면 음수가 나올 수 있습니다.
            # 서울에서는 6월이 가장 길고 12월이 가장 짧아야 하므로
            # 이 차이 값 자체가 올바른 낮 길이를 나타내야 합니다.
            # abs()를 제거하여 원래의 차이 값을 확인합니다.
            daylight_seconds = (s["sunset"] - s["sunrise"]).total_seconds()
            daylight_hours = daylight_seconds / 3600  # 시간 단위로 변환
            
            dates.append(current_date)
            day_lengths.append(daylight_hours)
        else:
            # 극지방처럼 일출/일몰이 없는 경우를 대비하지만, 서울에는 해당 없음.
            # 이 경우 데이터를 추가하지 않아 자동으로 NaN으로 처리됩니다.
            pass
        
        current_date += datetime.timedelta(days=1)


    df = pd.DataFrame({"Date": dates, "Daylight Hours": day_lengths})
    # 필요하다면 df.dropna(inplace=True)를 추가하여 None 값을 제거할 수 있습니다.
    # 하지만 위 루프에서 None을 추가하지 않으므로 필요 없을 것입니다.

    # 그래프 출력
    if not df.empty:
        # Dynamically adjust title based on selected dates
        title_text = f"서울 낮 길이 변화 ({start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')})"
        fig = px.line(df, x="Date", y="Daylight Hours",
                      title=title_text,
                      labels={"Daylight Hours": "낮 길이 (시간)", "Date": "날짜"},
                      hover_data={"Date": "|%Y년 %m월 %d일"}) # Customize hover tooltip date format
        fig.update_traces(mode='lines') # 선만 표시, 마커는 낮 길이 변화 추세에 따라 너무 많을 수 있음
        fig.update_layout(xaxis_title="날짜", yaxis_title="낮 길이 (시간)",
                          hovermode="x unified") # Unify hover tooltips along the x-axis
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("선택된 기간 동안 낮 길이 데이터를 계산할 수 없습니다. 날짜를 다시 확인해주세요.")

st.markdown("---")
st.info("이 앱은 'astral' 라이브러리를 사용하여 천문학적인 낮 길이를 계산합니다. 낮 길이는 6월 (하지 부근)에 가장 길고 12월 (동지 부근)에 가장 짧게 나타납니다.")
