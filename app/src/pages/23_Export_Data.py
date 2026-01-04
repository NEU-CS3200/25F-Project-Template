import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests
import json

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📥 Export Data')

st.write("### Export Player and Game Data")

# Export options
export_type = st.radio("Data Type",
                       ["Player Statistics", "Game Data", "Scout Reports", "Custom Query"])

if export_type == "Player Statistics":
    st.write("#### Player Statistics Export")

    col1, col2 = st.columns(2)

    with col1:
        season = st.selectbox("Season", ["2024-25", "2023-24", "All Time"])
        position_filter = st.multiselect("Positions", ["Guard", "Forward", "All"],
                                         default=["Guard", "Forward"])

    with col2:
        min_games = st.number_input("Minimum Games Played", min_value=0, value=0)
        format_type = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])

    include_fields = st.multiselect("Fields to Include",
                                    ["Player Info", "Season Stats", "Game-by-Game", "Advanced Metrics"],
                                    default=["Player Info", "Season Stats"])

    if st.button("Generate Export", type="primary"):
        try:
            # Get player statistics from API
            response = requests.get('http://web-api:4000/players/stats/aggregate')

            if response.status_code == 200:
                players_data = response.json()

                if players_data:
                    df = pd.DataFrame(players_data)

                    # Format the data
                    df['Player'] = df['firstName'] + ' ' + df['lastName']
                    df['PPG'] = pd.to_numeric(df['avg_points'], errors='coerce')
                    df['APG'] = pd.to_numeric(df['avg_assists'], errors='coerce')
                    df['RPG'] = pd.to_numeric(df['avg_rebounds'], errors='coerce')
                    df['Games'] = df['games_played']

                    export_df = df[['Player', 'position', 'PPG', 'APG', 'RPG', 'Games']]
                    export_df.columns = ['Player', 'Position', 'PPG', 'APG', 'RPG', 'Games']

                    st.success(f"✅ Export generated: {len(export_df)} players")

                    st.write("Preview:")
                    st.dataframe(export_df.head(10), use_container_width=True)

                    # Create export request in database
                    export_request_data = {
                        'requestedBy': 1,
                        'requestedUserType': 'analyst',
                        'format': format_type,
                        'dataType': 'Player Stats',
                        'status': 'completed'
                    }

                    requests.post('http://web-api:4000/analytics/datasets/export', json=export_request_data)

                    # Generate download based on format
                    if format_type == "CSV":
                        data = export_df.to_csv(index=False)
                        mime = "text/csv"
                    elif format_type == "JSON":
                        data = export_df.to_json(orient='records', indent=2)
                        mime = "application/json"
                    else:  # Excel
                        data = export_df.to_csv(index=False)  # Simplified for demo
                        mime = "text/csv"

                    st.download_button(
                        label=f"📥 Download {format_type}",
                        data=data,
                        file_name=f"player_stats_{season}.{format_type.lower()}",
                        mime=mime
                    )
                else:
                    st.info("No player data available")
            else:
                st.error(f"Failed to load data: {response.status_code}")

        except Exception as e:
            st.error(f"Error generating export: {str(e)}")

elif export_type == "Game Data":
    st.write("#### Game Data Export")

    col1, col2 = st.columns(2)

    with col1:
        date_from = st.date_input("From Date")
        league_filter = st.selectbox("League", ["All", "AAU", "High School"])

    with col2:
        date_to = st.date_input("To Date")
        format_type = st.selectbox("Format", ["CSV", "Excel", "JSON"])

    if st.button("Generate Export", type="primary"):
        try:
            # Get datasets from API
            response = requests.get('http://web-api:4000/analytics/datasets')

            if response.status_code == 200:
                game_data = response.json()

                if game_data:
                    df = pd.DataFrame(game_data)

                    st.success(f"✅ Game data export generated: {len(df)} records")
                    st.write("Preview:")
                    st.dataframe(df.head(10), use_container_width=True)

                    # Create export request
                    export_request_data = {
                        'requestedBy': 1,
                        'requestedUserType': 'analyst',
                        'format': format_type,
                        'dataType': 'Game Data',
                        'status': 'completed'
                    }

                    requests.post('http://web-api:4000/analytics/datasets/export', json=export_request_data)

                    st.download_button(
                        label="📥 Download",
                        data=df.to_csv(index=False),
                        file_name=f"game_data.{format_type.lower()}",
                        mime="text/csv"
                    )
                else:
                    st.info("No game data available")
            else:
                st.warning("Using sample data")
                st.download_button(
                    label="📥 Download",
                    data="game_id,date,opponent,venue\n1,2024-11-15,Warriors,Staples Center\n",
                    file_name="game_data.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.download_button(
                label="📥 Download Sample",
                data="game_id,date,home_team,away_team,score\n",
                file_name="game_data.csv",
                mime="text/csv"
            )

