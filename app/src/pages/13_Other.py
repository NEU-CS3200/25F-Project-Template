import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from datetime import date
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
def delete_subscription(sub_id):
    requests.delete(f"{API_URL}/subscriptions/{sub_id}")

def pay_subscription(sub_id, sub_name, sub_amount, account_id):
    # Get Subscriptions category ID
    cat_response = requests.get(f"{API_URL}/categories/expense")
    category_id = None
    if cat_response.status_code == 200:
        cats = cat_response.json()
        for c in cats:
            if c['name'].lower() == 'subscriptions':
                category_id = c['categoryID']
                break
    
    data = {
        "amount": -float(sub_amount),
        "date": str(date.today()),
        "description": f"Subscription: {sub_name}",
        "method": "Auto-pay",
        "accountID": account_id,
        "categoryID": category_id,
        "budgetID": None
    }
    response = requests.post(f"{API_URL}/transactions/", json=data)
    if response.status_code == 201:
        st.session_state['paid_sub_id'] = sub_id

def delete_loan(loan_id):
    requests.delete(f"{API_URL}/loans/{loan_id}")

def start_pay_loan(loan_id, loan_name, amount_paid, total_amount):
    st.session_state['paying_loan'] = loan_id
    st.session_state['paying_loan_name'] = loan_name
    st.session_state['paying_loan_paid'] = amount_paid
    st.session_state['paying_loan_total'] = total_amount

def cancel_pay_loan():
    st.session_state['paying_loan'] = None

def delete_investment(inv_id):
    requests.delete(f"{API_URL}/investments/{inv_id}")

def delete_bill(bill_id):
    response = requests.get(f"{API_URL}/bills/{bill_id}")
    if response.status_code == 200:
        bill = response.json()
        if bill.get('isPaid'):
            txn_response = requests.get(f"{API_URL}/transactions/user/{user_id}")
            if txn_response.status_code == 200:
                transactions = txn_response.json()
                for txn in transactions:
                    if f"(BillID:{bill_id})" in txn.get('description', ''):
                        requests.delete(f"{API_URL}/transactions/{txn['transactionID']}")
                        break
    requests.delete(f"{API_URL}/bills/{bill_id}")

def pay_bill(bill_id, bill_name, bill_amount):
    requests.put(f"{API_URL}/bills/{bill_id}/pay")
    acc_response = requests.get(f"{API_URL}/users/{user_id}/accounts")
    if acc_response.status_code == 200:
        accounts = acc_response.json()
        if accounts:
            # Get Utilities category ID (or Bills if exists)
            cat_response = requests.get(f"{API_URL}/categories/expense")
            category_id = None
            if cat_response.status_code == 200:
                cats = cat_response.json()
                for c in cats:
                    if c['name'].lower() in ['utilities', 'bills']:
                        category_id = c['categoryID']
                        break
            
            data = {
                "amount": -float(bill_amount),
                "date": str(date.today()),
                "description": f"Bill Payment: {bill_name}",
                "method": "Auto-pay",
                "accountID": accounts[0]['acctID'],
                "categoryID": category_id,
                "budgetID": None
            }
            requests.post(f"{API_URL}/transactions/", json=data)

def unpay_bill(bill_id):
    requests.put(f"{API_URL}/bills/{bill_id}/unpay")
    txn_response = requests.get(f"{API_URL}/transactions/user/{user_id}")
    if txn_response.status_code == 200:
        transactions = txn_response.json()
        for txn in transactions:
            if f"(BillID:{bill_id})" in txn.get('description', ''):
                requests.delete(f"{API_URL}/transactions/{txn['transactionID']}")
                break

st.title("Other Financial Data")
st.write("View and manage your debt, investments, subscriptions, and bills")

st.write("---")

# Tabs
tab_names = ["Debt", "Investments", "Subscriptions", "Bills"]

if 'other_tab' not in st.session_state:
    st.session_state['other_tab'] = 0

current_tab = st.session_state['other_tab']

cols = st.columns(len(tab_names))
for i, (col, name) in enumerate(zip(cols, tab_names)):
    with col:
        if i == current_tab:
            st.button(name, key=f"other_tab_{i}", type="primary", use_container_width=True, disabled=True)
        else:
            if st.button(name, key=f"other_tab_{i}", use_container_width=True):
                st.session_state['other_tab'] = i
                st.rerun()

st.write("---")

