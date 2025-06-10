import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="시드니 관광지 가이드", layout="wide")

# 타이틀
st.title("🇦🇺 시드니 관광지 친절 가이드")
st.markdown("시드니의 주요 명소들을 소개하고, 지도에서 위치를 확인해보세요!")

# 관광지 정보
tourist_spots = [
    {
        "name": "시드니 오페라 하우스",
        "lat": -33.8568,
        "lon": 151.2153,
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/40/Sydney_Opera_House_Sails.jpg",
        "description": "세계에서 가장 유명한 공연장 중 하나로, 유네스코 세계유산이기도 합니다. 바다와 어우러진 독특한 디자인은 사진 명소로도 유명합니다."
    },
    {
        "name": "하버 브리지",
        "lat": -33.8523,
        "lon": 151.2108,
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/84/Sydney_Harbour_Bridge_from_the_air.jpg",
        "description": "‘코트 행거’라는 별명을 가진 대형 아치형 철교입니다. 브리지 클라임을 통해 다리 꼭대기까지 올라가 볼 수 있습니다."
    },
    {
        "name": "본다이 비치",
        "lat": -33.8908,
        "lon": 151.2743,
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/39/Bondi_Beach_from_north.jpg",
        "description": "현지인과 관광객 모두에게 사랑받는 시드니의 대표 해변입니다. 수영, 서핑, 해변 산책로까지 다양하게 즐길 수 있어요."
    },
]

# 지도 생성
m = folium.Map(location=[-33.8688, 151.2093], zoom_start=12)

# 마커 추가
for spot in tourist_spots:
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(f"<b>{spot['name']}</b><br>{spot['description']}", max_width=300),
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# 지도 출력
st.subheader("🗺️ 시드니 관광지 지도")
st_data = st_folium(m, width=700, height=500)

# 관광지 정보 출력
st.subheader("📌 관광지 상세 안내")
for spot in tourist_spots:
    st.markdown(f"### {spot['name']}")
    st.image(spot["image"], use_column_width=True)
    st.write(spot["description"])
    st.markdown("---")
