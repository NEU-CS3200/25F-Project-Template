import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

API = "http://web-api:4000/trainer"

st.title("Create Workout-Specific Exercise")

with st.form("create_wse"):
    workout_id = st.number_input("Workout Template ID", min_value=1)
    exercise_id = st.number_input("Exercise ID", min_value=1)
    sets = st.number_input("Sets", min_value=1)
    reps = st.number_input("Reps", min_value=1)
    rest_period = st.number_input("Rest Period (seconds)", min_value=10)

    submitted = st.form_submit_button("Create")

if submitted:
    data = {
        "workout_id": workout_id,
        "exercise_id": exercise_id,
        "sets": sets,
        "reps": reps,
        "rest_period": rest_period
    }
    resp = requests.post(f"{API}/create-workout-exercises", json=data)

    if resp.status_code == 201:
        st.success("Workout-Specific Exercise Created!")
    else:
        st.error(resp.text)
