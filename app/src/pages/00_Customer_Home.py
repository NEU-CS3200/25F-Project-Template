import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# ---- Page Config ----
st.set_page_config(layout='wide')

# ---- Sidebar ----
SideBarLinks()

# ---- Styling (matches Farmer theme with customer colors) ----
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #E8F4FF, #F3FAFF);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.03);
}

.hero h1 {
    margin-bottom: 0.5rem;
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
    font-size: 2.5rem;
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
    <h1>🧑‍🍳 Welcome back, {st.session_state['first_name']}!</h1>
    <p>Customize your meals, plan your week, and chat with support.</p>
</div>
""", unsafe_allow_html=True)

# ---- Action Cards ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">🥗</div>
        <div class="section-title">Meal Preferences</div>
        <p>Set your dietary preferences and favorite meals.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Open Meal Preferences', use_container_width=True):
        st.switch_page('pages/01_Meal_Preferences.py')

with col2:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">🗓️</div>
        <div class="section-title">Meal Planning</div>
        <p>Plan your meals for the week with ease.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Open Meal Planner', use_container_width=True):
        st.switch_page('pages/02_Meal_Plan.py')

with col3:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">💬</div>
        <div class="section-title">Chat Support</div>
        <p>Chat with support or ask questions.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Open Chat Page', use_container_width=True):
        st.switch_page('pages/03_Chat_Page.py')

# ---- Footer ----
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; padding: 1rem;">
    🍽️ Making meal planning simple and enjoyable.
</div>
""", unsafe_allow_html=True)









