import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
from datetime import date

st.set_page_config(layout='wide')

# Call SideBarLinks to show navigation
SideBarLinks()

st.title('📊 My Statistics')

# Get player ID from session state
player_id = st.session_state.get('user_id', 1)

# Fetch season stats from API
st.write('### Season Statistics 2024-25')

try:
    # Call the aggregate stats endpoint
    response = requests.get('http://api:4000/players/stats/aggregate')

    if response.status_code == 200:
        all_stats = response.json()

        # Filter for current player
        player_stats = [p for p in all_stats if p['playerID'] == player_id]

        if player_stats:
            stats = player_stats[0]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Points Per Game", f"{float(stats['avg_points']):.1f}")
            with col2:
                st.metric("Assists Per Game", f"{float(stats['avg_assists']):.1f}")
            with col3:
                st.metric("Rebounds Per Game", f"{float(stats['avg_rebounds']):.1f}")
            with col4:
                st.metric("Games Played", int(stats['games_played']))
        else:
            st.warning(f"No season stats found for player ID {player_id}")
    else:
        st.error(f"API returned status code: {response.status_code}")

except Exception as e:
    st.error(f"Error loading season stats: {str(e)}")
    # Show placeholder data if API fails
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Points Per Game", "0.0")
    with col2:
        st.metric("Assists Per Game", "0.0")
    with col3:
        st.metric("Rebounds Per Game", "0.0")
    with col4:
        st.metric("Games Played", "0")

# Add new game stats
st.write("---")
st.write('### Add Game Statistics')
st.info("💡 Enter game details and your stats. The system will create the game record automatically.")

with st.form("add_stats_form"):
    # Game Information Section
    st.subheader("Game Information")
    col1, col2 = st.columns(2)

    with col1:
        game_date = st.date_input("Game Date", value=date.today(), max_value=date.today())
        opponent = st.text_input("Opponent Team", placeholder="e.g., Lakers")
        venue = st.text_input("Venue/Location", placeholder="e.g., Madison Square Garden")

    with col2:
        tournament = st.text_input("Tournament (Optional)", placeholder="e.g., AAU Championship")
        start_time = st.time_input("Start Time (Optional)", value=None)
        score = st.text_input("Final Score (Optional)", placeholder="e.g., 95-88")

    st.write("---")

    # Stats Section
    st.subheader("Your Game Statistics")
    col1, col2 = st.columns(2)

    with col1:
        minutes = st.number_input("Minutes Played", min_value=0, max_value=48, value=30)
        points = st.number_input("Points", min_value=0, value=0)
        rebounds = st.number_input("Rebounds", min_value=0, value=0)
        assists = st.number_input("Assists", min_value=0, value=0)
        steals = st.number_input("Steals", min_value=0, value=0)

    with col2:
        blocks = st.number_input("Blocks", min_value=0, value=0)
        turnovers = st.number_input("Turnovers", min_value=0, value=0)
        fouls = st.number_input("Fouls", min_value=0, value=0)
        three_pt = st.number_input("3-Pointers Made", min_value=0, value=0)

    submitted = st.form_submit_button("Submit Game & Stats", type="primary")

    if submitted:
        # Validate required fields
        if not opponent or not venue:
            st.error("⚠️ Please enter Opponent Team and Venue")
        else:
            try:
                # Prepare data for API
                game_and_stats_data = {
                    # Game information
                    'date': str(game_date),
                    'opponent': opponent,
                    'venue': venue,
                    'tournament': tournament if tournament else '',
                    'startTime': str(start_time) if start_time else '00:00:00',
                    'endTime': '00:00:00',  # Can add end time input if needed
                    'score': score if score else '',
                    # Player stats
                    'minutes': int(minutes),
                    'points': int(points),
                    'rebounds': int(rebounds),
                    'assists': int(assists),
                    'steals': int(steals),
                    'blocks': int(blocks),
                    'turnovers': int(turnovers),
                    'fouls': int(fouls),
                    'three_pt': int(three_pt)
                }

                # POST to NEW combined endpoint
                response = requests.post(
                    f'http://api:4000/players/{player_id}/game-and-stats',
                    json=game_and_stats_data
                )

                if response.status_code == 201:
                    result = response.json()
                    st.success(f"✅ Game and stats submitted successfully! Game ID: {result.get('gameID')}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Failed to submit stats. Status code: {response.status_code}")
                    st.error(f"Error details: {response.text}")

            except Exception as e:
                st.error(f"Error submitting stats: {str(e)}")

# Recent games - Fetch from API
st.write("---")
st.write("### Recent Games")

try:
    games_response = requests.get(f'http://api:4000/players/{player_id}/stats')

    if games_response.status_code == 200:
        games_data = games_response.json()

        if games_data:
            # Convert to DataFrame
            df = pd.DataFrame(games_data)

            # Select relevant columns for display
            if 'date' in df.columns:
                display_df = df[['date', 'opponent', 'venue', 'points', 'rebounds', 'assists']].copy()
                display_df.columns = ['Date', 'Opponent', 'Venue', 'Points', 'Rebounds', 'Assists']
            else:
                # If no date column, show what we have
                display_columns = ['points', 'rebounds', 'assists', 'steals', 'blocks']
                available_columns = [col for col in display_columns if col in df.columns]
                display_df = df[available_columns]

            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No game stats available yet. Add your first game above!")
    else:
        st.error(f"Failed to load recent games. Status code: {games_response.status_code}")

except Exception as e:
    st.error(f"Error loading recent games: {str(e)}")
