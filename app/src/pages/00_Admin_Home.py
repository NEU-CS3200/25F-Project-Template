import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 👋")
st.write('')
st.write('### System Administrator Dashboard')
st.write('Manage users, verify accounts, and monitor platform activity.')

if st.button('Manage User Profiles',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Manage_Users.py')

if st.button('Verification Requests',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Verifications.py')

if st.button('Platform Reports',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_Reports.py')
