import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from datetime import date
import requests

st.set_page_config(layout="wide")
SideBarLinks()

if "customer_id" not in st.session_state:
    st.session_state["customer_id"] = 1

API_URL = "http://web-api:4000/c"

# -------- GET CUSTOMER ID --------
customer_id = st.session_state.get("customer_id")

if not customer_id:
    st.error("No customer ID found. Please log in again.")
    if st.button("Return to Home"):
        st.switch_page("Home.py")
    st.stop()

# ----------- STYLE -----------
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

# ------------ HEADER ------------
st.markdown("""
<div class="page-title">🥗 Meal Preferences</div>
<div class="subtitle">Update your dietary preferences, delivery schedule, meal quantity, and start date.</div>
""", unsafe_allow_html=True)


# ----------- DIETARY PREFS -----------
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


# ----------- DELIVERY PREFS -----------
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


# ----------- MEAL QUANTITY -----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Amount of Meals Per Delivery</div>", unsafe_allow_html=True)

    meals = st.number_input("Meals", min_value=1, max_value=20, value=5)

    st.markdown("</div>", unsafe_allow_html=True)


# ----------- START DATE -----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Select Start Date</div>", unsafe_allow_html=True)

    start_date = st.date_input("Start Date")

    st.markdown("</div>", unsafe_allow_html=True)


# ----------- CHAT BOX -----------
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


# ----------- SAVE PREFERENCES (API CONNECTED) -----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Save Your Preferences</div>", unsafe_allow_html=True)

    st.write("Click below to save your updated dietary and delivery preferences.")

    if st.button("💾 Save Preferences", use_container_width=True):

        # ---- Convert checkboxes to strings stored in DB ----
        dietary_list = []
        if vegetarian: dietary_list.append("Vegetarian")
        if vegan: dietary_list.append("Vegan")
        if gluten_free: dietary_list.append("Gluten Free")
        if high_protein: dietary_list.append("High Protein")
        if dairy_free: dietary_list.append("Dairy Free")
        if nut_free: dietary_list.append("Nut Free")

        dietaryPref_str = ", ".join(dietary_list) if dietary_list else "None"

        # Delivery frequency logic → choose ONE priority
        if once_week: delivery_pref = "Once a week"
        elif twice_week: delivery_pref = "Twice a week"
        elif every_other: delivery_pref = "Every other week"
        elif monthly: delivery_pref = "Monthly"
        else: delivery_pref = "Unspecified"

        # Nutrition goals: meals per delivery + start date
        nutritionGoals_str = f"{meals} meals per delivery, starts {start_date}"

        payload = {
            "dietaryPref": dietaryPref_str,
            "nutritionGoals": nutritionGoals_str
        }

        try:
            response = requests.put(
                f"{API_URL}/customer/{customer_id}",
                json=payload
            )

            if response.status_code == 200:
                st.success("Your preferences have been saved successfully! 🎉")
            else:
                st.error(f"Failed to save preferences: {response.text}")

        except Exception as e:
            st.error(f"Error connecting to API: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
