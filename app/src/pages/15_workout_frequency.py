import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Workout Template Usage Frequency")

resp = requests.get("http://web-api:4000/health_analyst/frequency")

if resp.status_code == 200:
    st.dataframe(resp.json())
else:
    st.error("Error retrieving workout frequency.")
