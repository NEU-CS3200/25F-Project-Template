import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# sidebar links 
SideBarLinks()

st.markdown("""
    <div style="
        padding: 20px; 
        background-color:#000000;
        border-radius:12px;
        margin-bottom:20px;">
        <h1 style="color:#FF1A1A; margin:0;"> <i> Hello, Trainer. </i>💪</h1>
        <p style="color:#FFFFFF; margin-top:8px;">What would you like to do today? </p>
    </div>
""", unsafe_allow_html=True)

# Create Workout Template
if st.button("Create Workout Templates", use_container_width=True):
    st.switch_page("pages/18_trainer_workout_templates.py")

# Assign Workout to Client
if st.button("Assign Workout to Client", use_container_width=True):
    st.switch_page("pages/19_trainer_client_programs.py")

# Track Client Progress
if st.button("Track Client Progress", use_container_width=True):
    st.switch_page("pages/20_trainer_client_logs.py")