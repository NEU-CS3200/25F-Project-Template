##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################
##################################################
##################################################
# Set up basic logging infrastructure
import logging, base64

# import the main streamlit library as well
from datetime import datetime
from streamlit.components.v1 import html
import streamlit as st
from modules.nav import SideBarLinks

# ----- Logging -----
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

# Reset auth for landing
st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

# ----- Helpers -----
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Background image (JPEG)
bg_img = get_base64("assets/homepage_background.png")

# ----- HERO SECTION -----
st.markdown(f"""
<style>
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.hero {{
    position: relative;
    height: 420px;
    overflow: hidden;
    border-radius: 18px;
}}

.hero img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.hero-text {{
    position: absolute;
    top: 45%;
    left: 10%;
    color: #31333E;
    font-size: 3.6rem;
    font-weight: 800;
    animation: fadeIn 0.6s ease-out forwards;
}}

.hero-sub {{
    position: absolute;
    top: 60%;
    left: 10%;
    color: #444;
    font-size: 1.2rem;
    max-width: 520px;
    animation: fadeIn 0.8s ease-out forwards;
}}

.role-card {{
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    background: white;
    transition: transform 0.2s ease;
}}

.role-card:hover {{
    transform: scale(1.03);
}}

.section-title {{
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 2rem 0 1rem;
}}
</style>

<div class="hero">
    <img src="data:image/jpeg;base64,{bg_img}">
    <div class="hero-text">Welcome to Fresh Route!</div>
    <div class="hero-text"></div>
    <div class="hero-sub">
    Farm-fresh ingredients and smart delivery — powered by data.</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ----- LOGIN CARDS -----
st.markdown("<div class='section-title'>Choose Your Role</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='role-card'> 🛒 Customer</div>", unsafe_allow_html=True)
    if st.button("Log in as Daniel", use_container_width=True):
        st.session_state.update({
            "authenticated": True,
            "role": "customer",
            "first_name": "Daniel"
        })
        st.switch_page("pages/00_Customer_Home.py")

with col2:
    st.markdown("<div class='role-card'> 🌱 Farmer</div>", unsafe_allow_html=True)
    if st.button("Log in as Maria", use_container_width=True):
        st.session_state.update({
            "authenticated": True,
            "role": "farmer",
            "first_name": "Maria"
        })
        st.switch_page("pages/10_Farmer_Home.py")

with col3:
    st.markdown("<div class='role-card'> 🚚 Driver</div>", unsafe_allow_html=True)
    if st.button("Log in as Bob", use_container_width=True):
        st.session_state.update({
            "authenticated": True,
            "role": "driver",
            "first_name": "Bob",
            "driver_id": 6  # Bob Johnson
        })
        st.switch_page("pages/22_Driver_Home.py")

with col4:
    st.markdown("<div class='role-card'> 🖥️ Admin</div>", unsafe_allow_html=True)
    if st.button("Log in as Lancy", use_container_width=True):
        st.session_state.update({
            "authenticated": True,
            "role": "administrator",
            "first_name": "Lancy"
        })
        st.switch_page("pages/25_Admin_Home.py")

st.divider()

# ----- FEATURE STRIP -----
feature_cols = st.columns(3)

features = [
    ("🌾", "Farm-Fresh Sourcing", "Direct from sustainable local farms."),
    ("📦", "Smart Delivery", "Optimized routes for speed and freshness."),
    ("📊", "Data-Driven Choices", "Real-time insights into your food system.")
]

for i, col in enumerate(feature_cols):
    with col:
        st.markdown(f"""
        <div class="role-card">
            <h4>{features[i][0]} {features[i][1]}</h4>
            <p>{features[i][2]}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ----- FOOTER CTA -----
st.markdown("""
<div style="text-align:center; padding:2rem;">
    <h2>Fresh food. Smarter routes. Better futures.</h2>
    <p>Built as a Northeastern University CS3200 project.</p>
</div>
""", unsafe_allow_html=True)