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
    # Apply custom styling with gradient buttons
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

        /* Glowing effect for main title (h1) */
        h1 {
            text-shadow: 0 0 20px rgba(255, 107, 53, 0.6),
                         0 0 40px rgba(255, 107, 53, 0.4),
                         0 0 60px rgba(255, 107, 53, 0.2);
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from {
                text-shadow: 0 0 20px rgba(255, 107, 53, 0.6),
                             0 0 40px rgba(255, 107, 53, 0.4),
                             0 0 60px rgba(255, 107, 53, 0.2);
            }
            to {
                text-shadow: 0 0 30px rgba(255, 107, 53, 0.8),
                             0 0 50px rgba(255, 107, 53, 0.6),
                             0 0 70px rgba(255, 107, 53, 0.4);
            }
        }

        body, p, div, span, label {
            font-family: 'Inter', sans-serif;
            color: #FFFFFF;
        }

        /* Gradient buttons for all buttons */
        .stButton > button {
            font-family: 'Bebas Neue', sans-serif;
            letter-spacing: 1.5px;
            background: linear-gradient(90deg, #FF6B35 0%, #FF8C42 100%);
            color: white;
            border: none;
            border-radius: 0px;
            box-shadow: 0 4px 10px rgba(255, 107, 53, 0.3);
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #FF8555 0%, #FFA05C 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255, 107, 53, 0.5);
        }

        .stButton > button:active {
            transform: translateY(0px);
            box-shadow: 0 2px 5px rgba(255, 107, 53, 0.3);
        }

        /* Primary button styling (for type='primary') */
        .stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #FF6B35 0%, #FF8C42 100%);
            font-size: 16px;
            font-weight: bold;
            padding: 12px 24px;
            box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4);
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(90deg, #FF8555 0%, #FFA05C 100%);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(255, 107, 53, 0.6);
        }

        /* Sidebar buttons (role switcher) */
        .stSidebar .stButton > button {
            font-size: 13px;
            padding: 8px 12px;
            border-radius: 0px;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        button[kind="header"] {
            display: none;
        }

        /* Make sidebar logo bigger with glow */
        [data-testid="stSidebar"] img {
            width: 100% !important;
            max-width: 280px !important;
            margin: -10px auto 30px auto !important;
            display: block !important;
            filter: drop-shadow(0 0 15px rgba(255, 107, 53, 0.6))
                    drop-shadow(0 0 30px rgba(255, 107, 53, 0.4))
                    drop-shadow(0 0 45px rgba(255, 107, 53, 0.2));
            animation: logoGlow 2s ease-in-out infinite alternate;
        }

        /* Target the image container to push it up */
        [data-testid="stSidebar"] [data-testid="stImage"] {
            margin-top: -20px !important;
        }

        @keyframes logoGlow {
            from {
                filter: drop-shadow(0 0 15px rgba(255, 107, 53, 0.6))
                        drop-shadow(0 0 30px rgba(255, 107, 53, 0.4))
                        drop-shadow(0 0 45px rgba(255, 107, 53, 0.2));
            }
            to {
                filter: drop-shadow(0 0 20px rgba(255, 107, 53, 0.8))
                        drop-shadow(0 0 40px rgba(255, 107, 53, 0.6))
                        drop-shadow(0 0 60px rgba(255, 107, 53, 0.4));
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Display logo (will be sized by CSS)
    st.sidebar.image("assets/logo.png", use_container_width=True)

    # Always show Home link at top
    st.sidebar.page_link("Home.py", label="Landing Page", icon="🏠")

    # Set default session state (no login required)
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False  # Start as not authenticated
        st.session_state.role = None
        st.session_state.user_id = None
        st.session_state.first_name = None

    # Only show navigation if a role has been selected
    if st.session_state.get("authenticated", False) and st.session_state.get("role"):

        role = st.session_state.get("role")

        st.sidebar.markdown("---")

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

        # Always show About when authenticated
        st.sidebar.markdown("---")
        AboutPageNav()

        # Role switcher (only show when authenticated)
        st.sidebar.markdown("---")
        st.sidebar.write("**Switch Role:**")

        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("👤 Player", use_container_width=True):
                st.session_state.role = "player"
                st.session_state.user_id = 101
                st.session_state.first_name = "Sean"
                st.rerun()
            if st.button("📊 Analyst", use_container_width=True):
                st.session_state.role = "data_analyst"
                st.session_state.user_id = 1
                st.session_state.first_name = "John"
                st.rerun()

        with col2:
            if st.button("🔧 Admin", use_container_width=True):
                st.session_state.role = "system_admin"
                st.session_state.user_id = 1
                st.session_state.first_name = "Ryan"
                st.rerun()
            if st.button("🔍 Scout", use_container_width=True):
                st.session_state.role = "game_scout"
                st.session_state.user_id = 1
                st.session_state.first_name = "Sara"
                st.rerun()
    else:
        # On landing page, show About directly under Home (no divider)
        AboutPageNav()
