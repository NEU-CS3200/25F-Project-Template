import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📹 Live Game Scout')
st.write('Tag and annotate plays during live games')

# Game selection
game_id = st.number_input("Game ID", min_value=1, value=1)

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### Game Feed")
    st.info("Live game video would appear here")

    # Simulated game info
    st.write("**Lincoln HS vs Washington HS**")
    st.write("Q1 - 01:25 | Score: 10-8")

with col2:
    st.write("### Quick Tags")

    tag_buttons = st.columns(3)
    with tag_buttons[0]:
        if st.button("Fast Break", use_container_width=True):
            st.success("Tagged!")
    with tag_buttons[1]:
        if st.button("Assist", use_container_width=True):
            st.success("Tagged!")
    with tag_buttons[2]:
        if st.button("Rebound", use_container_width=True):
            st.success("Tagged!")

# Annotation form
st.write("---")
st.write("### Add Annotation")

with st.form("annotation_form"):
    player_id = st.number_input("Player ID", min_value=1)
    timestamp = st.text_input("Timestamp (MM:SS)", value="00:00")
    note = st.text_area("Notes")

    if st.form_submit_button("Save Annotation", type="primary"):
        st.success("Annotation saved!")

# Recent annotations
st.write("---")
st.write("### Recent Annotations")

annotations = [
    {"Player": "Sarah Johnson #23", "Time": "00:37", "Note": "Great defensive rotation"},
    {"Player": "Mike Chen #15", "Time": "02:15", "Note": "Excellent court vision on assist"}
]

import pandas as pd

st.dataframe(pd.DataFrame(annotations), use_container_width=True)