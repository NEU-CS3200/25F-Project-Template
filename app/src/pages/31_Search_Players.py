import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('🔍 Search Players')
st.write('Find players based on specific criteria')

# Search filters
col1, col2, col3 = st.columns(3)

with col1:
    position = st.selectbox("Position", ["All", "Guard", "Forward", "PG", "SG", "SF", "PF", "C"])
with col2:
    min_height = st.number_input("Min Height (inches)", min_value=60, max_value=90, value=70)
with col3:
    min_points = st.number_input("Min PPG", min_value=0, max_value=50, value=0)

if st.button("Search", type='primary'):
    try:
        # Build query parameters
        params = {'min_points': min_points}
        if position != "All":
            params['position'] = position

        # Get players from aggregate stats API
        response = requests.get('http://api:4000/players/stats/aggregate', params=params)

        if response.status_code == 200:
            players = response.json()

            if players:
                df = pd.DataFrame(players)

                # Format data for display
                df['Player'] = df['firstName'] + ' ' + df['lastName']
                df['Position'] = df.get('position', 'N/A')
                df['Team'] = df.get('team_name', 'N/A')
                df['PPG'] = pd.to_numeric(df['avg_points'], errors='coerce')
                df['APG'] = pd.to_numeric(df['avg_assists'], errors='coerce')
                df['RPG'] = pd.to_numeric(df['avg_rebounds'], errors='coerce')
                df['Games'] = df['games_played']

                # Apply height filter if we need to get full player profiles
                if min_height > 70:
                    # Get detailed player info for height filtering
                    filtered_players = []
                    for player_id in df['playerID'].tolist():
                        try:
                            player_response = requests.get(f'http://api:4000/players/{player_id}')
                            if player_response.status_code == 200:
                                player_data = player_response.json()
                                if player_data.get('height', 0) >= min_height:
                                    filtered_players.append(player_id)
                        except:
                            pass

                    if filtered_players:
                        df = df[df['playerID'].isin(filtered_players)]
                    else:
                        st.info("No players found matching height criteria")
                        df = pd.DataFrame()

                if len(df) > 0:
                    st.success(f"Found {len(df)} players matching criteria")

                    # Display results
                    display_df = df[['Player', 'Position', 'Team', 'PPG', 'APG', 'RPG', 'Games']].copy()
                    st.dataframe(display_df, use_container_width=True)

                    # Show detailed view option
                    st.write("---")
                    st.write("### Player Details")

                    selected_player = st.selectbox(
                        "Select player for details",
                        df['playerID'].tolist(),
                        format_func=lambda x: df[df['playerID'] == x]['Player'].iloc[0]
                    )

                    if st.button("View Full Profile"):
                        try:
                            profile_response = requests.get(f'http://api:4000/players/{selected_player}')

                            if profile_response.status_code == 200:
                                profile = profile_response.json()

                                col1, col2 = st.columns(2)

                                with col1:
                                    st.write("**Personal Info:**")
                                    st.write(f"Name: {profile.get('firstName')} {profile.get('lastName')}")
                                    st.write(f"Email: {profile.get('email')}")
                                    st.write(f"Phone: {profile.get('phone_Number', 'N/A')}")
                                    st.write(f"Height: {profile.get('height', 'N/A')} inches")
                                    st.write(f"Weight: {profile.get('weight', 'N/A')} lbs")

                                with col2:
                                    st.write("**Team Info:**")
                                    st.write(f"Team: {profile.get('team_name', 'N/A')}")
                                    st.write(f"Position: {profile.get('position', 'N/A')}")
                                    st.write(f"Jersey: #{profile.get('jerseyNumber', 'N/A')}")
                                    st.write(f"Status: {profile.get('AcctStatus', 'N/A')}")

                                if profile.get('UserBio'):
                                    st.write("**Bio:**")
                                    st.info(profile['UserBio'])
                            else:
                                st.error("Could not load player profile")
                        except Exception as e:
                            st.error(f"Error loading profile: {str(e)}")
                else:
                    st.info("No players found matching criteria. Try adjusting filters.")
            else:
                st.info("No players in database yet")
        else:
            st.error(f"API Error: {response.status_code}")

    except Exception as e:
        st.error(f"Could not connect to API: {str(e)}")

        # Show sample data
        st.info("Showing sample data for demonstration:")
        sample_data = {
            'Player': ['LeBron James', 'Stephen Curry', 'Kevin Durant'],
            'Position': ['Forward', 'Guard', 'Forward'],
            'Team': ['Lakers', 'Warriors', 'Nets'],
            'PPG': [28.5, 32.1, 26.8],
            'APG': [7.1, 6.8, 5.2],
            'RPG': [8.2, 5.1, 7.8],
            'Games': [25, 28, 24]
        }
        st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

# Quick stats
st.write("---")
st.write("### Search Tips")
st.info("""
- Use filters to narrow down your search
- Minimum PPG helps find top scorers
- Height filter useful for position-specific scouting
- Click on a player to see their full profile
- Results show current season averages
""")