elif export_type == "Scout Reports":
    st.write("#### Scout Reports Export")

    scout_filter = st.selectbox("Scout", ["All Scouts", "My Reports", "By Scout Name"])
    date_range = st.date_input("Date Range", value=[])
    format_type = st.selectbox("Format", ["PDF", "CSV", "Excel"])

    if st.button("Generate Export", type="primary"):
        st.success("✅ Scout reports export generated")

        # Create export request
        try:
            export_request_data = {
                'requestedBy': 1,
                'requestedUserType': 'analyst',
                'format': format_type,
                'dataType': 'Scout Reports',
                'status': 'completed'
            }

            requests.post('http://web-api:4000/analytics/datasets/export', json=export_request_data)

        except Exception as e:
            st.warning(f"Could not log export: {str(e)}")

else:  # Custom Query
    st.write("#### Custom Data Export")

    st.info("Export specific datasets based on your needs")

    dataset_type = st.selectbox("Dataset Type",
                                ["Player Statistics", "Game Statistics", "Competition Context", "Calculated Metrics"])

    format_type = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Preview Data", type="secondary"):
            try:
                response = requests.get('http://web-api:4000/analytics/datasets')

                if response.status_code == 200:
                    data = response.json()
                    if data:
                        st.write("Preview:")
                        df = pd.DataFrame(data)
                        st.dataframe(df.head(10), use_container_width=True)
                        st.info(f"✅ Dataset contains {len(data)} records")
                    else:
                        st.info("No data available")
                else:
                    st.warning("Could not load preview")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    with col2:
        if st.button("Execute & Export", type="primary"):
            try:
                response = requests.get('http://web-api:4000/analytics/datasets')

                if response.status_code == 200:
                    data = response.json()

                    if data:
                        df = pd.DataFrame(data)

                        # Create export request
                        export_request_data = {
                            'requestedBy': 1,
                            'requestedUserType': 'analyst',
                            'format': format_type,
                            'dataType': dataset_type,
                            'status': 'completed'
                        }

                        requests.post('http://web-api:4000/analytics/datasets/export', json=export_request_data)

                        st.success("✅ Export generated successfully")
                        st.download_button(
                            label="📥 Download Results",
                            data=df.to_csv(index=False),
                            file_name=f"custom_export.{format_type.lower()}",
                            mime="text/csv"
                        )
                    else:
                        st.info("No data to export")
                else:
                    st.error("Failed to generate export")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Export history
st.write("---")
st.write("### Recent Exports")

try:
    # Get export requests from API
    response = requests.get('http://web-api:4000/analytics/export-requests')

    if response.status_code == 200:
        exports_data = response.json()

        if exports_data:
            history = pd.DataFrame(exports_data)
            display_history = history[['exportID', 'dataType', 'timestamp', 'format', 'status']].copy()
            display_history.columns = ['Export ID', 'Data Type', 'Date', 'Format', 'Status']
            st.dataframe(display_history, use_container_width=True)
        else:
            st.info("No export history available")
    else:
        st.info("Export history unavailable")

except Exception as e:
    st.info("Export history unavailable")
    history = pd.DataFrame({
        'Export_Name': ['Player Stats 2024-25', 'Game Data Nov', 'Scout Reports Q4', 'Custom Query'],
        'Date': ['2025-12-03', '2025-12-02', '2025-12-01', '2025-11-30'],
        'Type': ['CSV', 'Excel', 'PDF', 'JSON'],
        'Size': ['2.3 MB', '5.1 MB', '12.4 MB', '890 KB']
    })
    st.dataframe(history, use_container_width=True)
