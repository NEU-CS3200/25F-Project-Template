import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_URL = "http://web-api:4000"

if 'user_id' not in st.session_state:
    st.switch_page('Home.py')

user_id = st.session_state['user_id']
first_name = st.session_state['first_name']
role = st.session_state['role']

col_title, col_btn = st.columns([4, 1])
with col_title:
    st.title(f"Welcome, {first_name}!")
with col_btn:
    st.write("")
    if st.button("Switch User", key="switch_user_btn", use_container_width=True):
        st.switch_page('pages/30_Users.py')

role_descriptions = {
    'student': 'College Student Budget Dashboard',
    'professional': 'Professional Finance Dashboard',
    'treasurer': 'Club Treasury Dashboard',
    'family': 'Family Budget Dashboard'
}
st.write(f"### {role_descriptions.get(role, 'Budget Dashboard')}")

st.write("---")

# Fetch totals from API
try:
    response = requests.get(f"{API_URL}/budgets/user/{user_id}/totals")
    if response.status_code == 200:
        totals = response.json()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Income", value=f"${totals['income']:,.0f}")
            if st.button("View Income →", key="link_income", use_container_width=True):
                st.session_state['budget_tab'] = 2
                st.session_state['budget_tab_action'] = 'link'
                st.switch_page('pages/10_Budget_Tracker.py')

        with col2:
            st.metric(label="Expenditures", value=f"${totals['expenditures']:,.0f}")
            if st.button("View Expenses →", key="link_expenses", use_container_width=True):
                st.session_state['budget_tab'] = 3
                st.session_state['budget_tab_action'] = 'link'
                st.switch_page('pages/10_Budget_Tracker.py')

        with col3:
            st.metric(label="Net Position", value=f"${totals['netPosition']:,.0f}",
                     delta=f"{totals['savingsRate']}% savings rate")

        with col4:
            st.metric(label="Total Savings", value=f"${totals['savings']:,.0f}")
            if st.button("View Savings →", key="link_savings", use_container_width=True):
                st.switch_page('pages/12_Savings.py')
    else:
        st.error("Could not load financial data")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to API: {str(e)}")

st.write("---")

# Quick actions
st.write("### Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Budget Tracker", type='primary', use_container_width=True):
        st.switch_page('pages/10_Budget_Tracker.py')

with col2:
    if st.button("Savings", type='primary', use_container_width=True):
        st.switch_page('pages/12_Savings.py')

with col3:
    if st.button("AI Insights", type='primary', use_container_width=True):
        st.switch_page('pages/20_AI_Insights.py')

with col4:
    if st.button("Other", type='secondary', use_container_width=True):
        st.switch_page('pages/13_Other.py')

st.write("---")

# Monthly Bar Charts - Last 6 Months
st.write("### Monthly Trends (Last 6 Months)")

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str[:10], '%Y-%m-%d')
    except:
        try:
            return datetime.strptime(date_str[:16], '%a, %d %b %Y')
        except:
            return None

def get_month_name(dt):
    return dt.strftime('%b %Y')

try:
    response = requests.get(f"{API_URL}/transactions/user/{user_id}")
    if response.status_code == 200:
        transactions = response.json()
        
        # Get last 6 months
        today = datetime.now()
        months = []
        for i in range(5, -1, -1):
            month_date = today - timedelta(days=i*30)
            months.append(month_date.strftime('%b %Y'))
        
        # Initialize data
        income_by_month = {m: 0 for m in months}
        expense_by_month = {m: 0 for m in months}
        
        # Process transactions
        for txn in transactions:
            txn_date = parse_date(txn.get('date'))
            if txn_date:
                month_key = get_month_name(txn_date)
                if month_key in income_by_month:
                    amount = float(txn.get('amount', 0))
                    if amount > 0:
                        income_by_month[month_key] += amount
                    else:
                        expense_by_month[month_key] += abs(amount)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Monthly Income")
            income_df = pd.DataFrame({
                'Month': list(income_by_month.keys()),
                'Income': list(income_by_month.values())
            })
            fig_income = px.bar(income_df, x='Month', y='Income', 
                               color_discrete_sequence=['#00CC96'])
            fig_income.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis_title="",
                yaxis_title="Amount ($)",
                showlegend=False
            )
            st.plotly_chart(fig_income, use_container_width=True)
        
        with col2:
            st.write("#### Monthly Expenses")
            expense_df = pd.DataFrame({
                'Month': list(expense_by_month.keys()),
                'Expenses': list(expense_by_month.values())
            })
            fig_expense = px.bar(expense_df, x='Month', y='Expenses',
                                color_discrete_sequence=['#EF553B'])
            fig_expense.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis_title="",
                yaxis_title="Amount ($)",
                showlegend=False
            )
            st.plotly_chart(fig_expense, use_container_width=True)
except:
    st.error("Could not load monthly data")

st.write("---")

# Pie Charts
st.write("### Spending & Income Breakdown")

col1, col2 = st.columns(2)

with col1:
    st.write("#### Expenses by Category")
    try:
        response = requests.get(f"{API_URL}/transactions/user/{user_id}/expenses/by-category")
        if response.status_code == 200:
            categories = response.json()
            if categories:
                df = pd.DataFrame(categories)
                df.columns = ['Category', 'Amount']
                fig = px.pie(df, values='Amount', names='Category', hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expense data yet")
    except:
        st.error("Could not load expense data")

with col2:
    st.write("#### Income by Source")
    try:
        response = requests.get(f"{API_URL}/transactions/user/{user_id}/income/by-source")
        if response.status_code == 200:
            sources = response.json()
            if sources:
                df = pd.DataFrame(sources)
                df.columns = ['Source', 'Amount']
                fig = px.pie(df, values='Amount', names='Source', hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No income data yet")
    except:
        st.error("Could not load income data")

st.write("---")

# Recent transactions
col_header, col_link = st.columns([3, 1])
with col_header:
    st.write("### Recent Transactions")
with col_link:
    if st.button("View All →", key="link_all_txns", use_container_width=True):
        st.session_state['budget_tab'] = 4
        st.session_state['budget_tab_action'] = 'link'
        st.switch_page('pages/10_Budget_Tracker.py')

try:
    response = requests.get(f"{API_URL}/transactions/user/{user_id}")
    if response.status_code == 200:
        transactions = response.json()[:5]

        if transactions:
            for txn in transactions:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{txn['description']}**")
                    st.caption(f"{txn['categoryName'] or 'Uncategorized'} • {txn['date'][:16]}")
                with col2:
                    amount = float(txn['amount'])
                    if amount > 0:
                        st.write(f":green[+${amount:,.0f}]")
                    else:
                        st.write(f":red[-${abs(amount):,.0f}]")
                with col3:
                    st.write(txn['method'] or '')
                st.write("---")
        else:
            st.info("No transactions found")
    else:
        st.error("Could not load transactions")
except requests.exceptions.RequestException as e:
    st.error(f"Error: {str(e)}")