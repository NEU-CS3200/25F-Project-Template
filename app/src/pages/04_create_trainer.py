import streamlit as st
import requests
import logging
logger = logging.getLogger(__name__)

API_BASE = "http://web-api:4000/system_admin"

st.title("Create Trainer Profile")

user_id = st.number_input("User ID", min_value=1)
first = st.text_input("First Name")
last = st.text_input("Last Name")
cert = st.text_input("Certification")
spec = st.text_input("Specialization")

if st.button("Create Trainer Profile"):
    payload = {
        "user_id": user_id,
        "first_name": first,
        "last_name": last,
        "certification": cert,
        "specialization": spec
    }

    resp = requests.post(f"{API_BASE}/trainer", json=payload)

    if resp.status_code == 201:
        st.success("Trainer profile created!")
        st.json(resp.json())
    else:
        st.error(resp.json())

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/00_Sys_Admin_home.py")
