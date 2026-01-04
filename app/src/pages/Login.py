##################################################
# CourtVision - Styled Login Page
##################################################

import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Page config
st.set_page_config(layout='wide')

# Custom CSS for login page
st.markdown("""
<style>
    .login-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 2px solid #FF6B35;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(255, 107, 53, 0.3);
        margin: 20px 0;
    }
    .welcome-text {
        font-size: 32px;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B35 0%, #FF8C42 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        animation: fadeIn 1s ease-in;
    }
    .role-badge {
        display: inline-block;
        background: rgba(255, 107, 53, 0.2);
        border: 1px solid #FF6B35;
        color: #FF6B35;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 14px;
        margin: 10px 0 15px 0;
        font-weight: 600;
    }
    .basketball-icon {
        font-size: 50px;
        animation: bounce 2s infinite;
        margin-bottom: 10px;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    .stButton > button {
        background: linear-gradient(90deg, #FF6B35 0%, #FF8C42 100%);
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 15px 50px;
        border-radius: 30px;
        border: none;
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Show sidebar
SideBarLinks()

# Check if role was selected from home page
if 'role' not in st.session_state or 'selected_user' not in st.session_state:
    st.error('⚠️ Please select a role from the home page first.')
    if st.button('← Back to Home'):
        st.switch_page('Home.py')
    st.stop()

# Get user info from session state
selected_user = st.session_state['selected_user']
role = st.session_state['role']

# Role display mapping
role_display = {
    'system_admin': '🛡️ System Administrator',
    'player': '🏀 Basketball Player',
    'data_analyst': '📊 Data Analyst Scout',
    'game_scout': '🔍 Game Scout'
}

# Center the login container
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(f"""
    <div class="login-container">
        <div class="basketball-icon">🏀</div>
        <div class="welcome-text">Welcome, {selected_user}!</div>
        <div class="role-badge">{role_display.get(role, role)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Login button
    if st.button('🔐 Log In', type='primary', use_container_width=True):
        # Set authenticated flag
        st.session_state['authenticated'] = True

        logger.info(f"User {selected_user} authenticated as {role}")

        # Redirect based on role
        if role == 'system_admin':
            st.switch_page('pages/00_Admin_Home.py')
        elif role == 'player':
            st.switch_page('pages/10_Player_Home.py')
        elif role == 'data_analyst':
            st.switch_page('pages/20_Analyst_Home.py')
        elif role == 'game_scout':
            st.switch_page('pages/30_Scout_Home.py')

    st.write("")

    # Back button
    if st.button('← Back to Home', use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['role'] = None
        st.switch_page('Home.py')
