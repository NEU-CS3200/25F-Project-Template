import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# API Test Page")
st.write("Testing all Admin API routes from Streamlit.")

API_BASE = "http://api:4000/a"

st.markdown("---")

# ============================
# USER STORY 1 — View Pending Reports
# ============================
st.write("### View Pending Reports")

try:
    response = requests.get(f"{API_BASE}/reports/pending")
    st.write(response.json())
except:
    st.write("Could not connect to API.")


# ============================
# USER STORY 1 — Resolve Report
# ============================
st.write("### Resolve Report (example: report_id = 1)")

try:
    response = requests.put(f"{API_BASE}/reports/1/resolve")
    st.write(response.json())
except:
    st.write("Could not resolve report.")


# ============================
# USER STORY 2 — Update User Role
# ============================
st.write("### Update User Role (example: user_id = 1 → admin)")

try:
    payload = {"role": "admin"}
    response = requests.put(f"{API_BASE}/users/1/role", json=payload)
    st.write(response.json())
except:
    st.write("Could not update user role.")


# ============================
# USER STORY 3 — Deactivate User
# ============================
st.write("### Deactivate User (example: user_id = 1)")

try:
    response = requests.put(f"{API_BASE}/users/1/deactivate")
    st.write(response.json())
except:
    st.write("Could not deactivate user.")


# ============================
# USER STORY 4 — Create Announcement
# ============================
st.write("### Create Announcement")

try:
    payload = {"announcer_id": 1, "message": "Test announcement"}
    response = requests.post(f"{API_BASE}/announcements", json=payload)
    st.write(response.json())
except:
    st.write("Could not create announcement.")


# ============================
# USER STORY 5 — Analytics Summary
# ============================
st.write("### Analytics Summary")

try:
    response = requests.get(f"{API_BASE}/analytics/summary")
    st.write(response.json())
except:
    st.write("Could not load analytics summary.")


# ============================
# USER STORY 6 — Delete Duplicate Items
# ============================
st.write("### Delete Duplicate Items")

try:
    response = requests.delete(f"{API_BASE}/items/duplicates")
    st.write(response.json())
except:
    st.write("Could not delete duplicate items.")


# ============================
# USER STORY 6+1 — Delete Specific Item
# ============================
st.write("### Delete Specific Item (example: item_id = 1)")

try:
    response = requests.delete(f"{API_BASE}/items/1")
    st.write(response.json())
except:
    st.write("Could not delete item.")
