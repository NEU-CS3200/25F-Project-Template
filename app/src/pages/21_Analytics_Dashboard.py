import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📊 Performance Analytics Dashboard')

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    season = st.selectbox("Season", ["2024-25", "2023-24", "2022-23"])
with col2:
    league = st.selectbox("League", ["All", "AAU", "High School"])
with col3:
    position = st.selectbox("Position", ["All", "PG", "SG", "SF", "PF", "C", "Guard", "Forward"])

# Key metrics
st.write("---")
st.write("### League-Wide Statistics")

try:
    # Get aggregate stats from API
    position_filter = "" if position == "All" else f"?position={position}"
    response = requests.get(f'http://api:4000/players/stats/aggregate{position_filter}')

    if response.status_code == 200:
        stats_data = response.json()

        if stats_data:
            df = pd.DataFrame(stats_data)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                # Convert to float to handle Decimal types
                avg_points = pd.to_numeric(df['avg_points'], errors='coerce').mean()
                st.metric("Avg Points/Game", f"{avg_points:.1f}")
            with col2:
                avg_assists = pd.to_numeric(df['avg_assists'], errors='coerce').mean()
                st.metric("Avg Assists/Game", f"{avg_assists:.1f}")
            with col3:
                avg_rebounds = pd.to_numeric(df['avg_rebounds'], errors='coerce').mean()
                st.metric("Avg Rebounds/Game", f"{avg_rebounds:.1f}")
            with col4:
                st.metric("Players Analyzed", len(stats_data))
        else:
            # Fallback metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Points/Game", "18.7", "+2.3")
            with col2:
                st.metric("Avg Assists/Game", "5.4", "+0.8")
            with col3:
                st.metric("Avg Rebounds/Game", "7.2", "-0.3")
            with col4:
                st.metric("Players Analyzed", "0")
    else:
        st.error(f"Failed to load statistics: {response.status_code}")

except Exception as e:
    st.error(f"Error loading statistics: {str(e)}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Points/Game", "18.7", "+2.3")
    with col2:
        st.metric("Avg Assists/Game", "5.4", "+0.8")
    with col3:
        st.metric("Avg Rebounds/Game", "7.2", "-0.3")
    with col4:
        st.metric("Players Analyzed", "847")

# Performance distribution
st.write("---")
st.write("### Points Per Game Distribution")

try:
    response = requests.get('http://api:4000/players/stats/aggregate')

    if response.status_code == 200:
        stats_data = response.json()

        if stats_data:
            ppg_df = pd.DataFrame(stats_data)
            ppg_df['Points_Per_Game'] = pd.to_numeric(ppg_df['avg_points'], errors='coerce')

            fig = px.histogram(ppg_df, x='Points_Per_Game',
                               title='Distribution of Points Per Game',
                               labels={'Points_Per_Game': 'Points Per Game'},
                               nbins=15)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for distribution")
    else:
        st.warning("Using sample distribution data")

except Exception as e:
    st.warning(f"Using sample distribution data: {str(e)}")
    ppg_data = pd.DataFrame({
        'Points_Per_Game': [12, 15, 18, 21, 14, 16, 19, 22, 13, 17, 20, 23,
                            11, 14, 18, 21, 15, 19, 24, 16, 13, 17, 20, 25]
    })
    fig = px.histogram(ppg_data, x='Points_Per_Game',
                       title='Distribution of Points Per Game',
                       labels={'Points_Per_Game': 'Points Per Game'},
                       nbins=20)
    st.plotly_chart(fig, use_container_width=True)

# Top performers
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.write("### Top Scorers")

    try:
        response = requests.get('http://api:4000/players/stats/aggregate?min_points=0')

        if response.status_code == 200:
            stats_data = response.json()

            if stats_data:
                df = pd.DataFrame(stats_data)
                df['Player'] = df['firstName'] + ' ' + df['lastName']
                df['PPG'] = pd.to_numeric(df['avg_points'], errors='coerce')
                df['Games'] = df['games_played']

                top_scorers = df.nlargest(5, 'PPG')[['Player', 'PPG', 'Games']]
                st.dataframe(top_scorers, use_container_width=True)
            else:
                st.info("No data available")
        else:
            st.warning("Using sample data")

    except Exception as e:
        top_scorers = pd.DataFrame({
            'Player': ['Mike Johnson', 'David Lee', 'Chris Wilson', 'Tyler Brown', 'Sam Davis'],
            'PPG': [28.5, 26.3, 24.8, 23.1, 22.7],
            'Games': [15, 14, 15, 13, 15]
        })
        st.dataframe(top_scorers, use_container_width=True)

