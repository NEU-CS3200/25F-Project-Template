import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()
from modules.nav import BackToDashboard
BackToDashboard()

st.title("About Don't Be Dumb Budgeting")

st.write("---")

st.write("""
### Our Mission

Don't Be Dumb Budgeting helps you understand and manage your personal finances 
through intelligent categorization and actionable insights. Whether you're a 
college student tracking a stipend, a professional managing investments, or a 
family planning for the future, our app provides the tools you need.
""")

st.write("---")

st.write("### Features")

col1, col2 = st.columns(2)

with col1:
    st.write("""
    **Budget Tracking**
    - Track income and expenses
    - Categorize transactions
    - Set spending limits
    - Monitor progress in real-time
    """)
    
    st.write("""
    **Savings Goals**
    - Create custom savings goals
    - Track progress over time
    - Set monthly contributions
    - Get recommendations
    """)

with col2:
    st.write("""
    **AI Insights**
    - Financial health score
    - Personalized recommendations
    - Spending pattern analysis
    - Optimization opportunities
    """)
    
    st.write("""
    **Multi-User Support**
    - Individual profiles
    - Family account management
    - Club/organization budgets
    - Dependent tracking
    """)

st.write("---")

st.write("### User Personas")

st.write("""
This app is designed for four key user types:

1. **College Students** - Track stipends, part-time income, and manage tight budgets
2. **Working Professionals** - Manage multiple accounts, investments, and long-term goals
3. **Club Treasurers** - Handle organization finances, member dues, and event budgets
4. **Family Managers** - Oversee household spending, dependents, and family goals
""")

st.write("---")

st.write("### Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("""
    **Frontend**
    - Streamlit
    - Python
    """)

with col2:
    st.write("""
    **Backend**
    - Flask REST API
    - Python
    """)

with col3:
    st.write("""
    **Database**
    - MySQL
    - Docker
    """)

st.write("---")

st.write("### Team")

st.write("""
**Fontenote's SQL Wizards**

- Ryan Porto
- Amogh Athimamula
- Adam Ancheta
- Shravan Ganta

CS 3200 - Database Design | Fall 2025 | Northeastern University
""")

st.write("---")

st.caption("Don't Be Dumb Budgeting © 2025")