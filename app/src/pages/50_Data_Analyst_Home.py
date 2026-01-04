import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

first_name = st.session_state.get('first_name', 'Data Analyst')
st.title(f"Welcome, {first_name}!")
st.write('')
st.write('')
st.write('### What would you like to explore today?')

# Each button routes to a different analytics page for this persona
if st.button('View Majors & Participation Analytics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/51_Major_Analytics.py')

if st.button('View Match Rates & Engagement',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/52_Match_Analytics.py')

if st.button('View Top Mentors & Companies',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/53_Mentor_Company_Analytics.py')
