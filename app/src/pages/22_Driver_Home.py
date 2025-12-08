import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Sidebar
SideBarLinks()

# ---- Styling ----
st.markdown("""
<style>
.hero {
background: linear-gradient(135deg, #EEF5FF, #F7FAFF);
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
<h1>🚚 Welcome back, {st.session_state['first_name']}!</h1>
<p>Manage your schedule and optimize your delivery routes.</p>
</div>
""", unsafe_allow_html=True)

# ---- Action Cards ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">🗓️</div>
        <div class="section-title">Availability Calendar</div>
        <p>View and update your driving schedule.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('View + Edit Calendar', use_container_width=True):
        st.switch_page('pages/23_Availability_Calendar.py')

with col2:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">🧭</div>
        <div class="section-title">Route Planner</div>
        <p>Plan efficient delivery routes.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Plan Your Route', use_container_width=True):
        st.switch_page('pages/24_Route_Planner.py')

with col3:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">💬</div>
        <div class="section-title">Order Management</div>
        <p>Plan efficient delivery routes.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Order Management', use_container_width=True):
        st.switch_page('pages/29_Driver_Chat.py')

# ---- Footer ----
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; padding: 1rem;">
🚚 Delivering freshness, faster and smarter.
</div>
""", unsafe_allow_html=True)





