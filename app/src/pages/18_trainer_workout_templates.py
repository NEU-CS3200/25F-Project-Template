import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("Create Workout Template")

API_BASE = "http://web-api:4000"

# basic template info 
name = st.text_input("Template Name")
description = st.text_area("Description")
duration = st.number_input("Duration (minutes)", min_value=1, step=5)
difficulty = st.selectbox("Difficulty", ["easy", "moderate", "hard"])

# get the Workout-Specific Exercises 
try:
    response = requests.get(f"{API_BASE}/trainer/workout-exercises")
    specific_exercises = response.json()
except:
    specific_exercises = []
    st.error("Could not connect to API.")

#  nice labels
formatted_options = {
    f"{ex['exercise_name']} • {ex['sets']}×{ex['reps']} • {ex['rest_period']}s rest (ID {ex['workout_exercise_id']})":
    ex['workout_exercise_id']
    for ex in specific_exercises
}

selected_exercises = st.multiselect(
    "Select Exercises for This Template",
    list(formatted_options.keys())
)

# create template 
if st.button("Create Template", type='primary', use_container_width=True):

    # 1. create the template row
    template_payload = {
        "name": name,
        "description": description,
        "duration_minutes": duration,
        "difficulty": difficulty,
        "trainer_id": st.session_state["user_id"]
    }

    result = requests.post(f"{API_BASE}/trainer/workout_session_template", json=template_payload)

    if result.status_code != 201:
        st.error("Failed to create template.")
        st.stop()

    workout_id = result.json().get("workout_id")

    # assign each selected exercise to that template
    for key in selected_exercises:
        wse_id = formatted_options[key]
        update_payload = {"workout_id": workout_id}

        requests.put(f"{API_BASE}/trainer/workout-exercises/{wse_id}", json=update_payload)

    st.success("Workout Template Created Successfully!")