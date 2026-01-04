import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 🏀")
st.write('')
st.write('### Player Dashboard')
st.write('Track your stats, upload highlights, and view scout feedback.')

if st.button('My Statistics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Player_Stats.py')

if st.button('Upload Highlights',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_Upload_Videos.py')

if st.button('Scout Feedback',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_View_Feedback.py')
