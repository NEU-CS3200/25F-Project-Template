import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from modules.nav import SideBarLinks, BackToDashboard

st.set_page_config(layout='wide')
SideBarLinks()
BackToDashboard()

API_URL = "http://web-api:4000"

if 'user_id' not in st.session_state:
    st.switch_page('Home.py')

user_id = st.session_state['user_id']
first_name = st.session_state['first_name']

# Hardcoded category mappings
EXPENSE_CATEGORIES = {
    "Food & Dining": 1,
    "Entertainment": 2,
    "Housing": 3,
    "Transportation": 4,
    "Personal & Other": 5,
    "Healthcare": 6,
    "Education": 7,
    "Shopping": 8,
    "Utilities": 9,
    "Subscriptions": 10
}

INCOME_CATEGORY_ID = 11

# Callback functions
def delete_transaction(txn_id):
    requests.delete(f"{API_URL}/transactions/{txn_id}")

def delete_budget(budget_id):
    requests.delete(f"{API_URL}/budgets/{budget_id}")

def edit_total_budget(budget):
    st.session_state['edit_total_budget'] = budget
    st.session_state['edit_total_limit'] = float(budget.get('limitAmount', 0)) if budget else 0.0

def save_total_budget(existing, new_limit, user_id):
    if existing:
        requests.put(f"{API_URL}/budgets/{existing['budgetID']}", json={
            "name": "Total Budget",
            "limitAmount": new_limit,
            "budgetType": "total",
            "categoryID": None
        })
    else:
        requests.post(f"{API_URL}/budgets/", json={
            "name": "Total Budget",
            "limitAmount": new_limit,
            "budgetType": "total",
            "userID": user_id,
            "categoryID": None
        })
    st.session_state['edit_total_budget'] = None

def cancel_total_edit():
    st.session_state['edit_total_budget'] = None

def edit_category_budget(cat_id, cat_name, existing):
    st.session_state['edit_category_id'] = cat_id
    st.session_state['edit_category_name'] = cat_name
    st.session_state['edit_category_budget'] = existing
    st.session_state['edit_category_limit'] = float(existing.get('limitAmount', 0)) if existing else 0.0

def save_category_budget(existing, cat_id, cat_name, new_limit, user_id):
    if existing:
        requests.put(f"{API_URL}/budgets/{existing['budgetID']}", json={
            "name": cat_name,
            "limitAmount": new_limit,
            "budgetType": "category",
            "categoryID": cat_id
        })
    else:
        requests.post(f"{API_URL}/budgets/", json={
            "name": cat_name,
            "limitAmount": new_limit,
            "budgetType": "category",
            "userID": user_id,
            "categoryID": cat_id
        })
    st.session_state['edit_category_id'] = None
    st.session_state['edit_category_name'] = None
    st.session_state['edit_category_budget'] = None

def cancel_category_edit():
    st.session_state['edit_category_id'] = None
    st.session_state['edit_category_name'] = None
    st.session_state['edit_category_budget'] = None

# Helper functions
def convert_to_csv(transactions):
    df = pd.DataFrame(transactions)
    columns_to_export = ['date', 'description', 'amount', 'categoryName', 'method', 'source', 'budgetName']
    available_cols = [c for c in columns_to_export if c in df.columns]
    return df[available_cols].to_csv(index=False)

def format_date(date_str):
    if not date_str:
        return "Unknown"
    try:
        dt = datetime.strptime(date_str[:10], '%Y-%m-%d')
        return dt.strftime('%b %d, %Y')
    except:
        try:
            dt = datetime.strptime(date_str[:16], '%a, %d %b %Y')
            return dt.strftime('%b %d, %Y')
        except:
            return date_str[:16] if len(date_str) >= 16 else date_str

def filter_transactions(transactions, search_term):
    if not transactions:
        return []
    
    filtered = transactions
    
    if search_term:
        search_lower = search_term.lower()
        filtered = [t for t in filtered if 
            search_lower in (t.get('description') or '').lower() or
            search_lower in (t.get('categoryName') or '').lower() or
            search_lower in (t.get('source') or '').lower() or
            search_lower in (t.get('method') or '').lower() or
            search_lower in (t.get('budgetName') or '').lower() or
            search_lower in str(abs(float(t.get('amount', 0)))) or
            search_lower.replace('$', '') in str(abs(float(t.get('amount', 0))))
        ]
    
    return filtered