# Debt Tab
if current_tab == 0:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("### Debt Overview")
    with col2:
        if st.button("Add Debt", type='primary', key='add_debt'):
            st.session_state['show_debt_form'] = True
    
    # Add debt form
    if st.session_state.get('show_debt_form', False):
        with st.form("debt_form"):
            st.write("#### Add New Debt")
            name = st.text_input("Loan Name")
            purpose = st.text_input("Purpose")
            amount = st.number_input("Total Amount ($)", min_value=0.01, step=100.0)
            amount_paid = st.number_input("Amount Already Paid ($)", min_value=0.0, step=100.0)
            interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
            min_payment = st.number_input("Minimum Payment ($)", min_value=0.0, step=10.0)
            
            acc_response = requests.get(f"{API_URL}/users/{user_id}/accounts")
            account_id = None
            if acc_response.status_code == 200:
                accounts = acc_response.json()
                if accounts:
                    account_options = {f"{a['accType']} - {a['institution']}": a['acctID'] for a in accounts}
                    selected_account = st.selectbox("Account", list(account_options.keys()))
                    account_id = account_options[selected_account]
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Add Debt")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                if name and account_id:
                    data = {
                        "name": name,
                        "purpose": purpose,
                        "amount": amount,
                        "amountPaid": amount_paid,
                        "interestRate": interest_rate,
                        "minPayment": min_payment,
                        "accountID": account_id
                    }
                    post_response = requests.post(f"{API_URL}/loans/", json=data)
                    if post_response.status_code == 201:
                        st.success("Debt added!")
                        st.session_state['show_debt_form'] = False
                        st.rerun()
                    else:
                        st.error("Failed to add debt")
                else:
                    st.warning("Please fill in all required fields")
            if cancelled:
                st.session_state['show_debt_form'] = False
                st.rerun()
    
    # Pay loan form
    if st.session_state.get('paying_loan'):
        loan_id = st.session_state['paying_loan']
        loan_name = st.session_state.get('paying_loan_name', 'Loan')
        amount_paid = st.session_state.get('paying_loan_paid', 0)
        total_amount = st.session_state.get('paying_loan_total', 0)
        remaining = total_amount - amount_paid
        
        with st.form("pay_loan_form"):
            st.write(f"#### 💳 Make Payment on {loan_name}")
            st.caption(f"Remaining balance: ${remaining:,.0f}")
            payment_amount = st.number_input("Payment Amount ($)", min_value=0.01, max_value=float(remaining), step=10.0, value=min(100.0, float(remaining)))
            
            col1, col2 = st.columns(2)
            with col1:
                pay_submitted = st.form_submit_button("Make Payment", type="primary")
            with col2:
                pay_cancelled = st.form_submit_button("Cancel")
            
            if pay_submitted:
                # Update loan amount paid
                response = requests.put(f"{API_URL}/loans/{loan_id}/pay", json={"amount": float(payment_amount)})
                if response.status_code == 200:
                    # Create expense transaction
                    acc_response = requests.get(f"{API_URL}/users/{user_id}/accounts")
                    if acc_response.status_code == 200:
                        accounts = acc_response.json()
                        if accounts:
                            # Get category ID for loan payments
                            cat_response = requests.get(f"{API_URL}/categories/expense")
                            category_id = None
                            if cat_response.status_code == 200:
                                cats = cat_response.json()
                                for c in cats:
                                    if c['name'].lower() in ['utilities', 'bills', 'debt']:
                                        category_id = c['categoryID']
                                        break
                            
                            txn_data = {
                                "amount": -float(payment_amount),
                                "date": str(date.today()),
                                "description": f"Loan Payment: {loan_name}",
                                "method": "Transfer",
                                "accountID": accounts[0]['acctID'],
                                "categoryID": category_id,
                                "budgetID": None
                            }
                            requests.post(f"{API_URL}/transactions/", json=txn_data)
                    
                    st.success(f"Payment of ${payment_amount:,.2f} applied to {loan_name}!")
                    st.session_state['paying_loan'] = None
                    st.rerun()
                else:
                    st.error("Failed to make payment")
            if pay_cancelled:
                st.session_state['paying_loan'] = None
                st.rerun()
        
        st.write("---")
    
    # Display loans
    response = requests.get(f"{API_URL}/loans/user/{user_id}")
    if response.status_code == 200:
        loans = response.json()
        
        if loans:
            total_debt = sum(float(l['amount']) - float(l['amountPaid']) for l in loans)
            st.metric("Total Remaining Debt", f"${total_debt:,.0f}")
            
            st.write("---")
            
            for loan in loans:
                remaining = float(loan['amount']) - float(loan['amountPaid'])
                progress = float(loan['amountPaid']) / float(loan['amount']) if float(loan['amount']) > 0 else 0
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{loan['name']}**")
                    st.caption(f"{loan['purpose'] or 'No purpose specified'}")
                    st.progress(progress)
                    st.caption(f"Paid: ${float(loan['amountPaid']):,.0f} / ${float(loan['amount']):,.0f}")
                    if loan.get('interestRate'):
                        st.caption(f"Interest Rate: {loan['interestRate']}%")
                with col2:
                    st.metric("Remaining", f"${remaining:,.0f}")
                    if loan.get('minPayment'):
                        st.caption(f"Min Payment: ${float(loan['minPayment']):,.0f}")
                with col3:
                    if remaining > 0:
                        st.button("💳 Pay", key=f"pay_loan_{loan['loanID']}",
                                 on_click=start_pay_loan,
                                 args=(loan['loanID'], loan['name'], float(loan['amountPaid']), float(loan['amount'])))
                    st.button("🗑️ Delete", key=f"del_loan_{loan['loanID']}",
                             on_click=delete_loan,
                             args=(loan['loanID'],))
                
                st.write("---")
        else:
            st.info("No debt records found")
    else:
        st.error("Could not load debt data")

