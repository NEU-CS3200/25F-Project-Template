import streamlit as st
import requests
import logging
logger = logging.getLogger(__name__)

API_BASE = "http://web-api:4000/system_admin"

st.title("System Logs")

action_filter = st.text_input("Filter by action_type (optional): e.g., EXERCISE_FLAGGED")

if st.button("Load Logs"):
    if action_filter:
        url = f"{API_BASE}/system_logs/{action_filter}"
    else:
        url = f"{API_BASE}/system_logs"

    response = requests.get(url)

    if response.status_code == 200:
        logs = response.json()
        st.dataframe(logs)
    else:
        st.error("Failed to load logs.")

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/00_Sys_Admin_home.py")