with col2:
    st.write("### Top Assist Leaders")

    try:
        response = requests.get('http://api:4000/players/stats/aggregate')

        if response.status_code == 200:
            stats_data = response.json()

            if stats_data:
                df = pd.DataFrame(stats_data)
                df['Player'] = df['firstName'] + ' ' + df['lastName']
                df['APG'] = pd.to_numeric(df['avg_assists'], errors='coerce')
                df['Games'] = df['games_played']

                top_assists = df.nlargest(5, 'APG')[['Player', 'APG', 'Games']]
                st.dataframe(top_assists, use_container_width=True)
            else:
                st.info("No data available")
        else:
            st.warning("Using sample data")

    except Exception as e:
        top_assists = pd.DataFrame({
            'Player': ['Emma Clark', 'John Smith', 'Lisa Wang', 'Tom Harris', 'Jake Moore'],
            'APG': [9.2, 8.7, 8.3, 7.9, 7.5],
            'Games': [15, 15, 14, 15, 13]
        })
        st.dataframe(top_assists, use_container_width=True)

# Player comparison
st.write("---")
st.write("### Compare Players")

try:
    # Get list of players for comparison
    response = requests.get('http://api:4000/players/stats/aggregate')

    if response.status_code == 200:
        players_data = response.json()

        if players_data:
            players_df = pd.DataFrame(players_data)
            players_df['name'] = players_df['firstName'] + ' ' + players_df['lastName']
            player_names = players_df['name'].tolist()

            col1, col2 = st.columns(2)

            with col1:
                player1_name = st.selectbox("Player 1", player_names, key="p1")
            with col2:
                player2_name = st.selectbox("Player 2", player_names, key="p2")

            # Get stats for selected players
            player1_data = players_df[players_df['name'] == player1_name].iloc[0]
            player2_data = players_df[players_df['name'] == player2_name].iloc[0]

            # Radar chart for comparison
            categories = ['Points', 'Assists', 'Rebounds']
            player1_stats = [
                pd.to_numeric(player1_data['avg_points'], errors='coerce'),
                pd.to_numeric(player1_data['avg_assists'], errors='coerce'),
                pd.to_numeric(player1_data['avg_rebounds'], errors='coerce')
            ]
            player2_stats = [
                pd.to_numeric(player2_data['avg_points'], errors='coerce'),
                pd.to_numeric(player2_data['avg_assists'], errors='coerce'),
                pd.to_numeric(player2_data['avg_rebounds'], errors='coerce')
            ]

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=player1_stats,
                theta=categories,
                fill='toself',
                name=player1_name
            ))

            fig.add_trace(go.Scatterpolar(
                r=player2_stats,
                theta=categories,
                fill='toself',
                name=player2_name
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, max(max(player1_stats), max(player2_stats)) + 5])),
                showlegend=True,
                title="Player Comparison"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No players available for comparison")

except Exception as e:
    st.warning(f"Using sample comparison data: {str(e)}")
    col1, col2 = st.columns(2)

    with col1:
        player1 = st.selectbox("Player 1", ["Mike Johnson", "David Lee", "Chris Wilson"])
    with col2:
        player2 = st.selectbox("Player 2", ["Tyler Brown", "Sam Davis", "Emma Clark"])

    categories = ['Points', 'Assists', 'Rebounds', 'Steals', 'Blocks']
    player1_stats = [28, 5, 7, 2, 1]
    player2_stats = [23, 8, 6, 3, 0]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=player1_stats,
        theta=categories,
        fill='toself',
        name=player1
    ))

    fig.add_trace(go.Scatterpolar(
        r=player2_stats,
        theta=categories,
        fill='toself',
        name=player2
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 30])),
        showlegend=True,
        title="Player Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)