# Investments Tab
elif current_tab == 1:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("### Investment Portfolio")
    with col2:
        if st.button("Add Investment", type='primary', key='add_inv'):
            st.session_state['show_inv_form'] = True
    
    if st.session_state.get('show_inv_form', False):
        with st.form("investment_form"):
            st.write("#### Add New Investment")
            name = st.text_input("Investment Name")
            account_type = st.selectbox("Account Type", ["Retirement", "Taxable", "Education", "Other"])
            balance = st.number_input("Current Balance ($)", min_value=0.0, step=100.0)
            return_rate = st.number_input("Return Rate (%)", min_value=-100.0, max_value=100.0, step=0.1)
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Add Investment")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                if name:
                    data = {
                        "name": name,
                        "accountType": account_type,
                        "balance": balance,
                        "returnRate": return_rate,
                        "userID": user_id
                    }
                    post_response = requests.post(f"{API_URL}/investments/", json=data)
                    if post_response.status_code == 201:
                        st.success("Investment added!")
                        st.session_state['show_inv_form'] = False
                        st.rerun()
                    else:
                        st.error("Failed to add investment")
                else:
                    st.warning("Please enter an investment name")
            if cancelled:
                st.session_state['show_inv_form'] = False
                st.rerun()
    
    response = requests.get(f"{API_URL}/investments/user/{user_id}")
    if response.status_code == 200:
        investments = response.json()
        
        if investments:
            total_invested = sum(float(i['balance']) for i in investments)
            st.metric("Total Portfolio Value", f"${total_invested:,.0f}")
            
            st.write("---")
            
            for inv in investments:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{inv['name']}**")
                    st.caption(f"Type: {inv['accountType'] or 'Unknown'}")
                    if inv.get('returnRate'):
                        st.caption(f"Return Rate: {inv['returnRate']}%")
                with col2:
                    st.metric("Balance", f"${float(inv['balance']):,.0f}")
                with col3:
                    st.button("🗑️ Delete", key=f"del_inv_{inv['investmentID']}",
                             on_click=delete_investment,
                             args=(inv['investmentID'],))
                
                st.write("---")
        else:
            st.info("No investment records found")
    else:
        st.error("Could not load investment data")

# Subscriptions Tab
elif current_tab == 2:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("### Subscriptions")
    with col2:
        if st.button("Add Subscription", type='primary', key='add_sub'):
            st.session_state['show_sub_form'] = True
    
    if st.session_state.get('show_sub_form', False):
        with st.form("subscription_form"):
            st.write("#### Add New Subscription")
            name = st.text_input("Subscription Name")
            amount = st.number_input("Amount ($)", min_value=0.01, step=1.0)
            frequency = st.selectbox("Frequency", ["monthly", "yearly", "weekly"])
            start_date = st.date_input("Start Date")
            next_billing = st.date_input("Next Billing Date")
            
            acc_response = requests.get(f"{API_URL}/users/{user_id}/accounts")
            account_id = None
            if acc_response.status_code == 200:
                accounts = acc_response.json()
                if accounts:
                    account_options = {f"{a['accType']} - {a['institution']}": a['acctID'] for a in accounts}
                    selected_account = st.selectbox("Account", list(account_options.keys()))
                    account_id = account_options[selected_account]
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Add Subscription")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                if name and account_id:
                    data = {
                        "name": name,
                        "amount": amount,
                        "frequency": frequency,
                        "startDate": str(start_date),
                        "nextBilling": str(next_billing),
                        "accountID": account_id
                    }
                    post_response = requests.post(f"{API_URL}/subscriptions/", json=data)
                    if post_response.status_code == 201:
                        st.success("Subscription added!")
                        st.session_state['show_sub_form'] = False
                        st.rerun()
                    else:
                        st.error("Failed to add subscription")
                else:
                    st.warning("Please fill in all required fields")
            if cancelled:
                st.session_state['show_sub_form'] = False
                st.rerun()
    
    response = requests.get(f"{API_URL}/subscriptions/user/{user_id}")
    if response.status_code == 200:
        subscriptions = response.json()
        
        if subscriptions:
            total_monthly = sum(
                float(s['amount']) if s['frequency'] == 'monthly' 
                else float(s['amount']) / 12 if s['frequency'] == 'yearly'
                else float(s['amount']) * 4 
                for s in subscriptions
            )
            st.metric("Total Monthly Cost", f"${total_monthly:,.0f}")
            
            st.write("---")
            
            for sub in subscriptions:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{sub['name']}**")
                    st.caption(f"Frequency: {sub['frequency'] or 'Unknown'}")
                    if sub.get('nextBilling'):
                        st.caption(f"Next Billing: {sub['nextBilling'][:10]}")
                with col2:
                    st.metric("Amount", f"${float(sub['amount']):,.0f}")
                with col3:
                    st.button("💳 Pay", key=f"pay_sub_{sub['subID']}",
                             on_click=pay_subscription,
                             args=(sub['subID'], sub['name'], sub['amount'], sub['accountID']))
                    st.button("🗑️ Delete", key=f"del_sub_{sub['subID']}",
                             on_click=delete_subscription,
                             args=(sub['subID'],))
                
                if st.session_state.get('paid_sub_id') == sub['subID']:
                    st.success(f"✅ Paid ${float(sub['amount']):,.2f} for {sub['name']}!")
                    st.session_state['paid_sub_id'] = None
                
                st.write("---")
        else:
            st.info("No subscriptions found")
    else:
        st.error("Could not load subscription data")