# Page header
st.title("Budget Tracker")

st.write("---")

# Tab navigation
tab_names = ["Totals", "Budget Manager", "Income", "Expenditures", "All Transactions"]

if 'budget_tab' not in st.session_state:
    st.session_state['budget_tab'] = 0

current_tab = st.session_state['budget_tab']

cols = st.columns(len(tab_names))
for i, (col, name) in enumerate(zip(cols, tab_names)):
    with col:
        if i == current_tab:
            st.button(name, key=f"tab_{i}", type="primary", use_container_width=True, disabled=True)
        else:
            if st.button(name, key=f"tab_{i}", use_container_width=True):
                st.session_state['budget_tab'] = i
                st.rerun()

st.write("---")

# Totals Tab
if current_tab == 0:
    st.write("### Financial Overview")
    
    response = requests.get(f"{API_URL}/budgets/user/{user_id}/totals")
    if response.status_code == 200:
        totals = response.json()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Income", f"${float(totals.get('income', 0)):,.0f}")
        with col2:
            st.metric("Total Expenses", f"${float(totals.get('expenditures', 0)):,.0f}")
        with col3:
            st.metric("Net", f"${float(totals.get('netPosition', 0)):,.0f}")
        with col4:
            st.metric("Savings Rate", f"{float(totals.get('savingsRate', 0)):,.0f}%")
    else:
        st.error("Could not load totals")
    
    st.write("---")
    st.write("### Budget Progress")
    
    budget_response = requests.get(f"{API_URL}/budgets/user/{user_id}/list")
    if budget_response.status_code == 200:
        budgets = budget_response.json()
        if budgets:
            for budget in budgets:
                limit_amount = budget.get('limitAmount')
                if limit_amount and float(limit_amount) > 0:
                    spent = float(budget.get('spent', 0))
                    limit = float(limit_amount)
                    progress = min(spent / limit, 1.0)
                    
                    if budget.get('budgetType') == 'total':
                        type_icon = "📊 "
                    elif budget.get('budgetType') == 'category':
                        type_icon = "📁 "
                    else:
                        type_icon = "🎯 "
                    
                    st.write(f"**{type_icon}{budget.get('categoryName') or budget.get('name', 'Budget')}**")
                    st.progress(progress)
                    st.caption(f"${spent:,.0f} / ${limit:,.0f}")
        else:
            st.info("No budgets set. Go to Budget Manager to create budgets.")
    
    st.write("---")
    st.write("### Spending by Category")
    
    response = requests.get(f"{API_URL}/budgets/user/{user_id}/categories")
    if response.status_code == 200:
        categories = response.json()
        if categories:
            for cat in categories:
                spent = float(cat.get('spent', 0))
                st.write(f"**{cat.get('category', 'Unknown')}**: ${spent:,.0f}")
        else:
            st.info("No spending data")
    else:
        st.error("Could not load categories")

