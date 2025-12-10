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

st.title("User Personas")
st.write("Select a user to view their financial profile")

st.write("---")

# User data with descriptions
users = [
    {
        'id': 1,
        'name': 'Alex Chen',
        'type': 'College Student',
        'role': 'student',
        'description': 'Junior at Northeastern. Receives $800/month stipend + $600/month from part-time job.',
        'pain_points': [
            "Doesn't know where money goes",
            "Overspends on food and entertainment",
            "Can't save for emergencies"
        ]
    },
    {
        'id': 2,
        'name': 'Jamie Rodriguez',
        'type': 'Working Professional',
        'role': 'professional',
        'description': '32-year-old marketing manager. $120k household income. Manages mortgage and investments.',
        'pain_points': [
            "Can't see aggregate spending across accounts",
            "Wants to track financial goals",
            "Needs trend analysis for forecasting"
        ]
    },
    {
        'id': 3,
        'name': 'Jordan Park',
        'type': 'Club Treasurer',
        'role': 'treasurer',
        'description': 'Treasurer of Finance and Investment Club. Manages $15k annual budget.',
        'pain_points': [
            "Manual reimbursement process",
            "Hard to track budget by project",
            "No automated reporting"
        ]
    },
    {
        'id': 4,
        'name': 'Sarah Kim',
        'type': 'Family Budget Manager',
        'role': 'family',
        'description': '45-year-old parent of two kids. Married. Household income $300k.',
        'pain_points': [
            "Hard to track spending across family members",
            "Wants to teach kids about money",
            "Needs to plan for college expenses"
        ]
    }
]

# Display user cards in 2 columns
col1, col2 = st.columns(2)

for i, user in enumerate(users):
    with col1 if i % 2 == 0 else col2:
        # Check if this user is selected
        is_selected = st.session_state.get('user_id') == user['id']
        
        # Card container
        with st.container():
            if is_selected:
                st.success(f"**{user['name']}** - Currently Selected")
            else:
                st.write(f"**{user['name']}**")
            
            st.caption(user['type'])
            st.write(user['description'])
            
            # Fetch financial summary
            try:
                response = requests.get(f"{API_URL}/budgets/user/{user['id']}/totals")
                if response.status_code == 200:
                    totals = response.json()
                    
                    mcol1, mcol2, mcol3 = st.columns(3)
                    with mcol1:
                        st.metric("Income", f"${totals['income']:,.0f}")
                    with mcol2:
                        st.metric("Spending", f"${totals['expenditures']:,.0f}")
                    with mcol3:
                        net = totals['netPosition']
                        if net >= 0:
                            st.metric("Net", f"${net:,.0f}")
                        else:
                            st.metric("Net", f"-${abs(net):,.0f}")
            except:
                pass
            
            # Pain points
            st.write("**Challenges:**")
            for point in user['pain_points']:
                st.caption(f"• {point}")
            
            # Select button
            if not is_selected:
                if st.button(f"Switch to {user['name']}", key=f"select_{user['id']}", use_container_width=True):
                    st.session_state['authenticated'] = True
                    st.session_state['user_id'] = user['id']
                    st.session_state['first_name'] = user['name'].split()[0]
                    st.session_state['role'] = user['role']
                    st.switch_page('pages/00_User_Home.py')
            
            st.write("---")