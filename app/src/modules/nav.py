# Navigation functions for Streamlit sidebar

import streamlit as st


# ------------------------ General Navigation ------------------------

def HomeNav():
    st.sidebar.page_link("Home.py", label="Home")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About")


# ------------------------ Admin Navigation ------------------------

def AdminHomeNav():
    st.sidebar.page_link("pages/05_Admin_Home.py", label="Admin Home")


def ReportsManagementNav():
    st.sidebar.page_link("pages/10_Reports_Management.py", label="Reports Management")


def AdminUserToolsNav():
    st.sidebar.page_link("pages/20_Admin_User_Tools.py", label="Admin User Tools")


def ItemCleanupNav():
    st.sidebar.page_link("pages/30_Item_Cleanup.py", label="Item Cleanup")


# ------------------------ Sidebar Link Controller ------------------------

def SideBarLinks(show_home=False):
    """
    Adds sidebar navigation links depending on authentication
    and the user's role stored in session_state.
    """

    # Always show the logo
    st.sidebar.image("assets/fitlogo.png", width=150)

    # If no user authentication flag exists, redirect to home
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    # Optional: show home link
    if show_home:
        HomeNav()

    # Show links based on role
    if st.session_state["authenticated"]:

        if st.session_state["role"] == "admin":
            AdminHomeNav()
            ReportsManagementNav()
            AdminUserToolsNav()
            ItemCleanupNav()

    # Always show About page
    AboutPageNav()

    # Logout
    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
