import streamlit as st
import requests
import logging
logger = logging.getLogger(__name__)

API_BASE = "http://web-api:4000/system_admin"

st.title("Backup Logs")

if st.button("View All Backups"):
    resp = requests.get(f"{API_BASE}/backup_logs")
    st.dataframe(resp.json())

st.write("---")
st.subheader("Backup Status (Is Backup Due?)")

if st.button("Check Backup Status"):
    resp = requests.get(f"{API_BASE}/backup_logs/status")
    st.json(resp.json())

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/00_Sys_Admin_home.py")
