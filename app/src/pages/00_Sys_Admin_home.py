import streamlit as st
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

# -------------------- PAGE SETUP --------------------
st.set_page_config(layout="wide")
SideBarLinks()

# -------------------- CUSTOM STYLES --------------------
st.markdown("""
    <style>
        .title-red {
            color: #d90429;
            font-weight: 900;
            font-size: 36px;
        }
        .section-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #2b2d42;
        }
        .btn-space {
            margin-top: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------

st.markdown("""
    <div style="
        padding: 20px; 
        background-color:#000000;
        border-radius:12px;
        margin-bottom:20px;">
        <h1 style="color:#FF1A1A; margin:0;"> <i> Hello, System Administrator. </i>⚙️</h1>
        <p style="color:#FFFFFF; margin-top:8px;"> What would you like to do today? </p>
    </div>
""", unsafe_allow_html=True)


st.write("")  # spacing

# -------------------- LAYOUT --------------------
col1, col2, col3 = st.columns(3, gap="large")

# -------------------- COLUMN 1: USER CREATION --------------------
with col1:
    st.markdown("<div class='section-title'>👤 User Management</div>", unsafe_allow_html=True)

    if st.button("➕ Create New User", use_container_width=True):
        st.switch_page("pages/03_create_user.py")

    if st.button("🏋️ Create Trainer Profile", use_container_width=True):
        st.switch_page("pages/04_create_trainer.py")

    if st.button("🧍 Create Client Profile", use_container_width=True):
        st.switch_page("pages/05_create_client.py")


# -------------------- COLUMN 2: SYSTEM MONITORING --------------------
with col2:
    st.markdown("<div class='section-title'>🖥 System Monitoring</div>", unsafe_allow_html=True)

    if st.button("📜 View System Logs", use_container_width=True):
        st.switch_page("pages/01_system_logs.py")

    if st.button("💾 View Backup Logs & Status", use_container_width=True):
        st.switch_page("pages/02_backup_logs.py")

    if st.button("🔐 Manage User Permissions", use_container_width=True):
        st.switch_page("pages/08_manage_permissions.py")


# -------------------- COLUMN 3: EXERCISE MANAGEMENT --------------------
with col3:
    st.markdown("<div class='section-title'>💪 Exercise Library</div>", unsafe_allow_html=True)

    if st.button("✏️ Update Exercise", use_container_width=True):
        st.switch_page("pages/06_update_exercise.py")

    if st.button("🗑️ Delete Exercise", use_container_width=True):
        st.switch_page("pages/07_delete_exercise.py")
