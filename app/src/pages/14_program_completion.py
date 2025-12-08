import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Workout Program Completion Rates")

resp = requests.get("http://web-api:4000/health_analyst/completion_rate")

if resp.status_code == 200:
    st.dataframe(resp.json())
else:
    st.error("Could not fetch completion rates.")
