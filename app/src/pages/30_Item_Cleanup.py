import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Item Cleanup Tools")

API_BASE = "http://api:4000/a"

# ===============================
# USER STORY 6 — DELETE DUPLICATES
# ===============================
st.write("## Remove Duplicate Items")

if st.button("Delete Duplicate Items"):
    try:
        resp = requests.delete(f"{API_BASE}/items/duplicates")
        st.write(resp.json())
    except:
        st.error("Error deleting duplicate items.")

# ===============================
# USER STORY 6+1 — DELETE SPECIFIC ITEM
# ===============================
st.write("## Delete Specific Item")

item_id = st.number_input("Enter Item ID to Delete", min_value=1, step=1)

if st.button("Delete Item"):
    try:
        resp = requests.delete(f"{API_BASE}/items/{item_id}")
        st.write(resp.json())
    except:
        st.error("Error deleting item.")
