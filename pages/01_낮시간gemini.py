import streamlit as st
import pandas as pd
import plotly.express as px
from astral.sun import sun
from astral import LocationInfo
import datetime

st.set_page_config(layout="wide") # 페이지 전체 너비 사용

st.title("☀️ 한국(서울)의 낮 길이 변화 시각화")
st.write("원하는 기간을 선택하여 서울의 낮 길이 변화를 확인해보세요.")
st.warning("⚠️ **참고:** 현재 코드는 요청에 따라 일출 시간에서 일몰 시간을 빼서 낮 길이를 계산하고 있습니다. 이는 일반적인 낮 길이 계산 방식과 다르며, 예상과 다른 결과가 나올 수 있습니다.")

# 한국(서울) 위치 정보
city = LocationInfo("Seoul", "South Korea", "Asia/Seoul", 37.5665, 126.9780)

# 날짜 선택 위젯
col1, col2 = st.columns(2)
with col1:
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
        
        if s["sunrise"] and s["sunset"]:
            # 요청에 따라 sunrise - sunset으로 변경
            # 일반적으로 이 값은 음수가 될 것입니다.
            daylight_seconds = (s["sunrise"] - s["sunset"]).total_seconds()
            daylight_hours = daylight_seconds / 3600  # 시간 단위로 변환
            
            dates.append(current_date)
            day_lengths.append(daylight_hours)
        else:
            pass # 일출/일몰 시간이 없는 경우 데이터에 추가하지 않음
        
        current_date += datetime.timedelta(days=1)

    df = pd.DataFrame({"Date": dates, "Daylight Hours": day_lengths})

    # 그래프 출력
    if not df.empty:
        title_text = f"서울 낮 길이 변화 ({start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')})"
        fig = px.line(df, x="Date", y="Daylight Hours",
                      title=title_text,
                      labels={"Daylight Hours": "낮 길이 (시간)", "Date": "날짜"},
                      hover_data={"Date": "|%Y년 %m월 %d일"})
        fig.update_traces(mode='lines')
        fig.update_layout(xaxis_title="날짜", yaxis_title="낮 길이 (시간)",
                          hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("선택된 기간 동안 낮 길이 데이터를 계산할 수 없습니다. 날짜를 다시 확인해주세요.")

st.markdown("---")
st.info("이 앱은 'astral' 라이브러리를 사용하여 천문학적인 시간을 계산합니다. **일반적인 낮 길이는 일몰 시간에서 일출 시간을 뺀 값입니다.**")
