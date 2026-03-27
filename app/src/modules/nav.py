# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st
import os
import streamlit as st

st.sidebar.image("assets/fitflowlogo.png", width=150)

############################
#      GENERAL NAV
############################
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/About.py", label="About", icon="🧠")


############################
#   SYSTEM ADMIN NAVIGATION
############################
def SysAdminHomeNav():
    st.sidebar.page_link("pages/00_Sys_Admin_home.py", label="Admin Home", icon="🖥️")

def SysAdminLogsNav():
    st.sidebar.page_link("pages/01_system_logs.py", label="System Logs", icon="📜")

def SysAdminBackupNav():
    st.sidebar.page_link("pages/02_backup_logs.py", label="Backup Logs", icon="💾")

def SysAdminCreateUserNav():
    st.sidebar.page_link("pages/03_create_user.py", label="Create User", icon="➕")

def SysAdminCreateTrainerNav():
    st.sidebar.page_link("pages/04_create_trainer.py", label="Create Trainer Profile", icon="🏋️")

def SysAdminCreateClientNav():
    st.sidebar.page_link("pages/05_create_client.py", label="Create Client Profile", icon="👤")

def SysAdminUpdateExerciseNav():
    st.sidebar.page_link("pages/06_update_exercise.py", label="Update Exercise", icon="✏️")

def SysAdminDeleteExerciseNav():
    st.sidebar.page_link("pages/07_delete_exercise.py", label="Delete Exercise", icon="🗑️")

def SysAdminManagePermissionsNav():
    st.sidebar.page_link("pages/08_manage_permissions.py", label="Manage Permissions", icon="🔐")


############################
#     HEALTH ANALYST NAV
############################
def HealthAnalystHomeNav():
    st.sidebar.page_link("pages/09_Health_Analyst_home.py", label="Health Analyst Home", icon="🧬")

def HealthAvgWorkoutDurationNav():
    st.sidebar.page_link("pages/10_avg_workout_duration.py", label="Avg Workout Duration", icon="⏱️")

def HealthClientInfoNav():
    st.sidebar.page_link("pages/11_client_info.py", label="Client Info", icon="📋")

def HealthRecentMetricsNav():
    st.sidebar.page_link("pages/12_recent_health_metrics.py", label="Recent Health Metrics", icon="📊")

def HealthProgressionNav():
    st.sidebar.page_link("pages/13_health_progression.py", label="Health Progression", icon="📈")

def HealthProgramCompletionNav():
    st.sidebar.page_link("pages/14_program_completion.py", label="Program Completion", icon="🎯")

def HealthWorkoutFrequencyNav():
    st.sidebar.page_link("pages/15_workout_frequency.py", label="Workout Frequency", icon="🔁")


############################
#        TRAINER NAV
############################
def TrainerHomeNav():
    st.sidebar.page_link("pages/16_Trainer_home.py", label="Trainer Home")
def TrainerExc():
    st.sidebar.page_link("pages/17_trainer_workout_specific_exercise.py", label="Create Exercises")
def TrainerWktTemp():
    st.sidebar.page_link("pages/18_trainer_workout_templates.py", label="Workout Templates")
def TrainerClientProg():
    st.sidebar.page_link("pages/19_trainer_client_programs.py", label="Client Programs")
def TrainerClientLog():
    st.sidebar.page_link("pages/20_trainer_client_logs.py", label="Client Logs & Feedback")


############################
#        CLIENT NAV
############################
def ClientHomeNav():
    st.sidebar.page_link("pages/21_Client_home.py", label="Client Home", icon="🙋")

def ClientDashboardNav():
    st.sidebar.page_link("pages/22_client_dashboard.py", label="Dashboard", icon="📊")

def ClientLogWorkoutNav():
    st.sidebar.page_link("pages/23_client_log_workout.py", label="Log Workout", icon="✍️")

def ClientMyProgramNav():
    st.sidebar.page_link("pages/24_client_my_program.py", label="My Program", icon="🎯")


############################################
#   MAIN SIDEBAR ROLE-BASED NAV CONTROLLER
############################################
def SideBarLinks(show_home=False):
    # Add Logo
    st.sidebar.image("assets/fitflowlogo.png", width=150)

    # Ensure authentication state exists
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    # Show Home if requested
    if show_home:
        HomeNav()

    # If logged in → show role-based nav
    if st.session_state.get("authenticated"):

        role = st.session_state.get("role")

        # ---------------- SYSTEM ADMIN ----------------
        if role == "system_admin":
            SysAdminHomeNav()
            SysAdminLogsNav()
            SysAdminBackupNav()
            SysAdminCreateUserNav()
            SysAdminCreateTrainerNav()
            SysAdminCreateClientNav()
            SysAdminUpdateExerciseNav()
            SysAdminDeleteExerciseNav()
            SysAdminManagePermissionsNav()

        # ---------------- HEALTH ANALYST ----------------
        elif role == "health_analyst":
            HealthAnalystHomeNav()
            HealthAvgWorkoutDurationNav()
            HealthClientInfoNav()
            HealthRecentMetricsNav()
            HealthProgressionNav()
            HealthProgramCompletionNav()
            HealthWorkoutFrequencyNav()

        # ---------------- TRAINER ----------------
        elif role == "trainer":
            TrainerHomeNav()
            TrainerExc()
            TrainerWktTemp()
            TrainerClientProg()
            TrainerClientLog()

        # ---------------- CLIENT ----------------
        elif role == "client":
            ClientHomeNav()
            ClientDashboardNav()
            ClientLogWorkoutNav()
            ClientMyProgramNav()

    # Always show About page
    AboutPageNav()

    # Logout button
    if st.session_state.get("authenticated"):
        if st.sidebar.button("Logout"):
            for k in ["role", "authenticated", "first_name"]:
                st.session_state.pop(k, None)
            st.switch_page("Home.py")
