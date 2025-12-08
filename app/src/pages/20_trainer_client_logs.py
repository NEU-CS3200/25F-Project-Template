import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("📊 Track Client Progress")

API_BASE = "http://web-api:4000"

# filter options
status_filter = st.selectbox(
    "Filter by Completion Status",
    ["all", "completed", "partial", "not_started"]
)

# get the logs
try:
    if status_filter == "all":
        response = requests.get(f"{API_BASE}/trainer/client-logs")
    else:
        response = requests.get(f"{API_BASE}/trainer/client-logs/{status_filter}")

    if response.status_code == 200:
        logs = response.json()
        st.write("### Client Workout Logs")
        st.dataframe(logs)
    else:
        st.error("Error fetching logs.")

except Exception as e:
    st.error(f"API connection error: {e}")