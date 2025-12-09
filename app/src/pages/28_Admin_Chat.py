import streamlit as st
from modules.nav import SideBarLinks
from modules.chat_utils import load_chats, save_chats
from datetime import datetime

st.set_page_config(layout="wide")
SideBarLinks()
st.title("📨 Admin Support Inbox")

# Load chat data
chats = load_chats()
if not isinstance(chats, dict):
    chats = {}

# Initialize keys if missing
if "customers" not in chats:
    chats["customers"] = {}

# ------------------ CUSTOMER CHAT ------------------
st.header("💜 Chat with Customers")
customer_list = list(chats.get("customers", {}).keys())

if customer_list:
    selected_customer = st.selectbox("Select Customer:", customer_list)
    st.subheader(f"Chat with {selected_customer}")

    # Show customer chat history
    for entry in chats["customers"][selected_customer]:
        speaker = entry["from"]
        message = entry["message"]
        timestamp = entry.get("timestamp", "")
        if speaker == "admin":
            st.markdown(f"<div style='color: #1e88e5'><b>Admin:</b> {message} <i>({timestamp})</i></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: #6a1b9a'><b>{selected_customer}:</b> {message} <i>({timestamp})</i></div>", unsafe_allow_html=True)

    # Admin response form
    with st.form(f"customer_reply_form_{selected_customer}"):
        reply = st.text_area("Your message to customer")
        submitted = st.form_submit_button("Send")
        if submitted and reply.strip():
            chats["customers"][selected_customer].append({
                "from": "admin",
                "message": reply.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_chats(chats)
            st.success("Message sent!")
            st.session_state["refresh"] = not st.session_state.get("refresh", False)
            st.stop()

    # Resolve customer chat
    if st.button(f"Resolve Chat with {selected_customer}"):
        chats["customers"][selected_customer] = []
        save_chats(chats)
        st.success(f"Chat with {selected_customer} has been resolved!")
        st.session_state["refresh"] = not st.session_state.get("refresh", False)
        st.stop()

else:
    st.info("No customer messages yet.")

# ------------------ DRIVER CHAT ------------------
st.header("💚 Chat with Drivers")
driver_list = list(chats.get("drivers", {}).keys())

if driver_list:
    selected_driver = st.selectbox("Select Driver:", driver_list)
    st.subheader(f"Chat with {selected_driver}")

    driver_chat = chats["drivers"][selected_driver]
    if not driver_chat:
        st.info("No messages yet. This chat may have been resolved.")
    else:
        for entry in driver_chat:
            speaker = entry["from"]
            message = entry["message"]
            timestamp = entry.get("timestamp", "")
            if speaker == "admin":
                st.markdown(f"<div style='color: #1e88e5'><b>Admin:</b> {message} <i>({timestamp})</i></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: #2e7d32'><b>{selected_driver}:</b> {message} <i>({timestamp})</i></div>", unsafe_allow_html=True)

    # Admin response form for driver
    with st.form(f"driver_reply_form_{selected_driver}"):
        reply = st.text_area("Your message to driver")
        submitted = st.form_submit_button("Send")
        if submitted and reply.strip():
            driver_chat.append({
                "from": "admin",
                "message": reply.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            chats["drivers"][selected_driver] = driver_chat
            save_chats(chats)
            st.success("Message sent!")
            st.session_state["refresh"] = not st.session_state.get("refresh", False)
            st.stop()

    # Resolve driver chat
    if st.button(f"Resolve Chat with {selected_driver}"):
        chats["drivers"][selected_driver] = []
        save_chats(chats)
        st.success(f"Chat with {selected_driver} has been resolved!")
        st.session_state["refresh"] = not st.session_state.get("refresh", False)
        st.stop()

else:
    st.info("No driver messages yet.")






