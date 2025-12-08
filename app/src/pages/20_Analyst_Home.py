import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 📊")
st.write('')
st.write('### Data Analyst Dashboard')
st.write('Access analytics, create custom metrics, and generate insights.')

if st.button('Performance Analytics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_Analytics_Dashboard.py')

if st.button('Custom Metrics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_Custom_Metrics.py')

if st.button('Export Data',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_Export_Data.py')