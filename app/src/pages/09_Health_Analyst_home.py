import streamlit as st
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

# ----- HEADER -----
st.markdown("""
    <div style="
        padding: 20px; 
        background-color:#000000;
        border-radius:12px;
        margin-bottom:20px;">
        <h1 style="color:#FF1A1A; margin:0;"> <i> Hello, Health Analyst. </i>📊</h1>
        <p style="color:#FFFFFF; margin-top:8px;">Analyze client health trends and performance insights.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Workout Analytics")
    st.page_link("pages/10_avg_workout_duration.py",
                 label="Average Workout Duration", icon="⏱️")
    st.page_link("pages/15_workout_frequency.py",
                 label="Workout Template Frequency", icon="📊")

with col2:
    st.header("Client Profiles")
    st.page_link("pages/11_client_info.py",
                 label="Client Demographics & Fitness Levels", icon="🧍‍♂️")

with col3:
    st.header("Health Metrics")
    st.page_link("pages/12_recent_health_metrics.py",
                 label="Most Recent Health Metrics", icon="❤️")
    st.page_link("pages/13_health_progression.py",
                 label="Health Progression by Month", icon="📈")
    st.page_link("pages/14_program_completion.py",
                 label="Workout Program Completion Rate", icon="🏆")
