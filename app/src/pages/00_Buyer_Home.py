import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Buyer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Products', 
             type='primary',
             use_container_width=True, 
             icon="🛒"):
  st.switch_page('pages/01_Shop_Products.py')

if st.button('View Order History', 
             type='primary',
             use_container_width=True, 
             icon="📜"):
  st.switch_page('pages/02_View_Orders.py')

if st.button('View Messages', 
             type='primary',
             use_container_width=True, 
             icon="📨"):
  st.switch_page('pages/03_Messages.py')
