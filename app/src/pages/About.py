import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    FitFlow is a health and fitness tracking website meant to connect gym members, trainers, and health professionals in one platform.

    Stay tuned for more information and features to come!
    """
)

st.write("## Our Mission")
st.markdown(
    """
    We bridge the gap between fitness professionals and their clients by transforming scattered data into actionable insights. 
    
    FitFlow empowers trainers to make informed, data-driven decisions while giving members the tools to track and celebrate their progress.

    """
)

st.write("## Our Solution")
st.markdown(
    """
    FitFlow provides a centralized platform where:

    - *Members* log workouts, visualize trends, and track their fitness journey
    - *Trainers* design personalized programs, monitor real-time progress, and quickly identify clients who need follow-up
    - *Health* Professionals access comprehensive performance data to support member wellness
    - *Administrators* oversee accounts and maintain platform integrity

    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
