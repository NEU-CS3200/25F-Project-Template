import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    position = st.selectbox("Position", ["All", "PG", "SG", "SF", "PF", "C"])

# Key metrics
st.write("---")
st.write("### League-Wide Statistics")

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

# Sample data for histogram
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
    top_scorers = pd.DataFrame({
        'Player': ['Mike Johnson', 'David Lee', 'Chris Wilson', 'Tyler Brown', 'Sam Davis'],
        'PPG': [28.5, 26.3, 24.8, 23.1, 22.7],
        'Games': [15, 14, 15, 13, 15]
    })
    st.dataframe(top_scorers, use_container_width=True)

with col2:
    st.write("### Top Assist Leaders")
    top_assists = pd.DataFrame({
        'Player': ['Emma Clark', 'John Smith', 'Lisa Wang', 'Tom Harris', 'Jake Moore'],
        'APG': [9.2, 8.7, 8.3, 7.9, 7.5],
        'Games': [15, 15, 14, 15, 13]
    })
    st.dataframe(top_assists, use_container_width=True)

# Player comparison
st.write("---")
st.write("### Compare Players")

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox("Player 1", ["Mike Johnson", "David Lee", "Chris Wilson"])
with col2:
    player2 = st.selectbox("Player 2", ["Tyler Brown", "Sam Davis", "Emma Clark"])

# Radar chart for comparison
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