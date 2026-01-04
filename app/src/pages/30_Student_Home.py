import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Student')}!")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# Get current student ID from session state
current_student_id = int(st.session_state.get('user_id', 1))

# Quick stats section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Connections", "5")
with col2:
    st.metric("Upcoming Sessions", "2")
with col3:
    st.metric("Connection Requests", "3 Pending")

st.write('')
st.write('')

# Main action buttons
if st.button('🔍 Browse Alumni Mentors', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Students_Browse_Alumni.py')

if st.button('📅 My Sessions', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Students_My_Sessions.py')

if st.button('👤 My Profile', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Students_My_Profile.py')

# Recent activity section
st.write('')
st.write('')
st.write('### 📌 Recent Activity')
st.info('✅ Connection accepted by John Doe (Software Engineer at Google)')
st.info('📅 Upcoming session with Jane Smith on Dec 15, 2024 at 2:00 PM')
st.info('💬 New message from Mike Johnson')