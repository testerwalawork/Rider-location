import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# 1. Tumchi Google Sheet CSV URL ithe taka
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSa1YGHQjXvOjLI0_GDeEDbk7l5jTsEU2W637m0hIrRhs-SRszSb32WsloW_UXWLJML_4YTBIhMwKIi/pub?gid=0&single=true&output=csv"

st.set_page_config(page_title="Rider Group App", layout="wide")

# App title
st.title("🏍️ Rider Group: Live Map & Chat")

# --- SIDEBAR: RIDER ACTIONS ---
st.sidebar.header("📍 Tumche Location")
loc = get_geolocation()
if loc:
    st.sidebar.success(f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}")
else:
    st.sidebar.warning("GPS Permission allow kara")

st.sidebar.divider()
st.sidebar.header("👥 Group Members")

try:
    # Google Sheet madhun data vachne
    df = pd.read_csv(SHEET_URL)
    df = df.dropna(subset=['Name', 'Phone', 'Latitude', 'Longitude'])

    for index, row in df.iterrows():
        with st.sidebar.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            # 1. Rider che Nav
            col1.write(f"**{row['Name']}**")
            
            # 2. Call Button (Direct Phone Dialer)
            col2.markdown(f"[📞](tel:{row['Phone']})")
            
            # 3. WhatsApp Button (Direct Chat)
            # Space asel tar URL madhe ti %20 ne badlavi lagte
            msg = f"Hey {row['Name']}, kuthe aahes? App var location check kar."
            wa_url = f"https://wa.me/{row['Phone']}?text={msg.replace(' ', '%20')}"
            col3.markdown(f"[💬]({wa_url})")
            
            st.sidebar.divider()

    # --- MAIN MAP ---
    st.subheader("Live Movement Map")
    
    # Map center point tharavne
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

    # Destination (He tumhi sheet madhun hi gheu shakta)
    dest_lat, dest_lon = 18.7557, 73.4091 
    folium.Marker([dest_lat, dest_lon], popup="Destination", icon=folium.Icon(color="red", icon="flag")).add_to(m)

    # Saglya Riders che Markers
    for index, row in df.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']], 
            popup=f"{row['Name']}\n{row['Phone']}",
            icon=folium.Icon(color="blue", icon="motorcycle", prefix='fa')
        ).add_to(m)

    st_folium(m, width=700, height=500)

    # Auto Refresh Button
    if st.button('🔄 Refresh Locations'):
        st.rerun()

except Exception as e:
    st.error(f"Error: Sheet link check kara. Details: {e}")

st.info("Tip: WhatsApp button var click kelya var direct chat ughdel.")
