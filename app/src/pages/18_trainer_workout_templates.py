import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

API = "http://web-api:4000/trainer"
TRAINER_ID = 1   # mock persona

st.title("Workout Templates")

# ---------------------------------------
# CREATE TEMPLATE
# ---------------------------------------
st.subheader("➕ Create Template")

with st.form("create_template"):
    name = st.text_input("Name")
    description = st.text_area("Description")
    duration = st.number_input("Duration (minutes)", min_value=1)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    submitted = st.form_submit_button("Create Template")

if submitted:
    data = {
        "name": name,
        "description": description,
        "duration_minutes": duration,
        "difficulty": difficulty
    }
    resp = requests.post(f"{API}/create-templates/{TRAINER_ID}", json=data)
    if resp.status_code == 201:
        st.success("Template Created!")
    else:
        st.error(resp.text)


# ---------------------------------------
# VIEW ALL TEMPLATES
# ---------------------------------------
st.subheader("📋 Your Templates")

resp = requests.get(f"{API}/view-all-templates/{TRAINER_ID}")
if resp.status_code == 200:
    templates = resp.json()
    for t in templates:
        with st.expander(f"{t['name']} (ID: {t['workout_id']})"):

            st.write(f"**Difficulty:** {t['difficulty']}")
            st.write(f"**Duration:** {t['duration_minutes']} minutes")
            st.write(f"**Description:** {t['description']}")

            col1, col2 = st.columns(2)

            # UPDATE FORM
            with col1:
                with st.form(f"update_{t['workout_id']}"):
                    new_name = st.text_input("Name", t["name"])
                    new_desc = st.text_area("Description", t["description"])
                    new_diff = st.selectbox("Difficulty",
                                            ["Easy", "Medium", "Hard"],
                                            index=["Easy","Medium","Hard"].index(t["difficulty"]))

                    new_dur = st.number_input("Duration", min_value=1, value=t["duration_minutes"])
                    upd = st.form_submit_button("Update")

                if upd:
                    update_data = {
                        "name": new_name,
                        "description": new_desc,
                        "difficulty": new_diff,
                        "duration_minutes": new_dur
                    }
                    r = requests.put(f"{API}/update-template/{t['template_id']}",
                                     json=update_data)
                    if r.status_code == 200:
                        st.success("Updated!")
                        st.rerun()
                    else:
                        st.error(r.text)

            # DELETE BUTTON
            with col2:
                if st.button("❌ Delete", key=f"del_{t['workout_id']}"):
                    r = requests.delete(f"{API}/delete-template/{t['template_id']}")
                    if r.status_code == 200:
                        st.success("Template Deleted!")
                        st.rerun()
                    else:
                        st.error(r.text)
else:
    st.error("Could not load templates.")
