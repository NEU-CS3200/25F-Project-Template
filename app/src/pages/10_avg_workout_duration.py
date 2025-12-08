import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Average Workout Duration")

with st.form("duration_form"):
    year = st.text_input("Filter by Year (optional)")
    week = st.text_input("Filter by Week # (optional)")
    submitted = st.form_submit_button("Submit")

if submitted:
    params = {}
    if year:
        params["year"] = year
    if week:
        params["week"] = week

    resp = requests.get("http://web-api:4000/health_analyst/avg_duration", params=params)

    if resp.status_code == 200:
        st.dataframe(resp.json())
    else:
        st.error("Error retrieving data.")