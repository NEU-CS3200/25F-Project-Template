import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime

API_BASE = "http://web-api:4000/a"

st.set_page_config(layout="wide", page_title="Customer Accounts")
SideBarLinks()

st.markdown("""
<style>
.page-header {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
}

.page-header h1 {
    color: white;
    margin: 0;
}

.page-header p {
    color: #a0a0a0;
    margin: 0.5rem 0 0 0;
}

.customer-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #28a745;
}

.customer-name {
    font-size: 1.15rem;
    font-weight: 600;
    color: #1a1a2e;
    margin: 0;
}

.customer-email {
    color: #6c757d;
    font-size: 0.9rem;
    margin: 0.25rem 0 0 0;
}

.message-card {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-top: 0.5rem;
    border-left: 3px solid #007bff;
}

.message-content {
    font-style: italic;
    color: #495057;
    font-size: 0.95rem;
}

.message-date {
    font-size: 0.75rem;
    color: #adb5bd;
    margin-top: 0.25rem;
}

.stats-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.stats-number {
    font-size: 2rem;
    font-weight: bold;
    color: #1a1a2e;
}

.stats-label {
    font-size: 0.85rem;
    color: #6c757d;
}

.no-messages {
    color: #adb5bd;
    font-style: italic;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>Customer Accounts & Feedback</h1>
    <p>View active customer accounts, read their messages, and respond directly</p>
</div>
""", unsafe_allow_html=True)


@st.cache_data(ttl=30)
def load_customers():
    """Fetch all customers from API"""
    try:
        r = requests.get(f"{API_BASE}/admin/customers")
        if r.status_code == 200:
            return r.json()
        else:
            return []
    except Exception as e:
        st.error(f"Error loading customers: {e}")
        return []


def load_customer_messages(customer_id):
    """Fetch messages for a specific customer"""
    try:
        r = requests.get(f"{API_BASE}/customer/{customer_id}/customermessages")
        if r.status_code == 200:
            return r.json()
        else:
            return []
    except Exception:
        return []


def send_message(customer_id, content):
    """Send a message to a customer"""
    try:
        message_id = int(datetime.now().timestamp() * 1000) % 2147483647
        payload = {
            "messageID": message_id,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d")
        }
        r = requests.post(f"{API_BASE}/customer/{customer_id}/customermessages", json=payload)
        return r.status_code == 201
    except Exception:
        return False


def delete_customer(customer_id):
    """Delete a customer account"""
    try:
        r = requests.delete(f"{API_BASE}/customers/{customer_id}")
        return r.status_code == 200
    except Exception:
        return False


customers = load_customers()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{len(customers)}</div>
        <div class="stats-label">Total Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    customers_with_messages = 0
    for c in customers:
        msgs = load_customer_messages(c.get('customerID'))
        if msgs:
            customers_with_messages += 1
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{customers_with_messages}</div>
        <div class="stats-label">With Messages</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{len(customers) - customers_with_messages}</div>
        <div class="stats-label">No Messages</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

search_col, filter_col = st.columns([3, 1])
with search_col:
    search_term = st.text_input("🔍 Search customers by name or email", placeholder="Type to search...")
with filter_col:
    show_with_messages = st.checkbox("Only show customers with messages", value=False)

filtered_customers = customers
if search_term:
    search_lower = search_term.lower()
    filtered_customers = [
        c for c in filtered_customers
        if search_lower in c.get('firstName', '').lower()
        or search_lower in c.get('lastName', '').lower()
        or search_lower in c.get('email', '').lower()
    ]

st.markdown(f"**Showing {len(filtered_customers)} customers**")

if not filtered_customers:
    st.info("No customers found.")
else:
    for cust in filtered_customers:
        cust_id = cust.get('customerID')
        first_name = cust.get('firstName', 'Unknown')
        last_name = cust.get('lastName', '')
        full_name = f"{first_name} {last_name}".strip()
        email = cust.get('email', 'No email')
        
        messages = load_customer_messages(cust_id)
        
        if show_with_messages and not messages:
            continue
        
        with st.container():
            st.markdown(f"""
            <div class="customer-card">
                <div class="customer-name">👤 {full_name}</div>
                <div class="customer-email">📧 {email}</div>
            </div>
            """, unsafe_allow_html=True)
            
            msg_col, action_col = st.columns([3, 1])
            
            with msg_col:
                if messages:
                    st.markdown("**Recent Messages:**")
                    sorted_msgs = sorted(
                        messages, 
                        key=lambda x: x.get('timestamp', ''), 
                        reverse=True
                    )[:3]
                    
                    for msg in sorted_msgs:
                        content = msg.get('content', '')[:150]
                        if len(msg.get('content', '')) > 150:
                            content += '...'
                        timestamp = msg.get('timestamp', 'Unknown date')
                        
                        st.markdown(f"""
                        <div class="message-card">
                            <div class="message-content">"{content}"</div>
                            <div class="message-date">📅 {timestamp}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<p class="no-messages">No messages from this customer yet.</p>', unsafe_allow_html=True)
            
            with action_col:
                st.markdown("**Actions:**")
                
                with st.expander("💬 Reply"):
                    reply_msg = st.text_area(
                        "Your message",
                        placeholder="Type your reply here...",
                        key=f"reply_text_{cust_id}",
                        height=100
                    )
                    if st.button("📤 Send Reply", key=f"send_reply_{cust_id}", use_container_width=True):
                        if reply_msg.strip():
                            if send_message(cust_id, reply_msg):
                                st.success("Message sent!")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("Failed to send message")
                        else:
                            st.warning("Please enter a message")
                
                if st.button("🗑️ Delete Account", key=f"delete_{cust_id}", use_container_width=True):
                    st.session_state[f'confirm_delete_{cust_id}'] = True
                
                if st.session_state.get(f'confirm_delete_{cust_id}', False):
                    st.warning(f"Delete {full_name}?")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("Yes", key=f"yes_del_{cust_id}", use_container_width=True):
                            if delete_customer(cust_id):
                                st.success("Customer deleted!")
                                st.session_state[f'confirm_delete_{cust_id}'] = False
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("Failed to delete")
                    with col_no:
                        if st.button("No", key=f"no_del_{cust_id}", use_container_width=True):
                            st.session_state[f'confirm_delete_{cust_id}'] = False
                            st.rerun()
            
            st.markdown("---")
