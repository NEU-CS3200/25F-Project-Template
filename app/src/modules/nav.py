import streamlit as st


# ------------------------ Navigation Functions ------------------------

def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


# System Admin
def AdminHomeNav():
    st.sidebar.page_link("pages/00_Admin_Home.py", label="Admin Home", icon="🏠")


def ManageUsersNav():
    st.sidebar.page_link("pages/01_Manage_Users.py", label="Manage Users", icon="👥")


def VerificationsNav():
    st.sidebar.page_link("pages/02_Verifications.py", label="Verifications", icon="✅")


def ReportsNav():
    st.sidebar.page_link("pages/03_Reports.py", label="Platform Reports", icon="📈")


# Player
def PlayerHomeNav():
    st.sidebar.page_link("pages/10_Player_Home.py", label="Player Home", icon="🏀")


def PlayerStatsNav():
    st.sidebar.page_link("pages/11_Player_Stats.py", label="My Statistics", icon="📊")


def UploadVideosNav():
    st.sidebar.page_link("pages/12_Upload_Videos.py", label="Upload Highlights", icon="🎥")


def ViewFeedbackNav():
    st.sidebar.page_link("pages/13_View_Feedback.py", label="Scout Feedback", icon="💬")


# Data Analyst
def AnalystHomeNav():
    st.sidebar.page_link("pages/20_Analyst_Home.py", label="Analyst Home", icon="📊")


def AnalyticsDashboardNav():
    st.sidebar.page_link("pages/21_Analytics_Dashboard.py", label="Performance Analytics", icon="📈")


def CustomMetricsNav():
    st.sidebar.page_link("pages/22_Custom_Metrics.py", label="Custom Metrics", icon="🔧")


def ExportDataNav():
    st.sidebar.page_link("pages/23_Export_Data.py", label="Export Data", icon="📥")


# Game Scout
def ScoutHomeNav():
    st.sidebar.page_link("pages/30_Scout_Home.py", label="Scout Home", icon="🔍")


def SearchPlayersNav():
    st.sidebar.page_link("pages/31_Search_Players.py", label="Search Players", icon="🔍")


def LiveScoutNav():
    st.sidebar.page_link("pages/32_Live_Scout.py", label="Live Game Scout", icon="📹")


def ScoutScheduleNav():
    st.sidebar.page_link("pages/33_Scout_Schedule.py", label="Scouting Schedule", icon="📅")


# ------------------------ Main Sidebar Function ------------------------

def SideBarLinks(show_home=False):
    # Apply custom styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600&display=swap');

        [data-testid="stSidebar"] {
            background-color: #000000;
        }

        .main, .stApp {
            background-color: #1A1A1A;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Bebas Neue', sans-serif;
            letter-spacing: 2px;
            color: #FFFFFF;
        }

        body, p, div, span, label {
            font-family: 'Inter', sans-serif;
            color: #FFFFFF;
        }

        .stButton > button {
            font-family: 'Bebas Neue', sans-serif;
            letter-spacing: 1.5px;
            background-color: #FF6B35;
            color: white;
            border: none;
        }

        .stButton > button:hover {
            background-color: #FF8555;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        button[kind="header"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display logo
    st.sidebar.image("assets/logo.png", width=150)

    # Check authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    # Show home link if requested
    if show_home:
        HomeNav()

    # Show role-specific navigation
    if st.session_state.get("authenticated", False):

        role = st.session_state.get("role", "")

        if role == "system_admin":
            AdminHomeNav()
            ManageUsersNav()
            VerificationsNav()
            ReportsNav()

        elif role == "player":
            PlayerHomeNav()
            PlayerStatsNav()
            UploadVideosNav()
            ViewFeedbackNav()

        elif role == "data_analyst":
            AnalystHomeNav()
            AnalyticsDashboardNav()
            CustomMetricsNav()
            ExportDataNav()

        elif role == "game_scout":
            ScoutHomeNav()
            SearchPlayersNav()
            LiveScoutNav()
            ScoutScheduleNav()

    # Always show About
    AboutPageNav()

    # Show logout button
    if st.session_state.get("authenticated", False):
        if st.sidebar.button("Logout"):
            st.session_state.role = None
            st.session_state.authenticated = False
            st.switch_page("Home.py")