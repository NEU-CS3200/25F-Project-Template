import streamlit as st
from modules.nav import SideBarLinks

# Athentification and Role check
if not st.session_state.get('authenticated'):
    st.switch_page('Home.py')

if st.session_state.get('role') != 'administrator':
    st.switch_page('Home.py')

# ----------------
# Page content
# ----------------
SideBarLinks()
st.title("System Statistics & Metrics")
st.write("Platform metrics will be shown here")