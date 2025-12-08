import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("Create Workout-Specific Exercise")

API_BASE = "http://web-api:4000"


# get the plain exercises (like plank, pushup, etc.)
try:
    response = requests.get(f"{API_BASE}/trainer/exercises")
    exercises = response.json()
except:
    exercises = []
    st.error("Could not connect to API (fetching base exercises).")

# dropdown to select the exercise
if exercises:
    exercise_options = {
        f"{ex['name']} (ID {ex['exercise_id']})": ex['exercise_id']
        for ex in exercises
    }
    selected_exercise = st.selectbox("Select Exercise", list(exercise_options.keys()))
else:
    st.error("No exercises available.")
    st.stop()


# inputs for sets/reps/rest period
sets = st.number_input("Sets", min_value=1, step=1)
reps = st.number_input("Reps", min_value=1, step=1)
rest = st.number_input("Rest Period (seconds)", min_value=0, step=10)

st.markdown("### Note")
st.info("This workout-specific exercise will be created WITHOUT a template. "
        "You will assign it later when creating a workout template.")


# save button
if st.button("Save Workout Exercise", type='primary', use_container_width=True):
    payload = {
        "exercise_id": exercise_options[selected_exercise],
        "sets": sets,
        "reps": reps,
        "rest_period": rest
    }

    result = requests.post(f"{API_BASE}/trainer/workout-exercises", json=payload)

    if result.status_code == 201:
        st.success("Workout Exercise Created!")
    else:
        st.error(f"Error creating workout exercise: {result.text}")

# show the existing workout exercises created
st.write("### Existing Workout-Specific Exercises")

try:
    existing = requests.get(f"{API_BASE}/trainer/workout-exercises").json()
    st.dataframe(existing)
except:
    st.info("No workout-specific exercises")