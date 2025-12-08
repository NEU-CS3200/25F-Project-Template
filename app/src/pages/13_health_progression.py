import streamlit as st
import requests
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Health Progression by Month")

client_id = st.text_input("Enter Client ID")

if st.button("Submit"):
    if not client_id:
        st.warning("Please enter a Client ID.")
    else:
        url = f"http://web-api:4000/health_analyst/health_progression/{client_id}"
        resp = requests.get(url)

        if resp.status_code == 200:
            st.dataframe(resp.json())
        else:
            st.error("Error retrieving health progression.")
