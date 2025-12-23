import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
st.set_page_config(layout="wide")
SideBarLinks()
add_logo("assets/FitHublogo.png")



API_BASE = "http://api:4000/a"

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

.page-title {
    color: #328E6E;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.section-title {
    color: #328E6E;
    font-size: 26px;
    font-weight: 600;
    margin-top: 25px;
}

div.stButton > button {
    background-color: #328E6E;
    color: #E1EEBC;
    height: 3.5em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

div.stButton > button:hover {
    background-color: #2a7359;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">📑 Reports Management</div>', unsafe_allow_html=True)

# View Pending Reports
st.markdown('<div class="section-title">View Pending Reports</div>', unsafe_allow_html=True)

try:
    response = requests.get(f"{API_BASE}/reports/pending")
    if response.status_code == 200:
        reports = response.json()
        st.write(f"Found **{len(reports)} pending reports**")

        for report in reports:
            with st.expander(f"Report #{report['ReportID']} — Severity {report['Severity']}"):
                st.write(f"**Note:** {report['Note']}")
                st.write(f"**Reported Item:** {report['ReportedItem']}")
    else:
        st.error("Failed to fetch reports.")
except requests.exceptions.RequestException:
    st.error("Could not connect")



# Resolve a Report
st.markdown('<div class="section-title">Resolve a Report</div>', unsafe_allow_html=True)

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
