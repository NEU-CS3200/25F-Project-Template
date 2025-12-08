import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('🎥 Upload Highlight Videos')

player_id = st.session_state.get('user_id', 101)

st.write("### Add New Highlight Video")

with st.form("upload_video"):
    title = st.text_input("Video Title", placeholder="e.g., 'AAU Semifinal Highlights'")
    url = st.text_input("Video URL", placeholder="https://youtube.com/watch?v=...")
    game_date = st.date_input("Game Date")
    description = st.text_area("Description (optional)")

    if st.form_submit_button("Upload Video", type="primary"):
        if title and url:
            st.success(f"Video '{title}' uploaded successfully!")
        else:
            st.error("Please provide both title and URL")

# Existing videos
st.write("---")
st.write("### My Highlight Videos")

import pandas as pd

videos = pd.DataFrame({
    'Title': ['AAU Championship Game', 'Season Highlights 2024', 'Defensive Plays Mix'],
    'Date': ['2025-11-20', '2025-11-10', '2025-10-15'],
    'Views': [245, 532, 128],
    'URL': ['https://youtube.com/1', 'https://youtube.com/2', 'https://youtube.com/3']
})

for idx, row in videos.iterrows():
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"**{row['Title']}**")
        st.caption(f"Uploaded: {row['Date']} | Views: {row['Views']}")
    with col2:
        st.link_button("View", row['URL'])
    with col3:
        if st.button("Delete", key=f"del_{idx}"):
            st.warning("Delete functionality here")
    st.write("---")