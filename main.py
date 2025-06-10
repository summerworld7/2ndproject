import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="시드니 관광지 & 브런치 카페 가이드", layout="wide")

# 타이틀
st.title("🇦🇺 시드니 관광지 & 브런치 카페 가이드")
st.markdown("드롭다운에서 명소나 브런치 카페를 선택해 자세한 정보를 확인해보세요!")

# 장소 정보
places = {
    # 관광지
    "시드니 오페라 하우스": {
        "lat": -33.8568,
        "lon": 151.2153,
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/40/Sydney_Opera_House_Sails.jpg",
        "description": "세계에서 가장 유명한 공연장 중 하나로, 유네스코 세계유산이기도 합니다. 바다와 어우러진 독특한 디자인은 사진 명소로도 유명합니다.",
        "category": "관광지"
    },
    "하버 브리지": {
        "lat": -33.8523,
        "lon": 151.2108,
        "image": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Sydney_Harbour_Bridge_from_the_south.jpg",
        "description": "‘코트 행거’라는 별명을 가진 대형 아치형 철교입니다. 브리지 클라임을 통해 다리 꼭대기까지 올라가 볼 수 있습니다.",
        "category": "관광지"
    },
    "본다이 비치": {
        "lat": -33.8908,
        "lon": 151.2743,
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Bondi_Beach_Sydney_Australia.jpg",
        "description": "현지인과 관광객 모두에게 사랑받는 시드니의 대표 해변입니다. 수영, 서핑, 해변 산책로까지 다양하게 즐길 수 있어요.",
        "category": "관광지"
    },
    
    # 브런치 카페
    "The Grounds of Alexandria": {
        "lat": -33.9105,
        "lon": 151.1944,
        "image": "https://thegrounds.com.au/wp-content/uploads/2023/02/grounds-garden-entry.jpeg",
        "description": "대형 정원과 포토존, 맛있는 커피와 베이커리로 유명한 시드니 최고의 브런치 명소입니다.",
        "category": "브런치 카페"
    },
    "Bourke Street Bakery": {
        "lat": -33.8896,
        "lon": 151.2099,
        "image": "https://cdn.weekendnotes.com/cache/8a/78/8a782232cbe20d6e9a001e31b8fc5ad2.jpg",
        "description": "현지인들이 사랑하는 파이와 커피가 있는 작은 베이커리 카페. 시드니 전역에 지점이 있지만, 서리힐즈 본점이 가장 유명합니다.",
        "category": "브런치 카페"
    },
    "Single O Surry Hills": {
        "lat": -33.8820,
        "lon": 151.2124,
        "image": "https://media.timeout.com/images/105240190/750/422/image.jpg",
        "description": "스페셜티 커피와 창의적인 브런치 메뉴로 유명한 서리힐즈의 인기 카페. 커피 애호가에게 강추!",
        "category": "브런치 카페"
    },
}

# 드롭다운 메뉴
selected_place = st.selectbox("📍 장소를 선택하세요", list(places.keys()))

# 선택된 장소 정보
spot = places[selected_place]

# 지도 생성
m = folium.Map(location=[spot["lat"], spot["lon"]], zoom_start=15)
folium.Marker(
    location=[spot["lat"], spot["lon"]],
    popup=f"<b>{selected_place}</b><br>{spot['description']}",
    tooltip=selected_place,
    icon=folium.Icon(color="green" if spot["category"] == "브런치 카페" else "blue", icon="info-sign"),
).add_to(m)

# 지도 출력
st.subheader("🗺️ 위치 확인")
st_folium(m, width=700, height=500)

# 상세 정보 출력
st.subheader(f"📌 {selected_place}")
st.image(spot["image"], use_column_width=True)
st.write(spot["description"])
