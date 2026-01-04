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

# Personalize page with the user's name from session state
first_name = st.session_state.get('first_name', 'Data Analyst')
st.title(f"Majors & Location Analytics")
st.write('')
st.write('### Major Participation across Students & Alumni')

# Pull data for majors, students, and alumni from the API
majors = api_get("/majors", default=[])
students = api_get("/students", default=[])
alumni = api_get("/alumni", default=[])

if majors and (students or alumni):
     # Convert majors list to DataFrame:
    majors_df = pd.DataFrame(majors)  # expect major_id, major_name, department

  # Build counts of students and alumni per major_id
    counts = {}
    for s in students or []:
        mid = s.get("major_id")
        if mid is not None:
            counts.setdefault(mid, {"students": 0, "alumni": 0})
            counts[mid]["students"] += 1

    for a in alumni or []:
        mid = a.get("major_id")
        if mid is not None:
            counts.setdefault(mid, {"students": 0, "alumni": 0})
            counts[mid]["alumni"] += 1

    counts_df = pd.DataFrame(
        [
            {
                "major_id": mid,
                "student_count": v["students"],
                "alumni_count": v["alumni"],
                "total": v["students"] + v["alumni"],
            }
            for mid, v in counts.items()
        ]
    )

    merged = majors_df.merge(counts_df, on="major_id", how="left").fillna(0)
    merged = merged.sort_values("total", ascending=False)

    st.dataframe(merged, use_container_width=True)

    if "major_name" in merged.columns:
        st.write('')
        st.write("#### Students & Alumni per Major")
        chart_df = merged.set_index("major_name")[["student_count", "alumni_count"]]
        st.bar_chart(chart_df)
else:
    st.info("Majors, students, or alumni data not available yet. Check your REST endpoints.")

st.write('')
st.write('---')
st.write('### Locations of Users')

locations = api_get("/locations", default=[])

if locations:
    loc_df = pd.DataFrame(locations)
    st.dataframe(loc_df, use_container_width=True)
else:
    st.info("No location data returned from /locations yet.")


