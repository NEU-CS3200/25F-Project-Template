##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks
import requests

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('NEU Connect')
st.write('\n\n')
# st.write('### Overview:')
# st.write('\n')
st.write('#### HI! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

personas = {
        "Student": {
                "role": "student",
                "home_page": "pages/30_Student_Home.py",
                "user_endpoint": "/students",
                "fallback_users": [
                        {"id": "1", "first_name": "Timmy", "last_name": "Anderson"},
                        {"id": "2", "first_name": "Joe", "last_name": "Smith"},
                ]
                
        },
        "Alumni": {
                "role": "alumni",
                "home_page": "pages/40_Alumni_Home.py",
                "user_endpoint": "/alumni",
                "fallback_users": [
                        {"id": "10", "first_name": "Johnny", "last_name": "Cage"},
                        {"id": "11", "first_name": "Karen", "last_name": "Williams"},
                ]
        },
        "System Administrator": {
                "role": "administrator",
                "home_page": "pages/20_Admin_Home.py",
                "user_endpoint": "/admin",
                "fallback_users": [
                        {"id": "20", "first_name": "Dave", "last_name": "Dunkin"},
                ]
        },
        "Data Analyst": {
                "role": "data_analyst",
                "home_page": "pages/50_Data_Analyst_Home.py",
                "user_endpoint": "/data_analyst",
                "fallback_users": [
                        {"id": "30", "first_name": "Carl", "last_name": "Johnson"},
                        {"id": "31", "first_name": "Bob", "last_name": "Brown"},
                ]
        }
}

# base url for flask API
try:
        API_BASE = st.secrets["API_BASE"]
except Exception:
        API_BASE = "http://backend:8000"

def get_users(persona_cfg):
        '''
        gets the users for a persona
        '''
        endpoint = persona_cfg.get("user_endpoint")
        fallback = persona_cfg.get("fallback_users", [])

        if not endpoint:
                return fallback
        try:
                response = requests.get(f"{API_BASE}{endpoint}", timeout=5)
                if response.status_code == 200:
                        data = response.json()
                        return data if isinstance(data, list) and len(data) > 0 else fallback      
                return fallback
        except Exception as e:
                logger.info(f"Using fallback users due to API issue: {e}")
                return fallback

# UI Layout
st.write('Select a user under each role, then click Login to continue.')

for persona_label, cfg in personas.items():
        with st.container(border=True):
                st.subheader(f"--- {persona_label} ---")
                users = get_users(cfg)

                # continue if no users found
                if not users:
                        st.warning("No users available for this role yet.")
                        continue

                # make a label with user's details
                def make_label(user):
                        first_name = user.get('first_name', 'First')
                        last_name = user.get('last_name', 'Last')
                        user_id = user.get('id', '')
                        return f"{first_name} {last_name} (id: {user_id})"

                # make labels for each user
                label_options = {make_label(u): u for u in users}

                selected_label = st.selectbox(
                        f"Select {persona_label} User:",
                        list(label_options.keys()),
                        key=f"select_{persona_label}"
                )

                if st.button(
                        f"Login as {persona_label}", 
                        type = 'primary', 
                        use_container_width=True,
                        key=f"login_{persona_label}"
                ):

                        selected_user = label_options[selected_label]
                        # when user clicks the button, they are now considered authenticated
                        st.session_state['authenticated'] = True
                        # we set the role of the current user
                        st.session_state['role'] = cfg['role']
                        # we add the first name of the user (so it can be displayed on subsequent pages). 
                        st.session_state['first_name'] = selected_user.get("first_name", persona_label)
                        st.session_state['user_id'] = selected_user.get("id")

                        logger.info(f"Logging in as {persona_label} Persona: {selected_label}")
                        # finally, we ask streamlit to switch to another page
                        st.switch_page(cfg['home_page'])





