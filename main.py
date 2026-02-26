import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# 1. Tumchi Google Sheet CSV URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSa1YGHQjXvOjLI0_GDeEDbk7l5jTsEU2W637m0hIrRhs-SRszSb32WsloW_UXWLJML_4YTBIhMwKIi/pub?gid=0&single=true&output=csv"

st.set_page_config(page_title="Rider Group Live", layout="wide")
st.title("🏍️ Rider Group: Live Tracking & Calls")

# --- AUTO LOCATION LOGIC ---
st.sidebar.header("📍 Tumche Location")
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    st.sidebar.success(f"Detected: {lat}, {lon}")
    st.sidebar.info("Hey location Google Sheet madhe update kara.")
else:
    st.sidebar.warning("GPS Allow kara ani Location ON theva.")

# --- MEMBER LIST & CALLING ---
try:
    df = pd.read_csv(SHEET_URL)
    
    st.sidebar.header("📞 Group Members")
    for index, row in df.iterrows():
        col1, col2 = st.sidebar.columns([2, 1])
        col1.write(f"**{row['Name']}**")
        # CALL BUTTON: 'tel:' vaprun direct dialer ughdto
        col2.markdown(f"[📞 Call](tel:{row['Phone']})")
        st.sidebar.divider()

    # --- MAP DISPLAY ---
    st.subheader("Live Movement Map")
    
    # Map center (Sagle riders distil asha paddhatine)
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

    # Destination Marker (Fix - Red)
    folium.Marker([18.7557, 73.4091], popup="Destination", icon=folium.Icon(color="red", icon="flag")).add_to(m)

    # Riders Markers (Blue)
    for index, row in df.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']], 
            popup=f"{row['Name']} (Calling: {row['Phone']})",
            icon=folium.Icon(color="blue", icon="motorcycle", prefix='fa')
        ).add_to(m)

    st_folium(m, width=700, height=500)

    # --- AUTO REFRESH (Dar 30 secondala) ---
    st.info("App dar 30 secondala auto-update hot aahe...")
    import time
    time.sleep(30)
    st.rerun()

except Exception as e:
    st.error("Data load hot nahiye. Sheet URL check kara.")
