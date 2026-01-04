import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('💬 Scout Feedback')

player_id = st.session_state.get('user_id', 101)

st.write("### Feedback from Scouts")

try:
    # Get feedback from API
    response = requests.get(f'http://web-api:4000/players/{player_id}/feedback')

    if response.status_code == 200:
        feedback_list = response.json()

        if feedback_list:
            for feedback in feedback_list:
                scout_name = f"{feedback.get('scout_first', 'Unknown')} {feedback.get('scout_last', 'Scout')}"
                scout_role = feedback.get('role', 'Scout')

                with st.expander(f"📋 {scout_name} - {scout_role}"):

                    # Summary
                    if feedback.get('summary'):
                        st.info(f"**Overall Assessment:** {feedback['summary']}")

                    # Strengths
                    if feedback.get('strengths'):
                        st.write(f"**✅ Strengths:** {feedback['strengths']}")

                    # Weaknesses
                    if feedback.get('weaknesses'):
                        st.write(f"**⚠️ Areas for Improvement:** {feedback['weaknesses']}")

                    # Report ID
                    st.caption(f"Report ID: {feedback.get('reportID', 'N/A')}")
        else:
            st.info("No scout feedback available yet. Keep playing and scouts will start evaluating your performance!")

    else:
        st.error(f"Failed to load feedback: {response.status_code}")

except Exception as e:
    st.error(f"Error loading feedback: {str(e)}")
    st.info("Showing sample feedback")

    # Sample feedback as fallback
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

# Statistics
st.write("---")
st.write("### Feedback Statistics")

try:
    response = requests.get(f'http://web-api:4000/players/{player_id}/feedback')

    if response.status_code == 200:
        feedback_list = response.json()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Reports", len(feedback_list))
        with col2:
            # Count unique scouts
            unique_scouts = len(set([f.get('scoutID') for f in feedback_list]))
            st.metric("Scouts Reviewing", unique_scouts)
        with col3:
            st.metric("Avg. Rating", "N/A")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Reports", "2")
        with col2:
            st.metric("Scouts Reviewing", "2")
        with col3:
            st.metric("Avg. Rating", "4.5/5")

except Exception as e:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reports", "2")
    with col2:
        st.metric("Scouts Reviewing", "2")
    with col3:
        st.metric("Avg. Rating", "4.5/5")

# Tips
st.write("---")
st.write("### 📌 How to Use Scout Feedback")
st.info("""
- Review feedback regularly to identify areas for improvement
- Focus on strengthening your weaknesses highlighted by scouts
- Keep track of recurring themes in feedback
- Use feedback to set specific training goals
- Scouts are evaluating your performance to help you improve and identify opportunities
""")
