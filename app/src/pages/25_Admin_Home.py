import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Sidebar
SideBarLinks()

# ---- Styling ----
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #FFF4F4, #FFF7F7);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.03);
}

.action-card {
    background: white;
    border-radius: 18px;
    padding: 2rem 1.5rem;
    box-shadow: 0 12px 25px rgba(0,0,0,0.05);
    text-align: center;
    transition: transform 0.2s ease;
}

.action-card:hover {
    transform: scale(1.03);
}

.action-icon {
    font-size: 2.6rem;
    margin-bottom: 0.6rem;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---- Hero Section ----
st.markdown(f"""
<div class="hero">
    <h1>💻 Welcome, {st.session_state['first_name']}</h1>
    <p>System Admin Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---- Action Cards ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">📖</div>
        <div class="section-title">Recipe Creator</div>
        <p>Create and manage platform recipes.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Create Recipes', use_container_width=True):
        st.switch_page('pages/26_Recipe_Creator.py')

with col2:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">👥</div>
        <div class="section-title">Customer Accounts</div>
        <p>View and manage user accounts.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Manage Accounts', use_container_width=True):
        st.switch_page('pages/27_Customer_Accounts.py')

with col3:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">💬</div>
        <div class="section-title">Customer Chats</div>
        <p>Respond to customer inquiries.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Open Customer Chats', use_container_width=True):
        st.switch_page('pages/28_Admin_Chat.py')


# ---- Footer ----
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; padding: 1rem;">
    ⚙️ Administrative access only.
</div>
""", unsafe_allow_html=True)

