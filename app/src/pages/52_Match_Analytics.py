import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout='wide')

SideBarLinks()

try:
    API_BASE = st.secrets["API_BASE"]
except Exception:
    API_BASE = "http://api:4000"

def api_get(path, params=None, default=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=5)
        if r.status_code == 200:
            return r.json()
        logger.info(f"GET {path} -> {r.status_code}")
    except Exception as e:
        logger.info(f"GET {path} failed: {e}")
    return default

first_name = st.session_state.get('first_name', 'Data Analyst')
st.title(f"Match & Engagement Analytics")
st.write('')
st.write('### Overall Connections & Session Activity')

# Pull data for students, connections, and sessions
students = api_get("/students", default=[])
connections = api_get("/connections", default=[])
sessions = api_get("/sessions", default=[])

total_students = len(students) if isinstance(students, list) else 0
total_connections = len(connections) if isinstance(connections, list) else 0
total_sessions = len(sessions) if isinstance(sessions, list) else 0

# Compute how many unique studnets have at least one connection
matched_students = set()
for c in connections or []:
    sid = c.get("student_id")
    if sid is not None:
        matched_students.add(sid)

num_matched_students = len(matched_students)
match_rate_pct = round((num_matched_students / total_students) * 100, 1) if total_students > 0 else 0.0

# Show core metrics in a grid
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", total_students)
col2.metric("Students with at least 1 connection", num_matched_students)
col3.metric("Student Match Rate", f"{match_rate_pct}%")

st.write('')
c1, c2 = st.columns(2)
c1.metric("Total Connections", total_connections)
c2.metric("Total Sessions", total_sessions)

st.write('')
st.write('---')
st.write('### Session Trends')

if sessions:
    sess_df = pd.DataFrame(sessions)  

    if "session_date" in sess_df.columns:
        sess_df["session_date"] = pd.to_datetime(sess_df["session_date"], errors="coerce")
        sess_df["month"] = sess_df["session_date"].dt.to_period("M").astype(str)
        month_counts = (
            sess_df.groupby("month")
            .size()
            .reset_index(name="session_count")
            .sort_values("month")
        )

        st.dataframe(month_counts, use_container_width=True)
        st.line_chart(
            month_counts.set_index("month")["session_count"]
        )
    else:
        st.info("Sessions endpoint does not expose session_date, showing raw data instead.")
        st.dataframe(sess_df, use_container_width=True)
else:
    st.info("No sessions found yet. Try generating some test data.")