import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

# Style
st.markdown("""
<style>

.page-title {
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: .3rem;
}

.subtitle {
    font-size: 1.05rem;
    color: #444;
    margin-bottom: 1.2rem;
}

.card {
    background: white;
    padding: 1.4rem 1.6rem;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: .7rem;
}

.chat-msg {
    display: flex;
    align-items: center;
    gap: .6rem;
    margin-bottom: .5rem;
}

.chat-dot {
    color: #31d231;
    font-size: 1.2rem;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-title">🥗 Meal Preferences</div>
<div class="subtitle">Update your dietary preferences, delivery schedule, meal quantity, and start date.</div>
""", unsafe_allow_html=True)

# Dietary Preferences
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Dietary Preferences</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        vegetarian = st.checkbox("Vegetarian")
        vegan = st.checkbox("Vegan")
        gluten_free = st.checkbox("Gluten Free")

    with col2:
        high_protein = st.checkbox("High Protein")
        dairy_free = st.checkbox("Dairy Free")
        nut_free = st.checkbox("Nut Free")

    st.markdown("</div>", unsafe_allow_html=True)


# Delivery Preferences
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Delivery Preferences</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        once_week = st.checkbox("Once a week")
        every_other = st.checkbox("Every other week")

    with col2:
        twice_week = st.checkbox("Twice a week")
        monthly = st.checkbox("Monthly")

    st.markdown("</div>", unsafe_allow_html=True)


# Meals Per Delivery
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Amount of Meals Per Delivery</div>", unsafe_allow_html=True)

    meals = st.number_input("Meals", min_value=1, max_value=20, value=5)

    st.markdown("</div>", unsafe_allow_html=True)


# Start Date
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Select Start Date</div>", unsafe_allow_html=True)

    start_date = st.date_input("Start Date")

    st.markdown("</div>", unsafe_allow_html=True)


# Chat Section
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Chat</div>", unsafe_allow_html=True)

st.markdown("""
<div class='chat-msg'>
    <span class='chat-dot'>🟢</span> 
    <span>Hello! Let me know your meal preferences.</span>
</div>
<div class='chat-msg'>
    <span class='chat-dot'>🟢</span> 
    <span>You can update dietary choices or delivery frequency anytime.</span>
</div>
""", unsafe_allow_html=True)

st.text_input("Send a message:", placeholder="Type here...")

st.markdown("</div>", unsafe_allow_html=True)

# Save Preferences
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Save Your Preferences</div>", unsafe_allow_html=True)

    st.write("Click below to save your updated dietary and delivery preferences.")

    if st.button("💾 Save Preferences", use_container_width=True):

        # Collect all preferences into a Python dict
        preferences = {
            "dietary": {
                "vegetarian": vegetarian,
                "vegan": vegan,
                "gluten_free": gluten_free,
                "high_protein": high_protein,
                "dairy_free": dairy_free,
                "nut_free": nut_free
            },
            "delivery_frequency": {
                "once_week": once_week,
                "twice_week": twice_week,
                "every_other_week": every_other,
                "monthly": monthly
            },
            "meals_per_delivery": meals,
            "start_date": str(start_date)
        }

        st.success("Your preferences have been saved successfully! 🎉")

    st.markdown("</div>", unsafe_allow_html=True)
