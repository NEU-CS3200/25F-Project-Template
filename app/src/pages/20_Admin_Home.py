# System Admin Landing Page

import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

# Athentification and Role check
if not st.session_state.get('authenticated'):
    st.switch_page('Home.py')

if st.session_state.get('role') != 'administrator':
    st.switch_page('Home.py')

SideBarLinks()


# ----------------
# Page content
# ----------------
logger.info("Loading System Administrator Dashboard")
st.title('System Administator Dashboard')
st.write(f"Welcome, {st.session_state.get('first_name', 'Admin')}!")
st.write("Use the tools below to manage users, review reports, and monitor platform health.")

st.divider()

st.subheader("Admin Overview Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pending Applications", "-")
    st.caption("Students/Alumni awaiting admin approval")

with col2:
    st.metric("Open Reports", "-")
    st.caption("Flagged issues requiring review")

with col3:
    st.metric("Active Connections", "-")
    st.caption("Current mentorship relationships")

st.divider()

st.subheader("Admin Tools")

c1, c2, c3 = st.columns(3)

with c1:
    st.write("**Review Applications**")
    st.caption("Approve or reject new user applications")
    if st.button('Go to Applications', type='primary', use_container_width=True):
      st.switch_page('pages/21_Admin_Applications.py')

with c2:
    st.write("**Review Reports**")
    st.caption("Reply to or resolve user-reported issues")
    if st.button('Go to Reports', type='primary', use_container_width=True):
      st.switch_page('pages/22_Admin_Reports.py')

with c3:
    st.write("**System Stats**")
    st.caption("High-level platform activity and health metrics")
    if st.button('View System Stats', type='primary', use_container_width=True):
      st.switch_page('pages/23_Admin_System_Stats.py')