import streamlit as st
import requests
from datetime import datetime
from modules.nav import SideBarLinks

st.set_page_config(layout='wide', page_title="Route Planner")

SideBarLinks()

st.markdown("""
<style>
.route-header {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
}

.route-header h1 {
    color: white;
    margin: 0;
}

.route-header p {
    color: #a0a0a0;
    margin: 0.5rem 0 0 0;
}

.order-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #dee2e6;
    transition: all 0.2s;
}

.order-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transform: translateX(4px);
}

.order-card.out_for_delivery {
    border-left-color: #ffc107;
    background: linear-gradient(135deg, #fff9e6, #ffffff);
}

.order-card.confirmed {
    border-left-color: #17a2b8;
}

.order-card.preparing {
    border-left-color: #6c757d;
}

.order-card.pending {
    border-left-color: #007bff;
}

.order-card.delivered {
    border-left-color: #28a745;
    opacity: 0.7;
}

.order-card.cancelled {
    border-left-color: #dc3545;
    opacity: 0.5;
}

.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status-out_for_delivery { background: #fff3cd; color: #856404; }
.status-confirmed { background: #d1ecf1; color: #0c5460; }
.status-preparing { background: #e2e3e5; color: #383d41; }
.status-pending { background: #cce5ff; color: #004085; }
.status-delivered { background: #d4edda; color: #155724; }
.status-cancelled { background: #f8d7da; color: #721c24; }

.stats-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
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
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="route-header">
    <h1>🗺️ Route Planner</h1>
    <p>Plan and manage your delivery routes, {st.session_state.get('first_name', 'Driver')}!</p>
</div>
""", unsafe_allow_html=True)

# Get driver ID from session
driver_id = st.session_state.get('driver_id')

if not driver_id:
    st.error("No driver ID found. Please log in again.")
    if st.button("Return to Home"):
        st.switch_page("Home.py")
    st.stop()

# API Base URL
API_BASE = f"http://web-api:4000/d/driver/{driver_id}"

# ---- Fetch orders ----
@st.cache_data(ttl=30)
def fetch_orders(driver_id):
    try:
        response = requests.get(f"http://web-api:4000/d/driver/{driver_id}/order")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching orders: {e}")
        return []

orders = fetch_orders(driver_id)

# Calculate stats
active_orders = [o for o in orders if o.get('status') in ['out_for_delivery', 'confirmed', 'preparing']]
pending_orders = [o for o in orders if o.get('status') == 'pending']
delivered_today = [o for o in orders if o.get('status') == 'delivered']

stat_cols = st.columns(4)
with stat_cols[0]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #ffc107;">{len(active_orders)}</div>
        <div class="stats-label">Active Deliveries</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[1]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #007bff;">{len(pending_orders)}</div>
        <div class="stats-label">Pending</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[2]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #28a745;">{len(delivered_today)}</div>
        <div class="stats-label">Delivered</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[3]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #1a1a2e;">{len(orders)}</div>
        <div class="stats-label">Total Orders</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Order Management")

filter_tab = st.radio(
    "Filter orders:",
    ["🚚 Active", "⏳ Pending", "✅ Delivered", "📋 All"],
    horizontal=True,
    label_visibility="collapsed"
)

if filter_tab == "Active":
    display_orders = [o for o in orders if o.get('status') in ['out_for_delivery', 'confirmed', 'preparing']]
elif filter_tab == "Pending":
    display_orders = [o for o in orders if o.get('status') == 'pending']
elif filter_tab == "Delivered":
    display_orders = [o for o in orders if o.get('status') == 'delivered']
else:
    display_orders = orders

if display_orders:
    for order in display_orders:
        order_id = order.get('orderID')
        status = order.get('status', 'pending')
        address = order.get('deliveryAddress', 'Unknown')
        qty = order.get('quantityOrdered', 0)
        scheduled = order.get('scheduledTime', 'N/A')
        
        status_labels = {
            'out_for_delivery': 'Out for Delivery',
            'confirmed': '✓ Confirmed',
            'preparing': 'Preparing',
            'pending': 'Pending',
            'delivered': '✅ Delivered',
            'cancelled': '❌ Cancelled'
        }
        
        with st.container():
            st.markdown(f"""
            <div class="order-card {status}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <strong style="font-size: 1.1rem;">Order #{order_id}</strong>
                        <span class="status-badge status-{status}" style="margin-left: 0.5rem;">{status.replace('_', ' ')}</span>
                    </div>
                    <div style="text-align: right; font-size: 0.85rem; color: #6c757d;">
                        Qty: {qty}
                    </div>
                </div>
                <div style="margin-top: 0.5rem;">
                    <div>📍 {address}</div>
                    <div style="color: #6c757d; font-size: 0.85rem;">📅 Scheduled: {scheduled}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if status in ['out_for_delivery', 'confirmed', 'preparing', 'pending']:
                btn_cols = st.columns([1, 1, 1])
                
                with btn_cols[0]:
                    if status != 'out_for_delivery' and st.button("Start", key=f"start_{order_id}", use_container_width=True):
                        try:
                            response = requests.put(
                                f"{API_BASE}/order/{order_id}",
                                json={"status": "out_for_delivery"}
                            )
                            if response.status_code == 200:
                                st.success("Started delivery!")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("Failed to update")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with btn_cols[1]:
                    if status == 'out_for_delivery' and st.button("Deliver", key=f"deliver_{order_id}", use_container_width=True):
                        try:
                            response = requests.put(
                                f"{API_BASE}/order/{order_id}",
                                json={"status": "delivered"}
                            )
                            if response.status_code == 200:
                                st.success("Marked as delivered!")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("Failed to update")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with btn_cols[2]:
                    if st.button("⚠️ Issue", key=f"issue_{order_id}", use_container_width=True):
                        st.session_state[f'show_issue_{order_id}'] = True
                
                # Issue reporting form
                if st.session_state.get(f'show_issue_{order_id}', False):
                    with st.expander("Report Delivery Issue", expanded=True):
                        issue_desc = st.text_area("Describe the issue:", key=f"issue_desc_{order_id}")
                        issue_cols = st.columns(2)
                        with issue_cols[0]:
                            if st.button("Submit Issue", key=f"submit_issue_{order_id}"):
                                if issue_desc:
                                    try:
                                        response = requests.post(
                                            f"http://web-api:4000/d/driver/{order_id}/order/deliveryIssue",
                                            json={
                                                "issueID": int(datetime.now().timestamp()),
                                                "timestamp": datetime.now().strftime('%Y-%m-%d'),
                                                "description": issue_desc
                                            }
                                        )
                                        if response.status_code == 201:
                                            st.success("Issue reported!")
                                            st.session_state[f'show_issue_{order_id}'] = False
                                            st.rerun()
                                        else:
                                            st.error("Failed to report issue")
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                                else:
                                    st.warning("Please describe the issue")
                        with issue_cols[1]:
                            if st.button("Cancel", key=f"cancel_issue_{order_id}"):
                                st.session_state[f'show_issue_{order_id}'] = False
                                st.rerun()
                
                st.markdown("---")
else:
    st.info("No orders found in this category.")

st.divider()
col_back, col_refresh, col_spacer = st.columns([1, 1, 2])
with col_back:
    if st.button("← Back to Driver Home"):
        st.switch_page("pages/22_Driver_Home.py")
with col_refresh:
    if st.button("🔄 Refresh Orders"):
        st.cache_data.clear()
        st.rerun()
