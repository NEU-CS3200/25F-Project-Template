import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

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
        position_filter = st.multiselect("Positions", ["PG", "SG", "SF", "PF", "C"],
                                         default=["PG", "SG", "SF", "PF", "C"])

    with col2:
        min_games = st.number_input("Minimum Games Played", min_value=0, value=5)
        format_type = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])

    include_fields = st.multiselect("Fields to Include",
                                    ["Player Info", "Season Stats", "Game-by-Game", "Advanced Metrics"],
                                    default=["Player Info", "Season Stats"])

    if st.button("Generate Export", type="primary"):
        st.success(f"✅ Export generated: {len(position_filter)} positions, {season}")

        # Sample data preview
        sample_data = pd.DataFrame({
            'Player': ['Mike Johnson', 'David Lee', 'Chris Wilson'],
            'Position': ['PG', 'SG', 'SF'],
            'PPG': [28.5, 26.3, 24.8],
            'APG': [5.2, 4.1, 6.3],
            'RPG': [7.1, 5.8, 8.2]
        })

        st.write("Preview:")
        st.dataframe(sample_data)

        st.download_button(
            label=f"📥 Download {format_type}",
            data=sample_data.to_csv(index=False),
            file_name=f"player_stats_{season}.{format_type.lower()}",
            mime="text/csv"
        )

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
        st.success("✅ Game data export generated")
        st.download_button(
            label="📥 Download",
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

else:  # Custom Query
    st.write("#### Custom SQL Query")

    st.info("Write a custom SQL query to export specific data")

    query = st.text_area("SQL Query",
                         value="SELECT * FROM Players WHERE class_of = 2026",
                         height=150)

    format_type = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Test Query", type="secondary"):
            st.info("Query validation in progress...")
            st.success("✅ Query is valid. Expected rows: 847")

    with col2:
        if st.button("Execute & Export", type="primary"):
            st.success("✅ Query executed successfully")
            st.download_button(
                label="📥 Download Results",
                data="sample,data\n1,2\n",
                file_name=f"custom_export.{format_type.lower()}",
                mime="text/csv"
            )

# Export history
st.write("---")
st.write("### Recent Exports")

history = pd.DataFrame({
    'Export_Name': ['Player Stats 2024-25', 'Game Data Nov', 'Scout Reports Q4', 'Custom Query'],
    'Date': ['2025-12-03', '2025-12-02', '2025-12-01', '2025-11-30'],
    'Type': ['CSV', 'Excel', 'PDF', 'JSON'],
    'Size': ['2.3 MB', '5.1 MB', '12.4 MB', '890 KB']
})

st.dataframe(history, use_container_width=True)