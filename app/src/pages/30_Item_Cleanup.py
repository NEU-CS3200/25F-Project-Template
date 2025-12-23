import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
add_logo("assets/FitHublogo.png")

API_BASE = "http://api:4000/a"

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

.page-title {
    color: #328E6E;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.section-title {
    color: #328E6E;
    font-size: 26px;
    font-weight: 600;
    margin-top: 20px;
}

div.stButton > button {
    background-color: #328E6E;
    color: #E1EEBC;
    height: 3.5em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

div.stButton > button:hover {
    background-color: #2a7359;
}

</style>
""", unsafe_allow_html=True)


st.markdown('<div class="page-title">🧹 Item Cleanup Tools</div>', unsafe_allow_html=True)


# Remove Duplicate Items
st.markdown('<div class="section-title">Remove Duplicate Items</div>', unsafe_allow_html=True)

if st.button("Delete Duplicate Items", use_container_width=True):
    try:
        resp = requests.delete(f"{API_BASE}/items/duplicates")
        st.write(resp.json())
    except:
        st.error("Error deleting duplicate items.")


# Delete Specific Item
st.markdown('<div class="section-title">Delete Specific Item</div>', unsafe_allow_html=True)

item_id = st.number_input("Enter Item ID to Delete", min_value=1, step=1)

if st.button("Delete Item", use_container_width=True):
    try:
        resp = requests.delete(f"{API_BASE}/items/{item_id}")
        st.write(resp.json())
    except:
        st.error("Error deleting item.")
