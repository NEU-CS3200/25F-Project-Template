import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()
from modules.nav import BackToDashboard
BackToDashboard()

API_URL = "http://web-api:4000"

if 'user_id' not in st.session_state:
    st.switch_page('Home.py')

user_id = st.session_state['user_id']
first_name = st.session_state['first_name']
role = st.session_state.get('role', '')

# Only family managers should see this page
if role != 'family':
    st.warning("This page is only available for family budget managers.")
    st.stop()

st.title("Family Members")
st.write("Manage and monitor family member accounts")

st.write("---")

# Fetch dependents
try:
    response = requests.get(f"{API_URL}/users/{user_id}/dependents")
    if response.status_code == 200:
        dependents = response.json()
        
        if dependents:
            st.write(f"### {first_name}'s Family ({len(dependents)} members)")
            st.write("")
            
            for dep in dependents:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.write("👤")
                    
                    with col2:
                        st.write(f"**{dep['name']}**")
                        st.caption(f"{dep['userType']} • {dep['email']}")
                        
                        # Get their account info
                        acc_response = requests.get(f"{API_URL}/users/{dep['userID']}/accounts")
                        if acc_response.status_code == 200:
                            accounts = acc_response.json()
                            if accounts:
                                total_balance = sum(float(a['balance']) for a in accounts)
                                st.write(f"Account Balance: ${total_balance:,.2f}")
                            else:
                                st.write("No accounts linked")
                        
                        # Get their recent transactions
                        txn_response = requests.get(f"{API_URL}/transactions/user/{dep['userID']}")
                        if txn_response.status_code == 200:
                            txns = txn_response.json()
                            if txns:
                                recent = txns[:3]
                                st.write("**Recent Activity:**")
                                for t in recent:
                                    amt = float(t['amount'])
                                    if amt > 0:
                                        st.caption(f"• {t['description']}: :green[+${amt:,.0f}]")
                                    else:
                                        st.caption(f"• {t['description']}: :red[-${abs(amt):,.0f}]")
                            else:
                                st.caption("No recent transactions")
                    
                    st.write("---")
        else:
            st.info("No family members linked to your account.")
            
except Exception as e:
    st.error(f"Could not load family members: {str(e)}")

st.write("---")

# Add family member form
st.write("### Add Family Member")

with st.form("add_dependent"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    user_type = st.selectbox("Role", ["Child", "Spouse", "Other"])
    
    submitted = st.form_submit_button("Add Member")
    
    if submitted:
        if name and email:
            data = {
                "name": name,
                "email": email,
                "userType": user_type,
                "supervisorUserID": user_id
            }
            post_response = requests.post(f"{API_URL}/users/", json=data)
            if post_response.status_code == 201:
                st.success(f"Added {name} to your family!")
                st.rerun()
            else:
                st.error("Failed to add family member")
        else:
            st.warning("Please fill in name and email")

st.write("---")

# Family spending summary
st.write("### Family Spending Overview")

try:
    # Get main user totals
    main_response = requests.get(f"{API_URL}/budgets/user/{user_id}/totals")
    if main_response.status_code == 200:
        main_totals = main_response.json()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Household Income", f"${main_totals['income']:,.0f}")
        with col2:
            st.metric("Household Spending", f"${main_totals['expenditures']:,.0f}")
        with col3:
            st.metric("Household Savings", f"${main_totals['netPosition']:,.0f}")

except Exception as e:
    st.error(f"Could not load family overview: {str(e)}")