# Budget Manager Tab
elif current_tab == 1:
    st.write("### Budget Manager")
    st.write("Set your total budget, category limits, and custom budgets")
    
    budget_response = requests.get(f"{API_URL}/budgets/user/{user_id}/list")
    budgets = []
    if budget_response.status_code == 200:
        budgets = budget_response.json()
    
    # Total Budget Section
    st.write("#### 📊 Total Budget")
    st.caption("Set an overall spending limit")
    
    total_budget = next((b for b in budgets if b.get('budgetType') == 'total'), None)
    
    if st.session_state.get('edit_total_budget') is not None or (st.session_state.get('edit_total_budget') is None and total_budget is None and st.session_state.get('creating_total')):
        existing = st.session_state.get('edit_total_budget')
        new_limit = st.number_input("Total Budget Limit ($)", 
                                   min_value=0.0, 
                                   step=100.0,
                                   value=st.session_state.get('edit_total_limit', 0.0),
                                   key="total_limit_input")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Save", key="save_total",
                     on_click=save_total_budget,
                     args=(existing, new_limit, user_id))
        with col2:
            st.button("Cancel", key="cancel_total",
                     on_click=cancel_total_edit)
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            if total_budget:
                st.write(f"**Total Budget**: ${float(total_budget.get('limitAmount', 0)):,.0f}")
            else:
                st.write("No total budget set")
        with col2:
            st.button("Edit", key="edit_total",
                     on_click=edit_total_budget,
                     args=(total_budget,))
    
    st.write("---")
    
    # Category Budgets Section
    st.write("#### 📁 Category Budgets")
    st.caption("Set spending limits for each category")
    
    cat_budgets = {b.get('categoryID'): b for b in budgets if b.get('budgetType') == 'category'}
    
    if st.session_state.get('edit_category_id'):
        cat_id = st.session_state['edit_category_id']
        cat_name = st.session_state['edit_category_name']
        existing = st.session_state.get('edit_category_budget')
        
        new_limit = st.number_input(f"Budget for {cat_name} ($)",
                                   min_value=0.0, step=100.0,
                                   value=st.session_state.get('edit_category_limit', 0.0),
                                   key="cat_limit_input")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Save", key="save_cat",
                     on_click=save_category_budget,
                     args=(existing, cat_id, cat_name, new_limit, user_id))
        with col2:
            st.button("Cancel", key="cancel_cat",
                     on_click=cancel_category_edit)
    
    for cat_name, cat_id in EXPENSE_CATEGORIES.items():
        existing = cat_budgets.get(cat_id)
        col1, col2 = st.columns([3, 1])
        with col1:
            if existing and existing.get('limitAmount'):
                st.write(f"**{cat_name}**: ${float(existing.get('limitAmount', 0)):,.0f}")
            else:
                st.write(f"**{cat_name}**: Not set")
        with col2:
            if not st.session_state.get('edit_category_id'):
                st.button("Edit", key=f"edit_cat_{cat_id}",
                         on_click=edit_category_budget,
                         args=(cat_id, cat_name, existing))
    
    st.write("---")
    
    # Custom Budgets Section
    st.write("#### 🎯 Custom Budgets")
    st.caption("Create custom budgets for specific goals")
    
    custom_budgets = [b for b in budgets if b.get('budgetType') == 'custom']
    
    if st.button("Add Custom Budget", key="add_custom"):
        st.session_state['show_custom_form'] = True
    
    if st.session_state.get('show_custom_form', False):
        with st.form("custom_budget_form"):
            name = st.text_input("Budget Name")
            limit = st.number_input("Limit ($)", min_value=0.01, step=100.0)
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Create Budget")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                if name:
                    data = {
                        "name": name,
                        "limitAmount": limit,
                        "budgetType": "custom",
                        "userID": user_id,
                        "categoryID": None
                    }
                    post_response = requests.post(f"{API_URL}/budgets/", json=data)
                    if post_response.status_code == 201:
                        st.success("Budget created!")
                        st.session_state['show_custom_form'] = False
                        st.rerun()
                    else:
                        st.error("Failed to create budget")
                else:
                    st.warning("Please enter a budget name")
            if cancelled:
                st.session_state['show_custom_form'] = False
                st.rerun()
    
    if custom_budgets:
        for budget in custom_budgets:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{budget.get('name', 'Budget')}**: ${float(budget.get('limitAmount', 0)):,.0f}")
            with col2:
                st.button("🗑️", key=f"del_budget_{budget.get('budgetID')}",
                         on_click=delete_budget,
                         args=(budget.get('budgetID'),))
    else:
        st.info("No custom budgets yet")

