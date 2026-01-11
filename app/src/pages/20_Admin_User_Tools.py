import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

API_BASE = "http://api:4000/a"

st.title("User Management")

col_left, col_right = st.columns([1, 1])

with col_left:

    st.subheader("Update User Role")

    user_id_role = st.text_input("“Enter ID”", key="role_user_id")

    st.write("")  # spacing

    # Role buttons (Figma style)
    role_selected = st.radio(
        "Select Role",
        ["Admin", "User", "Analyst"],
        label_visibility="collapsed"
    )

    # Convert Figma labels → backend values
    role_map = {
        "Admin": "admin",
        "User": "user",
        "Analyst": "worker"  # your DB role
    }

    chosen_role = role_map[role_selected]

    st.write("")  # spacing

    if st.button("Update Roles", use_container_width=True):
        if not user_id_role:
            st.error("Please enter a User ID.")
        else:
            try:
                payload = {"role": chosen_role}
                response = requests.put(
                    f"{API_BASE}/users/{user_id_role}/role",
                    json=payload
                )
                if response.status_code == 200:
                    st.success("User role updated successfully!")
                else:
                    st.error(f"Failed to update role: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {e}")


with col_right:

    st.subheader("")

    user_id_deactivate = st.text_input("“Enter ID”", key="deactivate_user_id")

    st.write("")

    if st.button("Deactivate User", use_container_width=True):
        if not user_id_deactivate:
            st.error("Please enter a User ID.")
        else:
            try:
                response = requests.put(
                    f"{API_BASE}/users/{user_id_deactivate}/deactivate"
                )
                if response.status_code == 200:
                    st.success("User deactivated successfully!")
                else:
                    st.error(f"Failed to deactivate user: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {e}")
