import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Reports Management")

API_BASE = "http://api:4000/a"

# ===============================
# USER STORY 1 — VIEW PENDING REPORTS
# ===============================
st.write("## View Pending Reports")

try:
    response = requests.get(f"{API_BASE}/reports/pending")
    if response.status_code == 200:
        reports = response.json()

        st.write(f"Found **{len(reports)} pending reports**")

        # Display each report inside an expander
        for report in reports:
            with st.expander(f"Report #{report['ReportID']} — Severity {report['Severity']}"):
                st.write(f"**Note:** {report['Note']}")
                st.write(f"**Reported Item:** {report['ReportedItem']}")

    else:
        st.error("Failed to fetch reports from API.")

except requests.exceptions.RequestException:
    st.error("Could not connect to API server.")
    st.info("Make sure the API is running.")

# ===============================
# USER STORY 1 — RESOLVE REPORT
# ===============================
st.write("## Resolve a Report")

col1, col2 = st.columns(2)
with col1:
    report_id = st.number_input("Enter Report ID", min_value=1, step=1)

with col2:
    if st.button("Resolve Report"):
        try:
            resp = requests.put(f"{API_BASE}/reports/{report_id}/resolve")
            st.write(resp.json())
        except:
            st.error("Could not resolve the report.")
