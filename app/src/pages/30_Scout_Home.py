import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 🔍")
st.write('')
st.write('### Game Scout Dashboard')
st.write('Search players, view game footage, and manage scouting schedule.')

if st.button('Search Players',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Search_Players.py')

if st.button('Live Game Scout',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Live_Scout.py')

if st.button('Scouting Schedule',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Scout_Schedule.py')