# Bills Tab
elif current_tab == 3:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("### Bills")
    with col2:
        if st.button("Add Bill", type='primary', key='add_bill'):
            st.session_state['show_bill_form'] = True
    
    if st.session_state.get('show_bill_form', False):
        with st.form("bill_form"):
            st.write("#### Add New Bill")
            name = st.text_input("Bill Name")
            amount = st.number_input("Amount ($)", min_value=0.01, step=10.0)
            due_date = st.date_input("Due Date")
            is_recurring = st.checkbox("Recurring Bill")
            frequency = st.selectbox("Frequency", ["monthly", "yearly", "weekly", "quarterly"])
            
            acc_response = requests.get(f"{API_URL}/users/{user_id}/accounts")
            account_id = None
            if acc_response.status_code == 200:
                accounts = acc_response.json()
                if accounts:
                    account_options = {f"{a['accType']} - {a['institution']}": a['acctID'] for a in accounts}
                    selected_account = st.selectbox("Account", list(account_options.keys()))
                    account_id = account_options[selected_account]
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Add Bill")
            with col2:
                cancelled = st.form_submit_button("Cancel")
            
            if submitted:
                if name and account_id:
                    data = {
                        "name": name,
                        "amount": amount,
                        "dueDate": str(due_date),
                        "isPaid": False,
                        "isRecurring": is_recurring,
                        "frequency": frequency if is_recurring else None,
                        "accountID": account_id
                    }
                    post_response = requests.post(f"{API_URL}/bills/", json=data)
                    if post_response.status_code == 201:
                        st.success("Bill added!")
                        st.session_state['show_bill_form'] = False
                        st.rerun()
                    else:
                        st.error("Failed to add bill")
                else:
                    st.warning("Please fill in all required fields")
            if cancelled:
                st.session_state['show_bill_form'] = False
                st.rerun()
    
    response = requests.get(f"{API_URL}/bills/user/{user_id}")
    if response.status_code == 200:
        bills = response.json()
        
        if bills:
            unpaid_total = sum(float(b['amount']) for b in bills if not b['isPaid'])
            st.metric("Unpaid Bills", f"${unpaid_total:,.0f}")
            
            st.write("---")
            
            for bill in bills:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    status = "✅ Paid" if bill['isPaid'] else "⏳ Unpaid"
                    st.write(f"**{bill['name']}** - {status}")
                    st.caption(f"Due: {bill['dueDate'][:10]}")
                    if bill.get('isRecurring'):
                        st.caption(f"Recurring: {bill['frequency']}")
                with col2:
                    st.metric("Amount", f"${float(bill['amount']):,.0f}")
                with col3:
                    if bill['isPaid']:
                        st.button("↩️ Unpay", key=f"unpay_{bill['billID']}",
                                 on_click=unpay_bill,
                                 args=(bill['billID'],))
                    else:
                        st.button("💳 Pay", key=f"pay_{bill['billID']}",
                                 on_click=pay_bill,
                                 args=(bill['billID'], bill['name'], bill['amount']))
                    st.button("🗑️ Delete", key=f"del_bill_{bill['billID']}",
                             on_click=delete_bill,
                             args=(bill['billID'],))
                
                st.write("---")
        else:
            st.info("No bills found")
    else:
        st.error("Could not load bills data")