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

# ------------------ BUTTON GRID ------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="padding:18px; border-radius:12px; border:1px solid #333;">
            <h3>📘 Workout Templates</h3>
            <p>Create, update, delete templates and manage your exercise library.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("➡ Manage Workout Templates", use_container_width=True):
        st.switch_page("pages/18_trainer_workout_templates.py")

    st.write("")

    st.markdown("""
        <div style="padding:18px; border-radius:12px; border:1px solid #333;">
            <h3>🧍 Client Programs</h3>
            <p>Assign templates, update schedules, and track program progress.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("➡ Manage Client Programs", use_container_width=True):
        st.switch_page("pages/19_trainer_client_programs.py")

with col2:
    st.markdown("""
        <div style="padding:18px; border-radius:12px; border:1px solid #333;">
            <h3>📊 Client Logs & Feedback</h3>
            <p>Review workout logs and add personalized feedback.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("➡ View Logs & Add Feedback", use_container_width=True):
        st.switch_page("pages/20_trainer_client_logs.py")

    st.write("")

    st.markdown("""
        <div style="padding:18px; border-radius:12px; border:1px solid #333;">
            <h3>📈 Client Progress</h3>
            <p>Analyze client PR trends, completion rates, and performance stats.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("➡ View Client Progress", use_container_width=True):
        st.switch_page("pages/21_Client_home.py")
