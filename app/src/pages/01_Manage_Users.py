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

    try:
        # Get all players from API
        response = requests.get('http://api:4000/admin/users?type=players')

        if response.status_code == 200:
            data = response.json()
            players = data.get('players', [])

            if players:
                # Convert to DataFrame
                players_df = pd.DataFrame(players)
                # Rename columns for display
                display_df = players_df[['id', 'firstName', 'lastName', 'email', 'status']].copy()
                display_df.columns = ['ID', 'First Name', 'Last Name', 'Email', 'Status']

                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No players found")
        else:
            st.error(f"Failed to load players: {response.status_code}")

    except Exception as e:
        st.error(f"Error loading players: {str(e)}")
        # Show sample data as fallback
        players_data = pd.DataFrame({
            'ID': [101, 102, 103, 104, 105],
            'Name': ['Sean Lee', 'Mike Johnson', 'Sarah Chen', 'David Brown', 'Emily White'],
            'Email': ['sean@email.com', 'mike@email.com', 'sarah@email.com', 'david@email.com', 'emily@email.com'],
            'Status': ['Active', 'Active', 'Pending', 'Active', 'Suspended']
        })
        st.dataframe(players_data, use_container_width=True)

    # Update player status
    st.write("---")
    st.write("### Update Player Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        player_id = st.number_input("Player ID", min_value=1, value=101)
    with col2:
        new_status = st.selectbox("New Status", ["active", "suspended", "inactive"])
    with col3:
        st.write("")
        st.write("")
        if st.button("Update Status", type="primary"):
            try:
                # Call API to update player status
                update_response = requests.put(
                    f'http://api:4000/admin/users/players/{player_id}/permissions',
                    json={'AcctStatus': new_status}
                )

                if update_response.status_code == 200:
                    st.success(f"Player {player_id} status updated to {new_status}")
                    st.rerun()
                else:
                    st.error(f"Failed to update status: {update_response.status_code}")
            except Exception as e:
                st.error(f"Error updating status: {str(e)}")

else:  # Scouts
    st.write("### Scout Accounts")

    try:
        # Get all scouts from API
        response = requests.get('http://api:4000/admin/users?type=scouts')

        if response.status_code == 200:
            data = response.json()
            scouts = data.get('scouts', [])

            if scouts:
                # Convert to DataFrame
                scouts_df = pd.DataFrame(scouts)
                display_df = scouts_df[['id', 'firstName', 'lastName', 'email', 'status']].copy()
                display_df.columns = ['ID', 'First Name', 'Last Name', 'Email', 'Status']

                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No scouts found")
        else:
            st.error(f"Failed to load scouts: {response.status_code}")

    except Exception as e:
        st.error(f"Error loading scouts: {str(e)}")
        # Show sample data as fallback
        scouts_data = pd.DataFrame({
            'ID': [201, 202, 203],
            'Name': ['John Tukey', 'Sara Chin', 'Mark Wilson'],
            'Email': ['john@scout.com', 'sara@scout.com', 'mark@scout.com'],
            'Role': ['Data Analyst', 'Game Scout', 'Senior Scout'],
            'Status': ['Active', 'Active', 'Active']
        })
        st.dataframe(scouts_data, use_container_width=True)

# Delete user
st.write("---")
st.write("### Remove User")

col1, col2 = st.columns([2, 1])

with col1:
    delete_id = st.number_input("User ID to Remove", min_value=1)
    delete_type = st.radio("User Type", ["player", "scout"])
    reason = st.text_input("Reason for removal")

with col2:
    st.write("")
    st.write("")
    if st.button("⚠️ Remove User", type="secondary"):
        if reason:
            try:
                # Call API to delete user
                if delete_type == "player":
                    delete_response = requests.delete(f'http://api:4000/players/{delete_id}')
                else:
                    delete_response = requests.delete(f'http://api:4000/scouts/{delete_id}')

                if delete_response.status_code == 200:
                    st.error(f"User {delete_id} has been removed. Reason: {reason}")
                    st.rerun()
                else:
                    st.error(f"Failed to remove user: {delete_response.status_code}")
            except Exception as e:
                st.error(f"Error removing user: {str(e)}")
        else:
            st.warning("Please provide a reason for removal")
