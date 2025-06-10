import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="시드니 관광지 가이드", layout="wide")

# 타이틀
st.title("🇦🇺 시드니 관광지 친절 가이드")
st.markdown("드롭다운에서 관광지를 선택하면, 해당 위치와 정보를 확인할 수 있어요!")

# 관광지 정보 정의
tourist_spots = {
    "시드니 오페라 하우스": {
        "lat": -33.8568,
        "lon": 151.2153,
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/40/Sydney_Opera_House_Sails.jpg",
        "description": "세계에서 가장 유명한 공연장 중 하나로, 유네스코 세계유산이기도 합니다. 바다와 어우러진 독특한 디자인은 사진 명소로도 유명합니다."
    },
    "하버 브리지": {
        "lat": -33.8523,
        "lon": 151.2108,
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Sydney_Harbour_Bridge_from_the_south.jpg",
        "description": "‘코트 행거’라는 별명을 가진 대형 아치형 철교입니다. 브리지 클라임을 통해 다리 꼭대기까지 올라가 볼 수 있습니다."
    },
    "본다이 비치": {
        "lat": -33.8908,
        "lon": 151.2743,
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Bondi_Beach_Sydney_Australia.jpg",
        "description": "현지인과 관광객 모두에게 사랑받는 시드니의 대표 해변입니다. 수영, 서핑, 해변 산책로까지 다양하게 즐길 수 있어요."
    },
}

# 드롭다운 메뉴
selected_spot = st.selectbox("👀 관광지를 선택하세요", list(tourist_spots.keys()))

# 선택된 관광지 정보
spot = tourist_spots[selected_spot]

# 지도 생성 및 마커 추가
m = folium.Map(location=[spot["lat"], spot["lon"]], zoom_start=14)
folium.Marker(
    location=[spot["lat"], spot["lon"]],
    popup=f"<b>{selected_spot}</b><br>{spot['description']}",
    tooltip=selected_spot,
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(m)

# 지도 출력
st.subheader("🗺️ 선택한 관광지 지도")
st_data = st_folium(m, width=700, height=500)

# 상세 정보 출력
st.subheader(f"📌 {selected_spot}")
st.image(spot["image"], use_column_width=True)
st.write(spot["description"])
