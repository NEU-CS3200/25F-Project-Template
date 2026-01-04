import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('🎥 Upload Highlight Videos')

player_id = st.session_state.get('user_id', 101)

st.write("### Add New Highlight Video")

with st.form("upload_video"):
    game_id = st.number_input("Game ID", min_value=1, value=1, help="Enter the game ID this video is from")
    url = st.text_input("Video URL", placeholder="https://youtube.com/watch?v=...")
    duration = st.number_input("Duration (seconds)", min_value=1, value=180)
    description = st.text_area("Description (optional)")

    if st.form_submit_button("Upload Video", type="primary"):
        if url and game_id:
            try:
                # Call API to upload video
                video_data = {
                    'gameID': int(game_id),
                    'URL': url,
                    'duration': int(duration)
                }

                response = requests.post(
                    f'http://web-api:4000/players/{player_id}/videos',
                    json=video_data
                )

                if response.status_code == 201:
                    st.success(f"Video uploaded successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Failed to upload video: {response.status_code}")

            except Exception as e:
                st.error(f"Error uploading video: {str(e)}")
        else:
            st.error("Please provide both Game ID and URL")

# Existing videos
st.write("---")
st.write("### My Highlight Videos")

try:
    # Get videos from API
    response = requests.get(f'http://web-api:4000/players/{player_id}/videos')

    if response.status_code == 200:
        videos_data = response.json()

        if videos_data:
            for video in videos_data:
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(f"**Video from Game #{video.get('gameID', 'Unknown')}**")
                    caption_text = f"Duration: {video.get('duration', 0)} seconds"
                    if 'date' in video:
                        caption_text += f" | Date: {video['date']}"
                    if 'opponent' in video:
                        caption_text += f" | vs {video['opponent']}"
                    st.caption(caption_text)

                with col2:
                    st.link_button("View", video['URL'])

                with col3:
                    if st.button("Delete", key=f"del_{video.get('footageID', video.get('gameID'))}"):
                        st.warning("Delete functionality requires DELETE endpoint implementation")

                st.write("---")
        else:
            st.info("No highlight videos uploaded yet. Upload your first video above!")

    else:
        st.error(f"Failed to load videos: {response.status_code}")

except Exception as e:
    st.error(f"Error loading videos: {str(e)}")
    # Show sample data as fallback
    st.info("Showing sample data")

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

# Upload tips
st.write("---")
st.write("### 📌 Upload Tips")
st.info("""
- Upload videos from YouTube, Vimeo, or other video platforms
- Make sure the video is public or unlisted
- Include key plays and highlights from your games
- Scouts will be able to view and provide feedback on your videos
""")
