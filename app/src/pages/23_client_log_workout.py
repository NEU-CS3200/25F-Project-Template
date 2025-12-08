import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Log Workout", page_icon="📝", layout="wide")
SideBarLinks()

if 'client_id' not in st.session_state:
    st.session_state.client_id = 1

BASE_URL = "http://web-api:4000"

st.title("📝 Log a New Workout")
st.markdown("### Record your training session")

st.markdown("---")

# Main logging form - [Chester-1]
st.subheader("➕ Create New Workout Log")

with st.form("workout_log_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        workout_id = st.selectbox(
            "Select Workout Template",
            options=[1, 2],
            format_func=lambda x: "Upper Body Blast" if x == 1 else "Leg Day Starter",
            help="Choose the workout template you completed"
        )
        
        workout_date = st.date_input(
            "Workout Date",
            value=datetime.now(),
            max_value=datetime.now(),
            help="When did you complete this workout?"
        )
        
        duration_minutes = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=300,
            value=45,
            step=5,
            help="How long was your workout?"
        )
    
    with col2:
        completion_status = st.selectbox(
            "Completion Status",
            options=["completed", "partial", "not_started"],
            index=0,
            help="Did you complete the full workout?"
        )
        
        notes = st.text_area(
            "Workout Notes",
            placeholder="Example: Felt strong today! Hit a PR on bench press (185 lbs). Right shoulder felt tight during overhead press.",
            height=150,
            help="Add any notes about how you felt, PRs achieved, or areas to improve"
        )
    
    col_a, col_b, col_c = st.columns([1, 1, 2])
    
    with col_a:
        submitted = st.form_submit_button("💾 Log Workout", use_container_width=True, type="primary")
    
    with col_b:
        cancelled = st.form_submit_button("❌ Clear Form", use_container_width=True)
    
    if submitted:
        workout_data = {
            "client_id": st.session_state.client_id,
            "workout_id": workout_id,
            "date": str(workout_date),
            "completion_status": completion_status,
            "duration_minutes": duration_minutes,
            "notes": notes
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/client/client_workout_log",
                json=workout_data
            )
            
            if response.status_code == 201:
                result = response.json()
                st.success(f"✅ Workout logged successfully! Log ID: {result.get('log_id')}")
                st.balloons()
            else:
                st.error(f"Failed to log workout: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

st.markdown("---")

# Show recently logged workouts
st.subheader("📋 Recently Logged Workouts")

try:
    response = requests.get(
        f"{BASE_URL}/client/client_workout_log",
        params={"client_id": st.session_state.client_id}
    )
    
    if response.status_code == 200:
        logs = response.json()
        
        if logs:
            df = pd.DataFrame(logs)
            df['workout_date'] = pd.to_datetime(df['workout_date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(
                df.head(5)[['workout_date', 'workout_name', 'duration_minutes', 'completion_status', 'notes']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "workout_date": "Date",
                    "workout_name": "Workout",
                    "duration_minutes": "Duration (min)",
                    "completion_status": "Status",
                    "notes": "Notes"
                }
            )
        else:
            st.info("No workouts logged yet. Log your first workout above!")
except Exception as e:
    st.error(f"Error loading recent workouts: {str(e)}")

st.markdown("---")

# Delete incomplete logs section - [Chester-6]
st.subheader("🗑️ Manage Incomplete Logs")

st.warning("""
⚠️ **Delete Incomplete Workout Logs**

This will permanently delete all workout logs with status 'not_started'. 
Use this to clean up placeholder or accidentally created logs.
This action cannot be undone!
""")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🗑️ Delete Incomplete Logs", type="secondary", use_container_width=True):
        try:
            response = requests.delete(
                f"{BASE_URL}/client/client_workout_log",
                params={"client_id": st.session_state.client_id}
            )
            
            if response.status_code == 200:
                result = response.json()
                rows_deleted = result.get('rows_deleted', 0)
                
                if rows_deleted > 0:
                    st.success(f"✅ Deleted {rows_deleted} incomplete workout log(s)!")
                    st.rerun()
                else:
                    st.info("No incomplete logs found to delete.")
            else:
                st.error(f"Failed to delete logs: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("pages/21_Client_home.py")

with col2:
    if st.button("📊 View Dashboard", use_container_width=True):
        st.switch_page("pages/22_client_dashboard.py")

with col3:
    if st.button("🎯 View My Program", use_container_width=True):
        st.switch_page("pages/24_client_my_program.py")