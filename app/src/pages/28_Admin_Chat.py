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

else:
    st.info("No customer messages yet.")

# ------------------ DRIVER CHAT ------------------
st.header("💚 Chat with Drivers")
driver_list = list(chats.get("drivers", {}).keys())

if driver_list:
    selected_driver = st.selectbox("Select Driver:", driver_list)
    st.subheader(f"Chat with {selected_driver}")

    driver_orders = chats["drivers"].get(selected_driver, {})

    # Choose order to chat about
    order_list = list(driver_orders.keys())
    if order_list:
        selected_order = st.selectbox("Select Order:", order_list)
        st.markdown(f"**Order:** {selected_order}")

        # Show chat history for that order
        for entry in driver_orders[selected_order]:
            speaker = entry["from"]
            message = entry["message"]
            timestamp = entry.get("timestamp", "")
            if speaker == "admin":
                st.markdown(f"<div style='color: #1e88e5'><b>Admin:</b> {message} <i>({timestamp})</i></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: #2e7d32'><b>{selected_driver}:</b> {message} <i>({timestamp})</i></div>", unsafe_allow_html=True)

        # Admin response form
        with st.form(f"driver_reply_form_{selected_driver}_{selected_order}"):
            reply = st.text_area("Your message to driver")
            submitted = st.form_submit_button("Send")
            if submitted and reply.strip():
                driver_orders[selected_order].append({
                    "from": "admin",
                    "message": reply.strip(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                save_chats(chats)
                st.success("Message sent!")

    else:
        st.info("No orders/messages for this driver yet.")

else:
    st.info("No driver messages yet.")



