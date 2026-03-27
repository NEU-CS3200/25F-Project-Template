##################################################
# Main Entry File for FitFlow Streamlit App
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# ---------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------
st.set_page_config(layout="wide", page_title="FitFlow")

# ---------------------------------------------
# Session State Initialization
# ---------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "first_name" not in st.session_state:
    st.session_state["first_name"] = None

# ---------------------------------------------
# Sidebar Navigation (home only shows Home/Logout)
# ---------------------------------------------
SideBarLinks(show_home=True)

# ---------------------------------------------
# HERO SECTION
# ---------------------------------------------
st.markdown(
    """
    <div style="
        background-color: #000;
        padding: 40px 30px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.2);
        margin-bottom: 30px;">
        <h1 style="color: #FF1A1A; font-size: 3rem; margin-bottom: 10px;">
            FitFlow
        </h1>
        <p style="color:white" font-size: 1.2rem;">
            Choose a persona to experience the platform.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------
# Persona Prompt
# ---------------------------------------------
st.markdown(
    "<h3 style='text-align:center;'>Select a user role to continue</h3>",
    unsafe_allow_html=True,
)
st.write("")

# ---------------------------------------------
# BUTTON GRID
# ---------------------------------------------
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

### --- SYSTEM ADMIN BUTTON ---
with col1:
    if st.button(
        "🖥️  Act as System Admin",
        type="primary",
        use_container_width=True,
    ):
        st.session_state["authenticated"] = True
        st.session_state["role"] = "system_admin"
        st.session_state["first_name"] = "Ava"
        logger.info("Logging in as System Admin persona")
        st.switch_page("pages/00_Sys_Admin_home.py")

### --- HEALTH ANALYST BUTTON ---
with col2:
    if st.button(
        "📊  Act as Health Analyst",
        type="primary",
        use_container_width=True,
    ):
        st.session_state["authenticated"] = True
        st.session_state["role"] = "health_analyst"
        st.session_state["first_name"] = "Dr. Riley"
        logger.info("Logging in as Health Analyst persona")
        st.switch_page("pages/09_Health_Analyst_home.py")

### --- TRAINER BUTTON ---
with col3:
    if st.button(
        "🏋️  Act as Trainer",
        type="primary",
        use_container_width=True,
    ):
        st.session_state["authenticated"] = True
        st.session_state["role"] = "trainer"
        st.session_state["first_name"] = "Jordan"
        logger.info("Logging in as Trainer persona")
        st.switch_page("pages/16_Trainer_home.py")

### --- CLIENT BUTTON ---
with col4:
    if st.button(
        "👤  Act as Client",
        type="primary",
        use_container_width=True,
    ):
        st.session_state["authenticated"] = True
        st.session_state["role"] = "client"
        st.session_state["first_name"] = "Taylor"
        logger.info("Logging in as Client persona")
        st.switch_page("pages/21_Client_home.py")



