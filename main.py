import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# 1. Tumchi Google Sheet chi CSV URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSa1YGHQjXvOjLI0_GDeEDbk7l5jTsEU2W637m0hIrRhs-SRszSb32WsloW_UXWLJML_4YTBIhMwKIi/pub?gid=0&single=true&output=csv"

st.title("🏍️ Auto-Moving Rider Map")

# 2. Browser kadun Location ghene (Auto-detect)
loc = get_geolocation()

if loc:
    curr_lat = loc['coords']['latitude']
    curr_lon = loc['coords']['longitude']
    st.success(f"Tumche Live Location: {curr_lat}, {curr_lon}")
    # Ithe ek button deu shakta 'Update My Location'
    # Jyane he coordinates Sheet madhe save hotil
else:
    st.warning("GPS access kara (Allow kara)")

# 3. Sheet madhun saglyancha data vachne
df = pd.read_csv(SHEET_URL)

# 4. Map display karne
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

for index, row in df.iterrows():
    folium.Marker(
        [row['Latitude'], row['Longitude']], 
        popup=row['Name'],
        icon=folium.Icon(color="blue", icon="motorcycle", prefix='fa')
    ).add_to(m)

st_folium(m, width=700, height=500)

# 5. Auto-Refresh logic (Dar 30 secondala app refresh hoil)
st.empty()
import time
time.sleep(30)
st.rerun()
