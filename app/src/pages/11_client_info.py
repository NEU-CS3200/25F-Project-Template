import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Client Background Information")

resp = requests.get("http://web-api:4000/health_analyst/client_info")

if resp.status_code == 200:
    st.dataframe(resp.json())
else:
    st.error("Could not fetch client info.")
