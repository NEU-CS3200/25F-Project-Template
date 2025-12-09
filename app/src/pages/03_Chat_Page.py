import streamlit as st
from modules.nav import SideBarLinks
from modules.chat_utils import load_chats, save_chats

st.set_page_config(layout="wide")
SideBarLinks()

customer = st.session_state["first_name"]

st.title("💬 Chat with Support")

# Load chat data
chats = load_chats()

# Ensure customer exists
if "customers" not in chats:
    chats["customers"] = {}

if customer not in chats["customers"]:
    chats["customers"][customer] = []

customer_chat = chats["customers"][customer]

# ---------------------------------------------------
# 1. RESOLVED MESSAGE (shown ONLY if admin cleared chat)
# ---------------------------------------------------
if len(customer_chat) == 0:
    st.info("Your previous chat was resolved by the admin. Start a new message below.")

# ---------------------------------------------------
# 2. Show chat history (if any)
# ---------------------------------------------------
elif len(customer_chat) > 0:
    st.subheader("Your Conversation")

    for entry in customer_chat:
        speaker = entry["from"]
        message = entry["message"]

        if speaker == "customer":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(
                f"<div style='color: #1e88e5'><b>Admin:</b> {message}</div>",
                unsafe_allow_html=True
            )

st.write("---")

# ---------------------------------------------------
# 3. Input box for new messages
# ---------------------------------------------------
msg = st.text_input("Enter your message:", key="msg_input")

if st.button("Send"):
    if msg.strip():
        customer_chat.append({
            "from": "customer",
            "message": msg.strip()
        })
        save_chats(chats)
        st.session_state["refresh"] = not st.session_state.get("refresh", False)
    else:
        st.warning("Message cannot be empty.")
