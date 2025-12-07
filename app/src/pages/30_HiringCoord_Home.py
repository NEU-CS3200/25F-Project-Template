import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role
SideBarLinks()

st.title('Hiring Coordinator Home')
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Manage Job Postings',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Manage_Postings.py')

if st.button('View Platform Analytics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Platform_Analytics.py')

if st.button('Create New Job Posting',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Create_Posting.py')