import logging
import streamlit as st
from modules.nav import SideBarLinks

# Logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(layout='wide')
st.session_state['authenticated'] = False

# Sidebar
SideBarLinks(show_home=True)

# ***************************************************
# CSS Styling
# ***************************************************
st.markdown("""
    <style>
    /* Center everything */
    .block-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Swap text styling */
    .swap-text {
        color: #328E6E;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 40px;
        margin-top: 20px;
        white-space: nowrap;
    }
    
    /* Buttons styling */
    div.stButton > button {
        background-color: #328E6E;
        color: #E1EEBC;
        height: 4em;
        width: 100%;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
    }
    
    div.stButton > button:hover {
        background-color: #2a7359;
        border-color: #328E6E;
    }
    
    /* Make all columns flex properly */
    [data-testid="column"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Emoji fixed width */
    .emoji-container {
        width: 80px;
        text-align: right;
        padding-right: 15px;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ***************************************************
# Main content
# ***************************************************

# Logo centered at top
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Swap into Style text
st.markdown('<div class="swap-text">Swap into style and swap roles</div>', unsafe_allow_html=True)

# Admin emoji + button
col1, col2 = st.columns([80, 1000], gap="small")
with col1:
    st.markdown('<div class="emoji-container"><div style="font-size: 60px;">🧑🏻‍💼</div></div>', unsafe_allow_html=True)
with col2:
    if st.button("Admin", key="Admin", use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'Admin: Aisha'
        st.session_state['first_name'] = 'Aisha'
        logger.info("Logging in as Admin Persona")
        st.switch_page('pages/05_Admin_Home.py')

st.markdown('<br>', unsafe_allow_html=True)

# Data Analyst emoji + button
col1, col2 = st.columns([80, 1000], gap="small")
with col1:
    st.markdown('<div class="emoji-container"><div style="font-size: 60px;">👩🏽‍💻</div></div>', unsafe_allow_html=True)
with col2:
    if st.button("Data Analyst", key="Data Analyst", use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'Data Analyst: Blair'
        st.session_state['first_name'] = 'Blair'
        logger.info("Logging in as Data Analyst Persona")
        st.switch_page('pages/00_DADash.py')

st.markdown('<br>', unsafe_allow_html=True)

# Swapper emoji + button
col1, col2 = st.columns([80, 1000], gap="small")
with col1:
    st.markdown('<div class="emoji-container"><div style="font-size: 60px;">🙋🏼‍♂️</div></div>', unsafe_allow_html=True)
with col2:
    if st.button("Swapper", key="Swapper", use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'Swapper: Andrea'
        st.session_state['first_name'] = 'Andrea'
        logger.info("Logging in as Swapper Persona")
        st.switch_page('pages/00_SwapperDash.py')

st.markdown('<br>', unsafe_allow_html=True)

# Taker emoji + button
col1, col2 = st.columns([80, 1000], gap="small")
with col1:
    st.markdown('<div class="emoji-container"><div style="font-size: 60px;">🙋🏼‍♀️</div></div>', unsafe_allow_html=True)
with col2:
    if st.button("Taker", key="Taker", use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'Taker: Alice'
        st.session_state['first_name'] = 'Alice'
        logger.info("Logging in as Taker Persona")
        st.switch_page('pages/00_TakerDash.py')