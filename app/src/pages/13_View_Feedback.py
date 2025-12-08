import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('💬 Scout Feedback')

player_id = st.session_state.get('user_id', 101)

st.write("### Feedback from Scouts")

# Sample feedback
feedback_data = [
    {
        'Scout': 'John Smith - Duke University',
        'Date': '2025-11-28',
        'Rating': '⭐⭐⭐⭐⭐',
        'Strengths': 'Excellent court vision, strong leadership, consistent three-point shooting',
        'Weaknesses': 'Needs to improve lateral quickness on defense',
        'Overall': 'Strong D1 prospect. Shows excellent offensive skills and basketball IQ.'
    },
    {
        'Scout': 'Sarah Johnson - UCLA',
        'Date': '2025-11-15',
        'Rating': '⭐⭐⭐⭐',
        'Strengths': 'Great ball handling, high basketball IQ',
        'Weaknesses': 'Tendency to over-dribble, needs work on off-ball defense',
        'Overall': 'Solid prospect with good potential. Focus on defensive fundamentals.'
    }
]

for feedback in feedback_data:
    with st.expander(f"📋 {feedback['Scout']} - {feedback['Date']}"):
        st.write(f"**Rating:** {feedback['Rating']}")
        st.write(f"**Strengths:** {feedback['Strengths']}")
        st.write(f"**Areas for Improvement:** {feedback['Weaknesses']}")
        st.info(f"**Overall Assessment:** {feedback['Overall']}")