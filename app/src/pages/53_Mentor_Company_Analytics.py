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
st.title(f"Mentors & Companies Analytics")
st.write('')
st.write('### Alumni Mentors Supporting the Most Students')

# Pull data for alumni, connections, and sessions
alumni = api_get("/alumni", default=[])
connections = api_get("/connections", default=[])
sessions = api_get("/sessions", default=[])

alum_df = pd.DataFrame(alumni) if alumni else pd.DataFrame()
conn_df = pd.DataFrame(connections) if connections else pd.DataFrame()
sess_df = pd.DataFrame(sessions) if sessions else pd.DataFrame()

if not alum_df.empty and (not conn_df.empty or not sess_df.empty):
    # count unique students per alumni_id from connections
    if not conn_df.empty and "alumni_id" in conn_df.columns and "student_id" in conn_df.columns:
        mentor_counts = (
            conn_df.groupby("alumni_id")["student_id"]
            .nunique()
            .reset_index(name="unique_students")
        )
    else:
        mentor_counts = pd.DataFrame(columns=["alumni_id", "unique_students"])

    # count total sessions per alumni
    if not sess_df.empty and "alumni_id" in sess_df.columns:
        session_counts = (
            sess_df.groupby("alumni_id")
            .size()
            .reset_index(name="session_count")
        )
    else:
        session_counts = pd.DataFrame(columns=["alumni_id", "session_count"])

    # Merge counts back onto alumni details 
    merged = alum_df.merge(mentor_counts, on="alumni_id", how="left").merge(
        session_counts, on="alumni_id", how="left"
    )
    merged[["unique_students", "session_count"]] = merged[
        ["unique_students", "session_count"]
    ].fillna(0)

    merged["unique_students"] = merged["unique_students"].astype(int)
    merged["session_count"] = merged["session_count"].astype(int)

    # Sort to find top mentors and show the top 10
    top_mentors = merged.sort_values(
        ["unique_students", "session_count"], ascending=False
    ).head(10)

    st.dataframe(top_mentors, use_container_width=True)

    if "name" in top_mentors.columns:
        st.write('')
        st.write("#### Top Mentors by Unique Students Mentored")
        chart_df = top_mentors.set_index("name")[["unique_students", "session_count"]]
        st.bar_chart(chart_df)
else:
    st.info("Not enough alumni / connections / sessions data to compute mentor rankings yet.")

st.write('')
st.write('---')
st.write('### Companies & Where Alumni Work')

companies = api_get("/companies", default=[])
if companies and not alum_df.empty:
    comp_df = pd.DataFrame(companies)  # expect company_id, company_name, industry

    if "company_id" in alum_df.columns:
        comp_counts = (
            alum_df.groupby("company_id")
            .size()
            .reset_index(name="alumni_count")
        )
        merged_comp = comp_df.merge(comp_counts, on="company_id", how="left").fillna(0)
        merged_comp["alumni_count"] = merged_comp["alumni_count"].astype(int)
        merged_comp = merged_comp.sort_values("alumni_count", ascending=False)

        st.dataframe(merged_comp, use_container_width=True)

        if "company_name" in merged_comp.columns:
            st.write('')
            st.write("#### Alumni Count by Company")
            chart_df = merged_comp.set_index("company_name")["alumni_count"]
            st.bar_chart(chart_df)
    else:
        st.dataframe(comp_df, use_container_width=True)
        st.caption("Alumni rows do not expose company_id, so only raw companies are shown.")
else:
    st.info("No company or alumni data available yet.")