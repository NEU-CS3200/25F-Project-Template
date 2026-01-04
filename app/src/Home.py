##################################################
# CourtVision - Basketball Scouting Platform
##################################################

import logging

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Reset authentication on landing page
st.session_state['authenticated'] = False
st.session_state['role'] = None

SideBarLinks(show_home=True)

# Custom CSS to center the content
st.markdown("""
<style>
    /* Center the main content */
    .block-container {
        max-width: 700px;
        margin: 0 auto;
        text-align: center;
        padding-top: 2rem !important;
    }

    /* Center all text elements */
    h1, h2, h3, h4, p {
        text-align: center !important;
    }

    /* Compact title spacing */
    h1 {
        margin-bottom: 0.5rem !important;
        font-size: 2.5rem !important;
    }

    h3 {
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        font-size: 1.3rem !important;
    }

    h4 {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
        font-size: 1.1rem !important;
    }

    /* Keep buttons full width but centered container */
    .stButton {
        display: block;
        margin: 8px auto;
    }

    .stButton > button {
        padding: 10px 20px !important;
        font-size: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

logger.info("Loading the Home page of the app")
st.title('🏀 CourtVision')
st.write('### Basketball Scouting & Analytics Platform')
st.write('#### Welcome! Select your role to continue:')

# System Admin - Ryan Suri
if st.button("Act as Ryan Suri - System Administrator",
             type='primary',
             use_container_width=True):
    st.session_state['role'] = 'system_admin'
    st.session_state['first_name'] = 'Ryan'
    st.session_state['user_id'] = 1
    st.session_state['selected_user'] = 'Ryan Suri'
    logger.info("Selected System Administrator - redirecting to login")
    st.switch_page('pages/Login.py')

# Basketball Player - Sean Lee (using Stephen Curry's ID as placeholder)
if st.button('Act as Sean Lee - Basketball Player',
             type='primary',
             use_container_width=True):
    st.session_state['role'] = 'player'
    st.session_state['first_name'] = 'Sean'
    st.session_state['user_id'] = 2  # Changed from 101 to 2 (Stephen Curry)
    st.session_state['selected_user'] = 'Sean Lee'
    logger.info("Selected Basketball Player - redirecting to login")
    st.switch_page('pages/Login.py')

# Data Analyst Scout - John Tukey
if st.button('Act as John Tukey - Data Analyst Scout',
             type='primary',
             use_container_width=True):
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = 'John'
    st.session_state['user_id'] = 1
    st.session_state['selected_user'] = 'John Tukey'
    logger.info("Selected Data Analyst Scout - redirecting to login")
    st.switch_page('pages/20_Analyst_Home.py')

# Game Scout - Sara Chin
if st.button('Act as Sara Chin - Game Scout',
             type='primary',
             use_container_width=True):
    st.session_state['role'] = 'game_scout'
    st.session_state['first_name'] = 'Sara'
    st.session_state['user_id'] = 1
    st.session_state['selected_user'] = 'Sara Chin'
    logger.info("Selected Game Scout - redirecting to login")
    st.switch_page('pages/30_Scout_Home.py')