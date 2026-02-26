import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Tumchya Google Sheet chi Public CSV Link ithe taka
# (Sheet madhe File > Share > Publish to web > CSV select kara ani ti link ithe taka)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSa1YGHQjXvOjLI0_GDeEDbk7l5jTsEU2W637m0hIrRhs-SRszSb32WsloW_UXWLJML_4YTBIhMwKIi/pub?gid=0&single=true&output=csv"

st.set_page_config(page_title="Rider Group Live Map", layout="wide")


def get_data():
    # Google Sheet madhun data vachne
    return pd.read_csv(SHEET_URL)


st.title("🏍️ Rider Group: Manual Location Update")

try:
    df = get_data()

    # Sidebar: Members and Calling
    st.sidebar.header("Group Members")
    for index, row in df.iterrows():
        col1, col2 = st.sidebar.columns([2, 1])
        col1.write(f"**{row['Name']}**")
        col2.markdown(f"[📞 Call](tel:{row['Phone']})")

    # Destination (He tumhi code madhe fix thevu shakta)
    dest_lat, dest_lon = 18.7557, 73.4091

    # 2. Map Setup
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=10)

    # Destination Marker (Red)
    folium.Marker([dest_lat, dest_lon], popup="Destination", icon=folium.Icon(color="red")).add_to(m)

    # Riders Markers (Blue) from Google Sheet
    for index, row in df.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=row['Name'],
            icon=folium.Icon(color="blue")
        ).add_to(m)

    # Display Map
    st_folium(m, width=800, height=500)

    if st.button('Refresh Location'):
        st.rerun()

except Exception as e:
    st.error("Sheet link check kara kiwa data format barobar asu dya.")