# Income Tab
elif current_tab == 2:
    col_header, col_export = st.columns([3, 1])
    with col_header:
        st.write("### Income Tracking")
    with col_export:
        response = requests.get(f"{API_URL}/transactions/user/{user_id}/income")
        if response.status_code == 200:
            income_txns_export = response.json()
            if income_txns_export:
                csv_data = convert_to_csv(income_txns_export)
                st.download_button(
                    label="📥 Export",
                    data=csv_data,
                    file_name=f"income_{first_name}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    search_income = st.text_input("🔍 Search income", placeholder="Search by description, source, amount...", key="search_income")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Add Income", type='primary', key='add_income', use_container_width=True):
            st.session_state['show_income_form'] = True
    
    if st.session_state.get('show_income_form', False):
        with st.form("income_form"):
            st.write("#### Add New Income")
            description = st.text_input("Description")
            amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
            source = st.selectbox("Source", ["Salary", "Freelance", "Investment", "Gift", "Other"])
            date = st.date_input("Date")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Add Income")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                acc_response = requests.get(f"{API_URL}/users/{user_id}/accounts")
                if acc_response.status_code == 200:
                    accounts = acc_response.json()
                    if accounts:
                        data = {
                            "amount": amount,
                            "date": str(date),
                            "description": description,
                            "source": source,
                            "accountID": accounts[0]['acctID'],
                            "categoryID": INCOME_CATEGORY_ID
                        }
                        post_response = requests.post(f"{API_URL}/transactions/", json=data)
                        if post_response.status_code == 201:
                            st.success("Income added!")
                            st.session_state['show_income_form'] = False
                            st.rerun()
                        else:
                            st.error("Failed to add income")
            if cancelled:
                st.session_state['show_income_form'] = False
                st.rerun()
    
    response = requests.get(f"{API_URL}/transactions/user/{user_id}/income")
    if response.status_code == 200:
        income_txns = response.json()
        
        filtered_income = filter_transactions(income_txns, search_income)
        
        total_income = sum(float(t.get('amount', 0)) for t in filtered_income)
        st.metric("Total Income", f"${total_income:,.0f}")
        
        if not search_income:
            st.write("#### Income by Source")
            source_response = requests.get(f"{API_URL}/transactions/user/{user_id}/income/by-source")
            if source_response.status_code == 200:
                sources = source_response.json()
                for src in sources:
                    st.write(f"**{src.get('source', 'Unknown')}**: ${float(src.get('total', 0)):,.0f}")
        
        st.write("#### Recent Income" if not search_income else f"#### Search Results ({len(filtered_income)})")
        for txn in filtered_income[:15]:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{txn.get('description', 'No description')}**")
                st.caption(f"{txn.get('source') or 'Unknown'} • {format_date(txn.get('date'))}")
            with col2:
                st.write(f":green[+${float(txn.get('amount', 0)):,.0f}]")
            with col3:
                st.button("🗑️", key=f"del_income_{txn.get('transactionID')}",
                         help="Delete transaction",
                         on_click=delete_transaction,
                         args=(txn.get('transactionID'),))
    else:
        st.error("Could not load income data")

# Expenditures Tab
elif current_tab == 3:
    col_header, col_export = st.columns([3, 1])
    with col_header:
        st.write("### Expenditure Tracking")
    with col_export:
        response = requests.get(f"{API_URL}/transactions/user/{user_id}/expenses")
        if response.status_code == 200:
            expense_txns_export = response.json()
            if expense_txns_export:
                csv_data = convert_to_csv(expense_txns_export)
                st.download_button(
                    label="📥 Export",
                    data=csv_data,
                    file_name=f"expenses_{first_name}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    search_expense = st.text_input("🔍 Search expenses", placeholder="Search by description, category, amount...", key="search_expense")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Add Expense", type='primary', key='add_expense', use_container_width=True):
            st.session_state['show_expense_form'] = True
    
    if st.session_state.get('show_expense_form', False):
        with st.form("expense_form"):
            st.write("#### Add New Expense")
            description = st.text_input("Description")
            amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
            category = st.selectbox("Category", list(EXPENSE_CATEGORIES.keys()))
            method = st.selectbox("Payment Method", ["Debit Card", "Credit Card", "Cash", "Auto-pay", "Transfer"])
            date = st.date_input("Date")
            
            budget_id = None
            budget_response = requests.get(f"{API_URL}/budgets/user/{user_id}/list")
            if budget_response.status_code == 200:
                budgets_list = budget_response.json()
                if budgets_list:
                    budget_options = {"None": None}
                    budget_options.update({b.get('name', 'Budget'): b.get('budgetID') for b in budgets_list})
                    selected_budget = st.selectbox("Add to Budget (optional)", list(budget_options.keys()))
                    budget_id = budget_options[selected_budget]
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Add Expense")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                acc_response = requests.get(f"{API_URL}/users/{user_id}/accounts")
                if acc_response.status_code == 200:
                    accounts = acc_response.json()
                    if accounts:
                        data = {
                            "amount": -amount,
                            "date": str(date),
                            "description": description,
                            "method": method,
                            "accountID": accounts[0]['acctID'],
                            "categoryID": EXPENSE_CATEGORIES.get(category, 5),
                            "budgetID": budget_id
                        }
                        post_response = requests.post(f"{API_URL}/transactions/", json=data)
                        if post_response.status_code == 201:
                            st.success("Expense added!")
                            st.session_state['show_expense_form'] = False
                            st.rerun()
                        else:
                            st.error("Failed to add expense")
            if cancelled:
                st.session_state['show_expense_form'] = False
                st.rerun()
    
    response = requests.get(f"{API_URL}/transactions/user/{user_id}/expenses")
    if response.status_code == 200:
        expense_txns = response.json()
        
        filtered_expenses = filter_transactions(expense_txns, search_expense)
        
        total_expenses = sum(abs(float(t.get('amount', 0))) for t in filtered_expenses)
        st.metric("Total Expenses", f"${total_expenses:,.0f}")
        
        if not search_expense:
            st.write("#### Expenses by Category")
            cat_response = requests.get(f"{API_URL}/transactions/user/{user_id}/expenses/by-category")
            if cat_response.status_code == 200:
                categories = cat_response.json()
                for cat in categories[:5]:
                    st.write(f"**{cat.get('category', 'Unknown')}**: ${float(cat.get('total', 0)):,.0f}")
        
        st.write("#### Recent Expenses" if not search_expense else f"#### Search Results ({len(filtered_expenses)})")
        for txn in filtered_expenses[:15]:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{txn.get('description', 'No description')}**")
                budget_label = f" • 🎯 {txn.get('budgetName')}" if txn.get('budgetName') else ""
                st.caption(f"{txn.get('categoryName') or 'Uncategorized'} • {format_date(txn.get('date'))}{budget_label}")
            with col2:
                st.write(f":red[-${abs(float(txn.get('amount', 0))):,.0f}]")
            with col3:
                st.button("🗑️", key=f"del_expense_{txn.get('transactionID')}",
                         help="Delete transaction",
                         on_click=delete_transaction,
                         args=(txn.get('transactionID'),))
    else:
        st.error("Could not load expense data")

