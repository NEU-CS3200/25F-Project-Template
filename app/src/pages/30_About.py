import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    CourtVision is a data-driven scouting platform for amateur basketball—designed for AAU programs and high school leagues. We centralize player profiles, performance metrics, and game data to help organizations identify talent and maximize team success.

Traditional scouting tools are fragmented, expensive, and focus on either stats or video—never both. Many amateur players have no centralized record of their abilities. CourtVision bridges this gap by collecting structured player data, verifying stats, and delivering clear analytics accessible to players, scouts, coaches, and analysts.

Our platform offers player comparisons, trend dashboards, and integrated video-stats views—giving everyone a complete picture of the game.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
