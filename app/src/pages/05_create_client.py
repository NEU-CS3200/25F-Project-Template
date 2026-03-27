import streamlit as st
import requests
import logging
logger = logging.getLogger(__name__)

API_BASE = "http://web-api:4000/system_admin"

st.title("Create Client Profile")

user_id = st.number_input("User ID", min_value=1)
first = st.text_input("First Name")
last = st.text_input("Last Name")
dob = st.date_input("Date of Birth")
fitness = st.text_input("Fitness Level")
goals = st.text_input("Goals")

if st.button("Create Client"):
    payload = {
        "user_id": user_id,
        "first_name": first,
        "last_name": last,
        "date_of_birth": str(dob),
        "fitness_level": fitness,
        "goals": goals
    }

    resp = requests.post(f"{API_BASE}/client", json=payload)

    if resp.status_code == 201:
        st.success("Client profile created!")
        st.json(resp.json())
    else:
        st.error(resp.json())

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/00_Sys_Admin_home.py")