# All Transactions Tab
elif current_tab == 4:
    col_header, col_export = st.columns([3, 1])
    with col_header:
        st.write("### All Transactions")
    with col_export:
        response = requests.get(f"{API_URL}/transactions/user/{user_id}")
        if response.status_code == 200:
            all_txns_export = response.json()
            if all_txns_export:
                csv_data = convert_to_csv(all_txns_export)
                st.download_button(
                    label="📥 Export All",
                    data=csv_data,
                    file_name=f"all_transactions_{first_name}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    search_all = st.text_input("🔍 Search transactions", placeholder="Search by description, category, source, amount...", key="search_all")
    
    response = requests.get(f"{API_URL}/transactions/user/{user_id}")
    if response.status_code == 200:
        all_txns = response.json()
        
        filtered_all = filter_transactions(all_txns, search_all)
        
        income_total = sum(float(t.get('amount', 0)) for t in filtered_all if float(t.get('amount', 0)) > 0)
        expense_total = sum(abs(float(t.get('amount', 0))) for t in filtered_all if float(t.get('amount', 0)) < 0)
        net_total = income_total - expense_total
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Income", f"${income_total:,.0f}")
        with col2:
            st.metric("Expenses", f"${expense_total:,.0f}")
        with col3:
            st.metric("Net", f"${net_total:,.0f}")
        
        st.write("#### Transactions" if not search_all else f"#### Search Results ({len(filtered_all)})")
        for txn in filtered_all[:25]:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{txn.get('description', 'No description')}**")
                category_or_source = txn.get('categoryName') or txn.get('source') or 'Uncategorized'
                budget_label = f" • 🎯 {txn.get('budgetName')}" if txn.get('budgetName') else ""
                st.caption(f"{category_or_source} • {format_date(txn.get('date'))}{budget_label}")
            with col2:
                amt = float(txn.get('amount', 0))
                if amt > 0:
                    st.write(f":green[+${amt:,.0f}]")
                else:
                    st.write(f":red[-${abs(amt):,.0f}]")
            with col3:
                st.button("🗑️", key=f"del_all_{txn.get('transactionID')}",
                         help="Delete transaction",
                         on_click=delete_transaction,
                         args=(txn.get('transactionID'),))
    else:
        st.error("Could not load transactions")