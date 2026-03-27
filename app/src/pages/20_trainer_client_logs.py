import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

API = "http://web-api:4000/trainer"

st.title("Client Workout Logs & Feedback")

resp = requests.get(f"{API}/client-logs")

if resp.status_code == 200:
    logs = resp.json()

    for log in logs:
        with st.expander(f"{log['client_id']} — {log['workout_date']}"):
            st.write(f"Workout ID: {log['workout_id']}")
            st.write(f"Status: **{log['completion_status']}**")
            st.write(f"Duration: {log['duration_minutes']} min")

            # EXISTING FEEDBACK
            fb_resp = requests.get(f"{API}/getfeedback/{log['log_id']}")
            if fb_resp.status_code == 200:
                feedbacks = fb_resp.json()
                for fb in feedbacks:
                    st.markdown(f"""
                        <div style='padding:10px;border-radius:8px;background:#111;border:1px solid #444;margin-bottom:8px'>
                            <b style='color:#FF1A1A'>Trainer Feedback:</b>
                            <p style='color:white'>{fb['feedback_text']}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    if st.button("🗑 Delete Feedback", key=f"delfb{fb['feedback_id']}"):
                        r = requests.delete(f"{API}/deletefeedback/{fb['feedback_id']}")
                        if r.status_code == 200:
                            st.success("Feedback deleted!")
                            st.rerun()
                        else:
                            st.error(r.text)

            # ADD NEW FEEDBACK
            st.subheader("Add Feedback:")
            feedback = st.text_area(f"Write feedback for log {log['log_id']}",
                                    key=f"fbbox{log['log_id']}")

            if st.button("Submit Feedback", key=f"submitfb{log['log_id']}"):
                data = {"log_id": log["log_id"], "trainer_id": 1, "feedback_text": feedback}
                r = requests.post(f"{API}/createfeedback", json=data)
                if r.status_code == 201:
                    st.success("Feedback added!")
                    st.rerun()
                else:
                    st.error(r.text)

else:
    st.error("Cannot load logs.")

