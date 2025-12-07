import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
Appli-Tracker will be a centralized dashboard designed to organize the chaos of the job search/coop search. Instead of juggling NUWorks, Linkedin, Handshake, random spreadsheets, and reddit threads, users will be able to get one place where they can track every application, interview stage, contact, and document they’ve sent out. By pulling everything into a single structured system, the app will help job seekers stay on top of where they’ve applied, what resume they submitted, who they talked to, and where they are in the process. It also turns the data into more useful statistics, like application-to-response rates, which types of roles they’re getting more interviews in, and what platforms are worth searching for jobs on. 

The app supports more than just applicants, career coaches can view all of their students' activity in one dashboard and understand who needs help. Hiring coordinators can monitor job postings across platforms and see which ones bring in the best candidates. System administrators also have tools to manage performance, backups, and updates, without having to dig too deep. Three key features a user can look forward to include, sortable application lists, integrated resume storage, and analytics around jobs. The goal overall is simple: make the job search easier for the people applying, smoother for the people supporting them, and more efficient for the people posting roles. 

    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
