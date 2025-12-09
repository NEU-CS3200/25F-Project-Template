import streamlit as st
from modules.nav import SideBarLinks
from modules.driver_chat_utils import load_chats, save_chats
from datetime import datetime

st.set_page_config(layout="wide")
SideBarLinks()

st.title("🚚 Driver Chat with Admin")

# Initialize session state for refresh toggle
if "refresh" not in st.session_state:
    st.session_state["refresh"] = False

# Load driver chat data
driver_chats = load_chats("driver_messages.json")
if "messages" not in driver_chats:
    driver_chats["messages"] = []

messages = driver_chats["messages"]

# ------------------ Show previous messages ------------------
st.subheader("💌 Previous Messages")
if messages:
    for entry in messages:
        speaker = entry.get("from", "")
        content = entry.get("message", "")
        timestamp = entry.get("timestamp", "")
        if speaker == "admin":
            st.markdown(f"<div style='color: #1e88e5'><b>Admin:</b> {content} <i>({timestamp})</i></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: #2e7d32'><b>You:</b> {content} <i>({timestamp})</i></div>", unsafe_allow_html=True)
else:
    st.info("No previous messages. Start a new chat below!")

st.write("---")

# ------------------ Send new message ------------------
st.subheader("📤 Send a New Message")
msg = st.text_area("Type your message here...", height=100)

# Quick preset messages
st.write("**Quick Messages:**")
quick_cols = st.columns(3)
quick_messages = [
    "Running late on delivery",
    "Need route assistance",
    "Customer not available"
]

for idx, qmsg in enumerate(quick_messages):
    with quick_cols[idx]:
        if st.button(qmsg, key=f"quick_{idx}", use_container_width=True):
            messages.append({
                "from": "driver",
                "message": qmsg,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_chats(driver_chats, "driver_messages.json")
            st.session_state["refresh"] = not st.session_state["refresh"]
            st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.stop()

# Send message button
if st.button("Send Message"):
    if msg.strip():
        messages.append({
            "from": "driver",
            "message": msg.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_chats(driver_chats, "driver_messages.json")
        st.success("Message sent!")
        st.session_state["refresh"] = not st.session_state["refresh"]
        st.stop()
    else:
        st.warning("Message cannot be empty.")

# ------------------ Clear chat button ------------------
st.write("---")
if st.button("🗑️ Clear Chat"):
    driver_chats["messages"] = []
    save_chats(driver_chats, "driver_messages.json")
    st.success("Chat cleared!")
    st.session_state["refresh"] = not st.session_state["refresh"]
    st.stop()



