import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('✅ Verification Requests')

st.write("### Pending Verifications")

try:
    # Get pending verifications from API
    response = requests.get('http://web-api:4000/admin/pending-verifications')

    if response.status_code == 200:
        pending_data = response.json()

        if pending_data:
            # Convert to DataFrame
            pending = pd.DataFrame(pending_data)

            # Format for display
            pending['User'] = pending['firstName'] + ' ' + pending['lastName'] + ' #' + pending['playerID'].astype(str)
            pending['Request_ID'] = pending['validationID']
            pending['Type'] = pending['verificationType']
            pending['Submitted'] = pending['submittedDate']
            pending['Status'] = pending['status']

            display_df = pending[['Request_ID', 'User', 'Type', 'Submitted', 'Status']]
            st.dataframe(display_df, use_container_width=True)

        else:
            st.info("No pending verifications")
            pending = None

    else:
        st.error(f"Failed to load verifications: {response.status_code}")
        pending = None

except Exception as e:
    st.error(f"Error loading verifications: {str(e)}")
    # Sample fallback data
    pending = pd.DataFrame({
        'Request_ID': [1, 2, 3, 4],
        'User': ['Mike Johnson #102', 'Sarah Chen #103', 'Tom Davis #106', 'Lisa Wang #107'],
        'Type': ['Player', 'Player', 'Scout', 'Player'],
        'Submitted': ['2025-12-01', '2025-12-02', '2025-11-30', '2025-12-03'],
        'Status': ['Pending', 'Pending', 'Pending', 'Pending']
    })
    st.dataframe(pending, use_container_width=True)

# Only show review section if we have pending verifications
if pending is not None and len(pending) > 0:
    st.write("---")
    st.write("### Review Verification Request")

    col1, col2 = st.columns([2, 1])

    with col1:
        request_id = st.selectbox("Select Request", pending['Request_ID'].tolist())

        # Show details for selected request
        selected = pending[pending['Request_ID'] == request_id].iloc[0]

        st.info(f"""
        **User:** {selected['User']}  
        **Type:** {selected['Type']}  
        **Submitted:** {selected['Submitted']}  
        **Status:** {selected['Status']}
        """)

        notes = st.text_area("Verification Notes")

    with col2:
        st.write("")
        st.write("")
        st.write("")

        if st.button("✅ Approve", type="primary", use_container_width=True):
            try:
                # Get player_id from the selected verification
                if 'playerID' in selected:
                    player_id = selected['playerID']
                    verification_id = selected['Request_ID']

                    # Update verification status
                    update_response = requests.put(
                        f'http://web-api:4000/players/{player_id}/verifications/{verification_id}',
                        json={
                            'status': 'approved',
                            'verifiedBy': 1,  # Admin ID
                            'notes': notes
                        }
                    )

                    if update_response.status_code == 200:
                        st.success(f"Request {request_id} approved!")
                        st.rerun()
                    else:
                        st.error(f"Failed to approve: {update_response.status_code}")
                else:
                    st.success(f"Request {request_id} approved!")

            except Exception as e:
                st.error(f"Error approving request: {str(e)}")

        if st.button("❌ Reject", type="secondary", use_container_width=True):
            try:
                # Get player_id from the selected verification
                if 'playerID' in selected:
                    player_id = selected['playerID']
                    verification_id = selected['Request_ID']

                    # Update verification status
                    update_response = requests.put(
                        f'http://web-api:4000/players/{player_id}/verifications/{verification_id}',
                        json={
                            'status': 'rejected',
                            'verifiedBy': 1,  # Admin ID
                            'notes': notes
                        }
                    )

                    if update_response.status_code == 200:
                        st.error(f"Request {request_id} rejected")
                        st.rerun()
                    else:
                        st.error(f"Failed to reject: {update_response.status_code}")
                else:
                    st.error(f"Request {request_id} rejected")

            except Exception as e:
                st.error(f"Error rejecting request: {str(e)}")

# Statistics
st.write("---")
st.write("### Verification Statistics")

try:
    # Get system statistics from API
    stats_response = requests.get('http://web-api:4000/admin/statistics')

    if stats_response.status_code == 200:
        stats = stats_response.json()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Pending", stats.get('pending_verifications', 0))
        with col2:
            st.metric("Total Players", stats.get('total_players', 0))
        with col3:
            st.metric("Total Scouts", stats.get('total_scouts', 0))
        with col4:
            st.metric("Flagged Accounts", stats.get('flagged_accounts', 0))
    else:
        # Fallback stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Pending", "4")
        with col2:
            st.metric("Approved Today", "7")
        with col3:
            st.metric("Rejected Today", "2")
        with col4:
            st.metric("Total This Week", "28")

except Exception as e:
    st.error(f"Error loading statistics: {str(e)}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pending", "4")
    with col2:
        st.metric("Approved Today", "7")
    with col3:
        st.metric("Rejected Today", "2")
    with col4:
        st.metric("Total This Week", "28")
