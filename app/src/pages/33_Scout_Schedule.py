import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📅 Scouting Schedule')
st.write('View upcoming games and manage your scouting calendar')

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("From", value=datetime.now())
with col2:
    end_date = st.date_input("To", value=datetime.now() + timedelta(days=14))

# Sample upcoming games
upcoming_games = pd.DataFrame({
    'Date': ['2025-12-05', '2025-12-07', '2025-12-10', '2025-12-12'],
    'Time': ['18:00', '19:30', '18:00', '20:00'],
    'Game': ['Lincoln HS vs Oak Ridge', 'Washington HS vs Central',
             'Roosevelt HS vs Lincoln HS', 'Oak Ridge vs Jefferson'],
    'Venue': ['Lincoln Gym', 'Washington Arena', 'Roosevelt Center', 'Oak Ridge Court'],
    'Players_to_Scout': [3, 2, 5, 1]
})

st.write("### Upcoming Games")
st.dataframe(upcoming_games, use_container_width=True)

# Add game to schedule
st.write("---")
st.write("### Track New Game")

with st.form("add_game"):
    col1, col2 = st.columns(2)

    with col1:
        game_id = st.number_input("Game ID", min_value=1)
        player_id = st.number_input("Player ID to Scout", min_value=1)

    with col2:
        game_date = st.date_input("Game Date")
        notes = st.text_input("Notes")

    if st.form_submit_button("Add to Schedule", type="primary"):
        st.success(f"Game {game_id} added to your schedule!")
        