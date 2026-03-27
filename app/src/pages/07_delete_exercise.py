import streamlit as st
import requests

API_BASE = "http://web-api:4000/system_admin"

st.title("Delete Exercise")

exercise_id = st.number_input("Exercise ID", min_value=1)

if st.button("Delete Exercise"):
    resp = requests.delete(f"{API_BASE}/exercise/{exercise_id}")

    try:
        data = resp.json()
    except:
        st.error("Non-JSON response from API")
        st.write(resp.text)
        st.stop()

    if resp.status_code == 200:
        st.success(data.get("message"))
    else:
        st.error(data)


