import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('👥 Manage User Profiles')

# Filter options
user_type = st.selectbox("User Type", ["Players", "Scouts"])

if user_type == "Players":
    st.write("### Player Accounts")

    # Sample player data
    players_data = pd.DataFrame({
        'ID': [101, 102, 103, 104, 105],
        'Name': ['Sean Lee', 'Mike Johnson', 'Sarah Chen', 'David Brown', 'Emily White'],
        'Email': ['sean@email.com', 'mike@email.com', 'sarah@email.com', 'david@email.com', 'emily@email.com'],
        'Status': ['Active', 'Active', 'Pending', 'Active', 'Suspended'],
        'Joined': ['2025-09-01', '2025-09-15', '2025-11-20', '2025-08-10', '2025-10-05']
    })

    st.dataframe(players_data, use_container_width=True)

    # Update player status
    st.write("---")
    st.write("### Update Player Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        player_id = st.number_input("Player ID", min_value=1, value=101)
    with col2:
        new_status = st.selectbox("New Status", ["Active", "Pending", "Suspended", "Banned"])
    with col3:
        st.write("")
        st.write("")
        if st.button("Update Status", type="primary"):
            st.success(f"Player {player_id} status updated to {new_status}")

else:  # Scouts
    st.write("### Scout Accounts")

    scouts_data = pd.DataFrame({
        'ID': [201, 202, 203],
        'Name': ['John Tukey', 'Sara Chin', 'Mark Wilson'],
        'Email': ['john@scout.com', 'sara@scout.com', 'mark@scout.com'],
        'Role': ['Data Analyst', 'Game Scout', 'Senior Scout'],
        'Status': ['Active', 'Active', 'Active'],
        'Verified': ['Yes', 'Yes', 'Pending']
    })

    st.dataframe(scouts_data, use_container_width=True)

# Delete user
st.write("---")
st.write("### Remove User")

col1, col2 = st.columns([2, 1])

with col1:
    delete_id = st.number_input("User ID to Remove", min_value=1)
    reason = st.text_input("Reason for removal")

with col2:
    st.write("")
    st.write("")
    if st.button("⚠️ Remove User", type="secondary"):
        if reason:
            st.error(f"User {delete_id} has been removed. Reason: {reason}")
        else:
            st.warning("Please provide a reason for removal")