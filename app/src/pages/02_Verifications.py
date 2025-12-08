import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('✅ Verification Requests')

st.write("### Pending Verifications")

# Sample verification requests
pending = pd.DataFrame({
    'Request_ID': [1, 2, 3, 4],
    'User': ['Mike Johnson #102', 'Sarah Chen #103', 'Tom Davis #106', 'Lisa Wang #107'],
    'Type': ['Player', 'Player', 'Scout', 'Player'],
    'Submitted': ['2025-12-01', '2025-12-02', '2025-11-30', '2025-12-03'],
    'Status': ['Pending', 'Pending', 'Pending', 'Pending']
})

st.dataframe(pending, use_container_width=True)

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
        st.success(f"Request {request_id} approved!")

    if st.button("❌ Reject", type="secondary", use_container_width=True):
        st.error(f"Request {request_id} rejected")

# Statistics
st.write("---")
st.write("### Verification Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Pending", "4")
with col2:
    st.metric("Approved Today", "7")
with col3:
    st.metric("Rejected Today", "2")
with col4:
    st.metric("Total This Week", "28")