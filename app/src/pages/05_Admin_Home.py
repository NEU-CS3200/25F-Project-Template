import logging
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# Page config
st.set_page_config(layout="wide")

# Sidebar with logo
SideBarLinks()
add_logo("assets/FitHublogo.png")

# Log admin dashboard access
logger.info(f"Admin Dashboard loaded by {st.session_state.get('first_name', 'Unknown')}")


# CSS Styling

st.markdown("""
<style>


.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

/* Page title */
.admin-title {
    color: #328E6E;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

/* Section subtitle */
.section-subtitle {
    color: #328E6E;
    font-size: 22px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 10px;
}

/* Buttons*/
div.stButton > button {
    background-color: #328E6E;
    color: #E1EEBC;
    height: 4em;
    width: 100%;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
}

div.stButton > button:hover {
    background-color: #2a7359;
    border-color: #328E6E;
}

/* Center columns properly */
[data-testid="column"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)


# Admin Dashboard UI


st.markdown('<div class="admin-title">🧑🏻‍💼 Admin Dashboard</div>', unsafe_allow_html=True)

st.markdown('<div class="section-subtitle">Manage the platform and user operations</div>', unsafe_allow_html=True)
st.write("")  # spacing


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Manage Reports"):
        st.switch_page("pages/10_Reports_Management.py")

with col2:
    if st.button("User Roles"):
        logger.info("Navigating to User Roles page")
        st.switch_page("pages/20_Admin_User_Tools.py")

with col3:
    if st.button("Item Cleanup Tools"):
        logger.info("Navigating to Item Cleanup Tools")
        st.switch_page("pages/30_Item_Cleanup.py")

