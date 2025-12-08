import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📊 My Statistics')

player_id = st.session_state.get('user_id', 101)

# Display season stats
st.write('### Season Statistics 2024-25')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Points Per Game", "18.5")
with col2:
    st.metric("Assists Per Game", "5.2")
with col3:
    st.metric("Rebounds Per Game", "6.8")
with col4:
    st.metric("Games Played", "15")

# Add new game stats
st.write("---")
st.write('### Add Game Statistics')

with st.form("add_stats_form"):
    col1, col2 = st.columns(2)

    with col1:
        game_id = st.number_input("Game ID", min_value=1)
        minutes = st.number_input("Minutes Played", min_value=0, max_value=48, value=30)
        points = st.number_input("Points", min_value=0, value=0)
        rebounds = st.number_input("Rebounds", min_value=0, value=0)

    with col2:
        assists = st.number_input("Assists", min_value=0, value=0)
        steals = st.number_input("Steals", min_value=0, value=0)
        blocks = st.number_input("Blocks", min_value=0, value=0)
        turnovers = st.number_input("Turnovers", min_value=0, value=0)

    submitted = st.form_submit_button("Submit Stats", type="primary")

    if submitted:
        st.success("Stats submitted successfully!")
        st.balloons()

# Recent games
st.write("---")
st.write("### Recent Games")

recent_games = pd.DataFrame({
    'Date': ['2025-11-30', '2025-11-27', '2025-11-23'],
    'Opponent': ['Oak Ridge HS', 'Central HS', 'Washington HS'],
    'Points': [22, 15, 19],
    'Rebounds': [7, 5, 8],
    'Assists': [6, 4, 5]
})

st.dataframe(recent_games, use_container_width=True)