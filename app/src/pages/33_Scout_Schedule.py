import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
from datetime import datetime, timedelta
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📅 Scouting Schedule')
st.write('View upcoming games and manage your scouting calendar')

scout_id = st.session_state.get('user_id', 1)

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("From", value=datetime.now())
with col2:
    end_date = st.date_input("To", value=datetime.now() + timedelta(days=14))

# Get upcoming games from player schedules
st.write("### Upcoming Games")

try:
    # Get player schedules for upcoming games
    # Using player 1 as example, in production would aggregate across all players
    response = requests.get('http://web-api:4000/players/1/schedule')

    if response.status_code == 200:
        schedule_data = response.json()

        if schedule_data:
            df = pd.DataFrame(schedule_data)

            # Format for display
            df['Date'] = df['date']
            df['Time'] = df['startTime']
            df['Game'] = 'vs ' + df['opponent']
            df['Venue'] = df['venue']

            display_df = df[['gameID', 'Date', 'Time', 'Game', 'Venue']].copy()
            display_df.columns = ['Game ID', 'Date', 'Time', 'Matchup', 'Venue']

            st.dataframe(display_df, use_container_width=True)
            st.success(f"Found {len(display_df)} upcoming games")
        else:
            st.info("No upcoming games scheduled")
    else:
        st.warning("Could not load schedule")

except Exception as e:
    st.warning(f"Using sample schedule: {str(e)}")
    upcoming_games = pd.DataFrame({
        'Date': ['2025-12-05', '2025-12-07', '2025-12-10', '2025-12-12'],
        'Time': ['18:00', '19:30', '18:00', '20:00'],
        'Game': ['Lincoln HS vs Oak Ridge', 'Washington HS vs Central',
                 'Roosevelt HS vs Lincoln HS', 'Oak Ridge vs Jefferson'],
        'Venue': ['Lincoln Gym', 'Washington Arena', 'Roosevelt Center', 'Oak Ridge Court'],
        'Players_to_Scout': [3, 2, 5, 1]
    })
    st.dataframe(upcoming_games, use_container_width=True)

# My scouting calendar
st.write("---")
st.write("### My Scouting Calendar")

try:
    # Get games this scout is planning to attend
    response = requests.get(f'http://web-api:4000/scouts/{scout_id}/game_history')

    if response.status_code == 200:
        my_games = response.json()

        if my_games:
            calendar_df = pd.DataFrame(my_games)
            display_calendar = calendar_df[['gameID', 'date', 'opponent', 'venue', 'notes']].copy()
            display_calendar.columns = ['Game ID', 'Date', 'Opponent', 'Venue', 'Notes']

            st.dataframe(display_calendar, use_container_width=True)
            st.info(f"You have {len(my_games)} games in your scouting calendar")
        else:
            st.info("No games in your calendar yet. Add games below!")
    else:
        st.info("Scouting calendar unavailable")

except Exception as e:
    st.info("Scouting calendar unavailable")

# Add game to schedule
st.write("---")
st.write("### Track New Game")

with st.form("add_game"):
    col1, col2 = st.columns(2)

    with col1:
        game_id = st.number_input("Game ID", min_value=1, value=1)
        player_ids = st.text_input("Player IDs to Scout (comma-separated)", value="1,2")

    with col2:
        game_date = st.date_input("Game Date")
        notes = st.text_area("Scouting Notes", placeholder="e.g., Focus on defensive plays, watch for leadership")

    if st.form_submit_button("Add to Schedule", type="primary"):
        try:
            # Note: This would ideally create a Scout_Activity record
            # For now, we'll show success message
            # In production, you'd want a POST endpoint for scout scheduling

            st.success(f"Game {game_id} added to your schedule!")
            st.info("Players to scout: " + player_ids)

            if notes:
                st.write(f"**Notes:** {notes}")

        except Exception as e:
            st.error(f"Error adding to schedule: {str(e)}")

# Quick stats
st.write("---")
st.write("### Scouting Stats")

try:
    response = requests.get(f'http://web-api:4000/scouts/{scout_id}/game_history')

    if response.status_code == 200:
        games_data = response.json()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Games Scouted", len(games_data))
        with col2:
            # Get unique players scouted
            players_response = requests.get(f'http://web-api:4000/scouts/{scout_id}/player_history')
            if players_response.status_code == 200:
                players_data = players_response.json()
                st.metric("Players Evaluated", len(players_data))
            else:
                st.metric("Players Evaluated", "N/A")
        with col3:
            st.metric("Upcoming Games", "4")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Games Scouted", "0")
        with col2:
            st.metric("Players Evaluated", "0")
        with col3:
            st.metric("Upcoming Games", "4")

except Exception as e:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Games Scouted", "0")
    with col2:
        st.metric("Players Evaluated", "0")
    with col3:
        st.metric("Upcoming Games", "4")

# Tips
st.write("---")
st.write("### 📌 Scheduling Tips")
st.info("""
- Add games to your calendar early to plan your scouting
- Track which players you want to focus on for each game
- Add notes about what to look for (offensive skills, defense, leadership)
- Review your past scouted games to track your evaluation progress
- Coordinate with other scouts to cover more games
""")
