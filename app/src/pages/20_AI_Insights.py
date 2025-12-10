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

st.title("AI Insights & Recommendations")
st.write("Personalized financial guidance powered by intelligent analysis")

st.write("---")

# Financial Health Score
st.write("### Financial Health Score")

try:
    response = requests.get(f"{API_URL}/insights/user/{user_id}/health-score")
    if response.status_code == 200:
        health = response.json()
        
        score = health['score']
        label = health['label']
        
        # Color based on score
        if score >= 80:
            color = "green"
        elif score >= 60:
            color = "blue"
        elif score >= 40:
            color = "orange"
        else:
            color = "red"
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.metric("Your Score", f"{score}/100", label)
            st.progress(score / 100)
        
        with col2:
            st.metric("Savings Rate", f"{health['savingsRate']}%")
        
        with col3:
            net = health['netPosition']
            if net >= 0:
                st.metric("Net Position", f"${net:,.0f}", "Positive")
            else:
                st.metric("Net Position", f"-${abs(net):,.0f}", "Negative")

except Exception as e:
    st.error(f"Could not load health score: {str(e)}")

st.write("---")

# Key Insights
st.write("### Key Insights")

try:
    response = requests.get(f"{API_URL}/insights/user/{user_id}")
    if response.status_code == 200:
        insights = response.json()
        
        if insights:
            for insight in insights:
                st.info(insight)
        else:
            st.success("No issues detected - your finances look healthy!")

except Exception as e:
    st.error(f"Could not load insights: {str(e)}")

st.write("---")

# Personalized Recommendations
st.write("### Personalized Recommendations")

try:
    response = requests.get(f"{API_URL}/insights/user/{user_id}/recommendations")
    if response.status_code == 200:
        recommendations = response.json()
        
        if recommendations:
            for rec in recommendations:
                impact = rec['impact']
                
                # Set color based on impact
                if impact == 'Critical':
                    box_type = 'error'
                elif impact == 'High':
                    box_type = 'warning'
                elif impact == 'Positive':
                    box_type = 'success'
                else:
                    box_type = 'info'
                
                with st.container():
                    st.write(f"**{rec['title']}**")
                    st.write(rec['description'])
                    st.caption(f"Impact: {impact} | Action: {rec['action']}")
                    st.write("---")
        else:
            st.success("No specific recommendations right now - keep up the good work!")

except Exception as e:
    st.error(f"Could not load recommendations: {str(e)}")

st.write("---")

# Spending Optimization
st.write("### Spending Optimization Opportunities")

try:
    response = requests.get(f"{API_URL}/transactions/user/{user_id}/expenses/by-category")
    if response.status_code == 200:
        categories = response.json()
        
        if categories:
            st.write("Areas where you could potentially save money:")
            st.write("")
            
            for cat in categories[:3]:
                spent = float(cat['total'])
                potential = spent * 0.15  # 15% potential savings
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{cat['category']}**")
                    st.caption(f"Current: ${spent:,.0f}/month")
                
                with col2:
                    st.write(f":green[Save ${potential:,.0f}]")
                    st.caption("15% reduction")
                
                with col3:
                    annual = potential * 12
                    st.write(f"${annual:,.0f}/year")
                
                st.write("---")
        else:
            st.info("Not enough spending data to analyze yet")

except Exception as e:
    st.error(f"Could not load spending data: {str(e)}")

# Tips based on role
st.write("### Tips for You")

role = st.session_state.get('role', '')

if role == 'student':
    st.write("""
    **College Student Tips:**
    - Track every purchase, especially food delivery and entertainment
    - Start an emergency fund, even with just $25/month
    - Use student discounts wherever possible
    - Consider meal prepping to reduce food costs
    """)
elif role == 'professional':
    st.write("""
    **Working Professional Tips:**
    - Maximize your 401(k) employer match
    - Review subscriptions quarterly and cancel unused ones
    - Automate savings transfers on payday
    - Consider tax-advantaged accounts like HSA or Roth IRA
    """)
elif role == 'treasurer':
    st.write("""
    **Club Treasurer Tips:**
    - Keep detailed records of all transactions
    - Set aside funds for unexpected expenses
    - Create budget categories for each major event
    - Review spending against budget monthly
    """)
elif role == 'family':
    st.write("""
    **Family Budget Tips:**
    - Involve family members in budget discussions
    - Set up separate savings for each major goal
    - Review and adjust budgets as kids' needs change
    - Consider 529 plans for education savings
    """)