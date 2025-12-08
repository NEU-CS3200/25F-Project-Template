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
    background: linear-gradient(135deg, #E9F7EF, #F4FFF7);
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
    <h1>🌾 Welcome back, {st.session_state['first_name']}!</h1>
    <p>Manage your produce, track ingredients, and forecast demand.</p>
</div>
""", unsafe_allow_html=True)

# ---- Action Cards ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">🧺</div>
        <div class="section-title">Produce Editor</div>
        <p>Update and manage your available produce.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Open Produce Editor', use_container_width=True):
        st.switch_page('pages/11_Produce_Edit.py')

with col2:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">📁</div>
        <div class="section-title">Ingredient Directory</div>
        <p>Browse and manage available ingredients.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('View Ingredient Directory', use_container_width=True):
        st.switch_page('pages/14_Ingredient_Directory.py')

with col3:
    st.markdown("""
    <div class="action-card">
        <div class="action-icon">📊</div>
        <div class="section-title">Predict Demand</div>
        <p>Forecast future ingredient demand.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button('Predict Ingredient Demand', use_container_width=True):
        st.switch_page('pages/12_Ingredient_Predict.py')

# ---- Footer ----
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; padding: 1rem;">
    🌱 Helping you grow smarter, fresher, and faster.
</div>
""", unsafe_allow_html=True)