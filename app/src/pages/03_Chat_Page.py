import streamlit as st
from modules.nav import SideBarLinks
from modules.chat_utils import load_chats, save_chats

st.set_page_config(layout="wide")
SideBarLinks()

customer = st.session_state["first_name"]

st.title("💬 Chat with Support")

chats = load_chats()

if customer not in chats["customers"]:
    chats["customers"][customer] = []

# Display message history
st.subheader("Your Conversation")
for entry in chats["customers"][customer]:
    speaker = entry["from"]
    message = entry["message"]
    if speaker == "customer":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"<div style='color: #1e88e5'><b>Admin:</b> {message}</div>", unsafe_allow_html=True)

# Input box
st.write("---")
msg = st.text_input("Enter your message:", key="msg_input")

if st.button("Send"):
    if msg.strip():
        chats["customers"][customer].append({
            "from": "customer",
            "message": msg
        })
        save_chats(chats)
        st.session_state["refresh"] = not st.session_state.get("refresh", False)