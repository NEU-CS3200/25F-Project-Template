import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Alumni, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Your Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Alumni_Profile.py')

if st.button('View Student Profiles', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Student_Profiles.py')

if st.button('Configure your availability', type='primary', 
                                            use_container_width=True):
  st.switch_page('pages/03_Alumni_Availability.py')