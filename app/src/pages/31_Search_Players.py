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
    position = st.selectbox("Position", ["All", "PG", "SG", "SF", "PF", "C"])
with col2:
    min_height = st.number_input("Min Height (inches)", min_value=60, max_value=90, value=70)
with col3:
    class_of = st.number_input("Class Of", min_value=2024, max_value=2030, value=2026)

if st.button("Search", type='primary'):
    try:
        # Try to get players from API
        response = requests.get('http://api:4000/players')

        if response.status_code == 200:
            players = response.json()

            if players:
                df = pd.DataFrame(players)

                # Apply filters
                if position != "All" and 'position' in df.columns:
                    df = df[df['position'] == position]

                if 'height' in df.columns:
                    df = df[df['height'] >= min_height]

                if 'class_of' in df.columns:
                    df = df[df['class_of'] == class_of]

                if len(df) > 0:
                    st.success(f"Found {len(df)} players matching criteria")
                    st.dataframe(df, use_container_width=True)
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
            'playerID': [1, 2, 3],
            'firstName': ['LeBron', 'Stephen', 'Kevin'],
            'lastName': ['James', 'Curry', 'Durant'],
            'position': ['SF', 'PG', 'SF'],
            'height': [78, 75, 82],
            'class_of': [2026, 2026, 2025]
        }
        st.dataframe(pd.DataFrame(sample_data), use_container_width=True)