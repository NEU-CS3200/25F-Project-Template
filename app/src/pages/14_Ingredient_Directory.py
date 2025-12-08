import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

API_URL = "http://web-api:4000"

st.write("# Accessing Farmer Inventory")

with st.form('farmer_id'): 

    col1, spacer1, spacer2 = st.columns([1, 2, 2])
    farmerID = col1.number_input("Farmer ID", min_value=1, step=1)
    submit = st.form_submit_button("Submit")

if submit: 
    try:
        response = requests.get(f"{API_URL}/f/farmers/{int(farmerID)}/inventory")

        if response.status_code == 200:
            inventory = response.json()
            st.success(f"Found {len(inventory)} inventory entries.")
            st.table(inventory)  # display table

        elif response.status_code == 404:
            st.warning("No inventory found for this farmer.")

        else:
            st.error(f"Error: {response.json().get('error')}")

    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")