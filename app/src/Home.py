##################################################
# CourtVision - Basketball Scouting Platform
##################################################

import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")
st.title('CourtVision')
st.write('### Basketball Scouting & Analytics Platform')
st.write('\n\n')
st.write('#### Welcome! Select your role to continue:')

# System Admin - Ryan Suri
if st.button("Act as Ryan Suri - System Administrator",
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'system_admin'
    st.session_state['first_name'] = 'Ryan'
    st.session_state['user_id'] = 1
    logger.info("Logging in as System Administrator")
    st.switch_page('pages/00_Admin_Home.py')

# Basketball Player - Sean Lee
if st.button('Act as Sean Lee - Basketball Player',
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'player'
    st.session_state['first_name'] = 'Sean'
    st.session_state['user_id'] = 101
    logger.info("Logging in as Basketball Player")
    st.switch_page('pages/10_Player_Home.py')

# Data Analyst Scout - John Tukey
if st.button('Act as John Tukey - Data Analyst Scout',
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = 'John'
    st.session_state['user_id'] = 201
    logger.info("Logging in as Data Analyst Scout")
    st.switch_page('pages/20_Analyst_Home.py')

# Game Scout - Sara Chin
if st.button('Act as Sara Chin - Game Scout',
            type='primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'game_scout'
    st.session_state['first_name'] = 'Sara'
    st.session_state['user_id'] = 202
    logger.info("Logging in as Game Scout")
    st.switch_page('pages/30_Scout_Home.py')