import logging
logger = logging.getLogger(__name__)

import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Load sidebar navigation (includes admin links if authenticated)
SideBarLinks()

# Add logo to sidebar
add_logo("public/FitHublogo.png")

# Log admin dashboard access
logger.info(f"Admin Dashboard loaded by {st.session_state.get('first_name', 'Unknown')}")

# Title
st.title("Admin Dashboard")

st.markdown("### ")

if st.button("Manage Reports", use_container_width=True):
    logger.info("Navigating to Reports Management")
    st.switch_page("pages/21_Admin_Manage_Reports.py")

if st.button("User Roles & Access Tools", use_container_width=True):
    logger.info("Navigating to User Tools")
    st.switch_page("pages/22_Admin_User_Tools.py")

if st.button("Item Cleanup Tools", use_container_width=True):
    logger.info("Navigating to Item Cleanup Tools")
    st.switch_page("pages/23_Admin_Item_Cleanup.py")

st.markdown("<br><center>DistinctDevs ©2025</center>", unsafe_allow_html=True)
