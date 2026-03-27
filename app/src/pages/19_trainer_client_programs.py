import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

API = "http://web-api:4000/trainer"
TRAINER_ID = 1

st.title("Client Programs")

# ------------------------------------
# ASSIGN PROGRAM
# ------------------------------------
st.subheader("➕ Assign Program to Client")

with st.form("assign_prog"):
    client_id = st.number_input("Client ID", min_value=1)
    workout_id = st.number_input("Workout Template ID", min_value=1)
    name = st.text_input("Program Name")
    description = st.text_area("Description")

    submitted = st.form_submit_button("Assign Program")

if submitted:
    data = {
        "client_id": client_id,
        "workout_id": workout_id,
        "name": name,
        "description": description
    }
    resp = requests.post(f"{API}/client-programs/{TRAINER_ID}", json=data)

    if resp.status_code == 201:
        st.success("Assigned!")
    else:
        st.error(resp.text)


# ------------------------------------
# VIEW PROGRAMS
# ------------------------------------
st.subheader("📋 Assigned Programs")

resp = requests.get(f"{API}/client-programs/{TRAINER_ID}")
if resp.status_code == 200:
    programs = resp.json()

    for p in programs:
        with st.expander(f"{p['name']} (ID {p['program_id']})"):
            st.write(f"Client: {p['client_id']}")
            st.write(f"Workout Template: {p['workout_id']}")
            st.write(f"Description: {p['description']}")

            col1, col2 = st.columns(2)

            # UPDATE
            with col1:
                with st.form(f"update_{p['program_id']}"):
                    new_name = st.text_input("Name", p["name"])
                    new_desc = st.text_area("Description", p["description"])
                    upd = st.form_submit_button("Update")

                if upd:
                    update_data = {"name": new_name, "description": new_desc}
                    r = requests.put(f"{API}/client-program/{p['program_id']}", json=update_data)
                    if r.status_code == 200:
                        st.success("Updated!")
                        st.rerun()
                    else:
                        st.error(r.text)

            # DELETE
            with col2:
                if st.button("❌ Remove", key=f"del_{p['program_id']}"):
                    r = requests.delete(f"{API}/client-program/{p['program_id']}")
                    if r.status_code == 200:
                        st.success("Program removed!")
                        st.rerun()
                    else:
                        st.error(r.text)
else:
    st.error("Could not load programs.")
