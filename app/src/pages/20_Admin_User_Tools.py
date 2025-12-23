import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

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
    margin-bottom: 10px;
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

st.markdown('<div class="page-title">Admin: User Management</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

# UPDATE USER ROLE
with col1:
    st.markdown('<div class="section-title">Update User Role</div>', unsafe_allow_html=True)

    user_id = st.number_input("User ID:", step=1, min_value=1)

    new_role = st.selectbox(
        "Select Role",
        ["admin", "user", "worker"]
    )

    if st.button("Update Role", use_container_width=True):
        logger.info(f"Updating role for user {user_id} → {new_role}")
        try:
            response = requests.put(
                f"{API_BASE}/users/{int(user_id)}/role",
                json={"role": new_role}
            )
            st.write(response.json())
        except:
            st.error("Could not update role.")


# DEACTIVATE USER
with col2:
    st.markdown('<div class="section-title">Deactivate User</div>', unsafe_allow_html=True)

    deactivate_user_id = st.number_input("User ID to Deactivate:", step=1, min_value=1)

    if st.button("Deactivate User", use_container_width=True):
        logger.info(f"Deactivating user {deactivate_user_id}")
        try:
            response = requests.put(
                f"{API_BASE}/users/{int(deactivate_user_id)}/deactivate"
            )
            st.write(response.json())
        except:
            st.error("Could not deactivate user.")
