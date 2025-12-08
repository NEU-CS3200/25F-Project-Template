import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Assign Workout to a Client")

trainer_id = st.session_state.get("trainer_id", 1)

client_id = st.number_input("Client ID", step=1)
workout_id = st.number_input("Workout Template ID", step=1)
name = st.text_input("Program Name")
description = st.text_area("Program Description")

if st.button("Assign Program", type="primary"):
    payload = {
        "client_id": client_id,
        "workout_id": workout_id,
        "name": name,
        "description": description
    }

    response = requests.post(
        f"http://web-api:4000/trainer/programs/client-programs/{trainer_id}",
        json=payload
    )

    if response.status_code == 201:
        st.success("Program Assigned Successfully!")
        st.write(response.json())
    else:
        st.error("Error assigning program")
        st.write(response.text)