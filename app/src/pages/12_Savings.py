import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks, BackToDashboard

st.set_page_config(layout='wide')
SideBarLinks()
BackToDashboard()

API_URL = "http://web-api:4000"

if 'user_id' not in st.session_state:
    st.switch_page('Home.py')

user_id = st.session_state['user_id']
first_name = st.session_state['first_name']

# Callback functions
def delete_saving(saving_id):
    requests.delete(f"{API_URL}/savings/{saving_id}")

def start_add_money(saving_id, current_amount, goal_name):
    st.session_state['modifying_saving'] = saving_id
    st.session_state['modify_action'] = 'add'
    st.session_state['modify_current'] = current_amount
    st.session_state['modify_goal_name'] = goal_name

def start_remove_money(saving_id, current_amount, goal_name):
    st.session_state['modifying_saving'] = saving_id
    st.session_state['modify_action'] = 'remove'
    st.session_state['modify_current'] = current_amount
    st.session_state['modify_goal_name'] = goal_name

def cancel_modify():
    st.session_state['modifying_saving'] = None
    st.session_state['modify_action'] = None

st.title("Savings Goals")
st.write("Track your progress toward financial goals")

st.write("---")

# Display savings goals
try:
    response = requests.get(f"{API_URL}/savings/user/{user_id}")
    if response.status_code == 200:
        savings = response.json()
        
        if savings:
            # Summary
            total_saved = sum(float(s['currAmt']) for s in savings)
            total_target = sum(float(s['targAmt']) for s in savings)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Saved", f"${total_saved:,.0f}")
            with col2:
                st.metric("Total Target", f"${total_target:,.0f}")
            with col3:
                overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0
                st.metric("Overall Progress", f"{overall_progress:.1f}%")
            
            st.write("---")
            
            # Add new savings goal button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("### Your Goals")
            with col2:
                if st.button("Add Savings Goal", type='primary', key='add_saving'):
                    st.session_state['show_saving_form'] = True
        else:
            # No savings yet - show button prominently
            st.info("No savings goals yet. Create your first one!")
            if st.button("Add Savings Goal", type='primary', key='add_saving'):
                st.session_state['show_saving_form'] = True

        if st.session_state.get('show_saving_form', False):
            with st.form("saving_form"):
                st.write("#### Create New Savings Goal")
                goal_name = st.text_input("Goal Name")
                target_amount = st.number_input("Target Amount ($)", min_value=1.0, step=100.0)
                current_amount = st.number_input("Current Amount ($)", min_value=0.0, step=10.0)
                monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, step=10.0)
                target_date = st.date_input("Target Date")
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Create Goal")
                with col2:
                    cancelled = st.form_submit_button("Cancel")
                
                if submitted:
                    if goal_name:
                        data = {
                            "goalName": goal_name,
                            "targAmt": target_amount,
                            "currAmt": current_amount,
                            "monthlyContribution": monthly_contribution,
                            "targetDeadline": str(target_date),
                            "userID": user_id
                        }
                        post_response = requests.post(f"{API_URL}/savings/", json=data)
                        if post_response.status_code == 201:
                            st.success("Savings goal created!")
                            st.session_state['show_saving_form'] = False
                            st.rerun()
                        else:
                            st.error("Failed to create savings goal")
                    else:
                        st.warning("Please enter a goal name")
                if cancelled:
                    st.session_state['show_saving_form'] = False
                    st.rerun()
        
        if savings:
            # Check if we're modifying a saving (add or remove)
            if st.session_state.get('modifying_saving'):
                saving_id = st.session_state['modifying_saving']
                goal_name = st.session_state.get('modify_goal_name', 'Goal')
                action = st.session_state.get('modify_action', 'add')
                current = st.session_state.get('modify_current', 0)
                
                if action == 'add':
                    with st.form("add_money_form"):
                        st.write(f"#### 💰 Add Money to {goal_name}")
                        amount = st.number_input("Amount to Add ($)", min_value=0.01, step=10.0, value=10.0)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            add_submitted = st.form_submit_button("Add Money", type="primary")
                        with col2:
                            add_cancelled = st.form_submit_button("Cancel")
                        
                        if add_submitted:
                            response = requests.put(f"{API_URL}/savings/{saving_id}/add", json={"amount": float(amount)})
                            if response.status_code == 200:
                                st.success(f"Added ${amount:,.2f} to {goal_name}!")
                                st.session_state['modifying_saving'] = None
                                st.session_state['modify_action'] = None
                                st.rerun()
                            else:
                                st.error("Failed to add money")
                        if add_cancelled:
                            st.session_state['modifying_saving'] = None
                            st.session_state['modify_action'] = None
                            st.rerun()
                else:
                    with st.form("remove_money_form"):
                        st.write(f"#### 💸 Remove Money from {goal_name}")
                        st.caption(f"Current balance: ${current:,.0f}")
                        max_val = float(current) if current > 0 else 0.01
                        amount = st.number_input("Amount to Remove ($)", min_value=0.01, max_value=max_val, step=10.0, value=min(10.0, max_val))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            remove_submitted = st.form_submit_button("Remove Money", type="primary")
                        with col2:
                            remove_cancelled = st.form_submit_button("Cancel")
                        
                        if remove_submitted:
                            response = requests.put(f"{API_URL}/savings/{saving_id}/remove", json={"amount": float(amount)})
                            if response.status_code == 200:
                                st.success(f"Removed ${amount:,.2f} from {goal_name}!")
                                st.session_state['modifying_saving'] = None
                                st.session_state['modify_action'] = None
                                st.rerun()
                            else:
                                st.error("Failed to remove money")
                        if remove_cancelled:
                            st.session_state['modifying_saving'] = None
                            st.session_state['modify_action'] = None
                            st.rerun()
                
                st.write("---")
            
            for saving in savings:
                current = float(saving['currAmt'])
                target = float(saving['targAmt'])
                progress = min(current / target, 1.0) if target > 0 else 0
                monthly = float(saving['monthlyContribution']) if saving['monthlyContribution'] else 0
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{saving['goalName']}**")
                    st.progress(progress)
                    st.caption(f"${current:,.0f} / ${target:,.0f} ({progress*100:.0f}%)")
                    if monthly > 0:
                        st.caption(f"Monthly contribution: ${monthly:,.0f}")
                    if saving.get('targetDeadline'):
                        st.caption(f"Target date: {saving['targetDeadline'][:10]}")
                
                with col2:
                    st.button("💰 Add", key=f"add_{saving['savingID']}",
                             on_click=start_add_money,
                             args=(saving['savingID'], current, saving['goalName']))
                    st.button("💸 Remove", key=f"remove_{saving['savingID']}",
                             on_click=start_remove_money,
                             args=(saving['savingID'], current, saving['goalName']))
                    st.button("🗑️ Delete", key=f"del_{saving['savingID']}",
                             on_click=delete_saving,
                             args=(saving['savingID'],))
                
                st.write("---")
    else:
        st.error("Could not load savings data")
except requests.exceptions.RequestException as e:
    st.error(f"Error: {str(e)}")