# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st



#### ------------------------ General ------------------------
"""Home home page for all. Where you can pick each persona sidebar"""
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of Customer ------------------------
def CustomerHomeNav():
    st.sidebar.page_link(
        "pages/00_Customer_Home.py", label="Customer Home", icon="🏠"
    )


def MealPreferencesNav():
    st.sidebar.page_link(
        "pages/01_Meal_Preferences.py", label="Meal Preferences", icon="🥗"
    )


def MealPlanNav():
    st.sidebar.page_link("pages/02_Meal_Plan.py", label="Meal Plan", icon="🗓️️")

def CustomerChatNav():
    st.sidebar.page_link("pages/03_Chat_Page.py", label="Chat Page", icon="💬️")


## ------------------------ Examples for Role of Farmer ------------------------

def FarmerHomeNav():
    st.sidebar.page_link(
      "pages/10_Farmer_Home.py", label="Your Home", icon="🏠"
    )
def ProduceEditNav():
    st.sidebar.page_link(
        "pages/11_Produce_Edit.py", label="Produce Editor", icon="🧺")

def IngredientDirectoryNav():
    st.sidebar.page_link("pages/14_Ingredient_Directory.py", label="Ingredient Directory", icon="📁")


def IngredientPredictorNav():
    st.sidebar.page_link("pages/12_Ingredient_Predict.py", label="Ingredient Predictor", icon="📊")


## ------------------------ Examples for Role of Driver ------------------------

def DriverHomeNav():
    st.sidebar.page_link(
      "pages/22_Driver_Home.py", label="Your Home", icon="🏠"
    )
def AvailabilityCalendarNav():
    st.sidebar.page_link(
        "pages/23_Availability_Calendar.py", label="Availability Calendar", icon="🗓️")

def RoutePlannerNav():
    st.sidebar.page_link("pages/24_Route_Planner.py", label="Route Planner", icon="🧭")

def DriverChatNav():
    st.sidebar.page_link(
        "pages/29_Driver_Chat.py", label="Driver Chat", icon="💬️"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/25_Admin_Home.py", label="System Admin", icon="🏠")
def RecipeCreatorNav():
    st.sidebar.page_link(
        "pages/26_Recipe_Creator.py", label="Recipe Creator", icon="📖"
    )
def CustomerAccountsNav():
    st.sidebar.page_link(
        "pages/27_Customer_Accounts.py", label="Customer Accounts", icon="👥"
    )
def CustomerChatsNav():
    st.sidebar.page_link(
        "pages/28_Admin_Chat.py", label="Chat to Customers + Drivers", icon="💬️"
    )

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=300

                     
                     )

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "customer":
            CustomerHomeNav()
            MealPreferencesNav()
            MealPlanNav()
            CustomerChatNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "farmer":
            FarmerHomeNav()
            ProduceEditNav()
            IngredientDirectoryNav()
            IngredientPredictorNav()

        # If the user role is Delivery Driver, show the Api Testing page
        if st.session_state["role"] == "driver":
            DriverHomeNav()
            AvailabilityCalendarNav()
            RoutePlannerNav()
            DriverChatNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
            RecipeCreatorNav()
            CustomerAccountsNav()
            CustomerChatsNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]   
            st.switch_page("Home.py")