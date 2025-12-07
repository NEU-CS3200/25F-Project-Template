import streamlit as st
import pandas as pd
import requests
import logging
import time
logger = logging.getLogger(__name__)
from datetime import date

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Appli-Tracker")
SideBarLinks()

if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'James'
if 'student_id' not in st.session_state:
    st.session_state['student_id'] = 1 


@st.dialog("Add New Job Application")
def add_application_dialog():
    st.write(f"Enter details for **{st.session_state['first_name']}**'s new application.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company = st.text_input("Company Name", placeholder="e.g. Netflix")
        position = st.text_input("Position", placeholder="e.g. Data Scientist")
        stage = st.selectbox("Stage", ["Applied", "Interviewing", "Ghosted", "Offer", "Rejected"])
    
    with col2:
        date_applied = st.date_input("Date Applied", value=date.today())
        
        resume_map = {}
        try:
            api_url = f"http://web-api:4000/app_tracker/resumes/{st.session_state['student_id']}"
            response = requests.get(api_url)

            if response.status_code == 200:
                res_data = response.json()
                for r in res_data:
                    r_id = r.get('resumeID')
                    r_label = r.get('label')
                    
                    if r_label in resume_map:
                        r_label = f"{r_label} (ID: {r_id})"
                    
                    if r_id:
                        resume_map[r_label] = r_id
        except Exception as e:
            st.error(f"Error loading resumes: {e}")

        # Display Sorted Dropdown
        selected_resume_id = None
        if resume_map:
            sorted_labels = sorted(list(resume_map.keys()))
            
            selected_label = st.selectbox("Resume Used", sorted_labels)
            selected_resume_id = resume_map[selected_label]
            
        else:
            st.warning("No resumes found.")
        job_board = st.text_input("Job Board", placeholder="e.g. LinkedIn")

    st.write("")
    col_submit, col_cancel = st.columns([1, 1])
    
    with col_submit:
        if st.button("Submit Application", type="primary"):
            if not company or not position:
                st.error("Please fill in Company and Position.")
            elif selected_resume_id is None:
                st.error("Please select a resume.")
            else:
                new_app_data = {
                    "student_id": st.session_state['student_id'],
                    "company": company,
                    "position": position,
                    "stage": stage,
                    "date_applied": str(date_applied),
                    "resume_id": selected_resume_id,
                    "job_board": job_board
                }
                
                try:
                    api_url = f"http://web-api:4000/app_tracker/applications/{st.session_state['student_id']}" 
                    response = requests.post(api_url, json=new_app_data)
                    
                    if response.status_code == 201:
                        st.success(f"Application for {company} added!")
                        time.sleep(1)
                        
                        st.rerun()
                    else:
                        st.error(f"Backend Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")


# Creating header
col_title, col_user = st.columns([4, 1])

with col_title:
    st.title("Appli-Tracker")

with col_user:
    st.write("")
    st.write("")
    st.write(f"**Logged In As:** {st.session_state['first_name']}")
    
    if st.button("Upload Resumes", type="secondary"):
        st.switch_page("pages/02_Upload_Page.py") 

col_sort, col_empty = st.columns([1, 4])
with col_sort:
    st.selectbox("Sort By", ["Date Added", "Company", "Status"])

try:
    api_url = f"http://web-api:4000/app_tracker/applications/{st.session_state['student_id']}?t={time.time()}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        df = pd.DataFrame()
        
except Exception as e:
    st.error(f"Error connecting to backend: {e}")
    df = pd.DataFrame()

# Creating Table
if not df.empty:
    if 'Date_Applied' in df.columns:
        df['Date_Applied'] = pd.to_datetime(df['Date_Applied']).dt.date

    if 'Status' in df.columns:
        df['Status_Normalized'] = df['Status'].str.lower()
        
        status_emoji_map = {
            "applied": "✅",
            "interviewing": "👀",
            "ghosted": "👻",
            "offer": "🎉",
            "rejected": "😢"
        }
        df['Status_Icon'] = df['Status_Normalized'].map(status_emoji_map).fillna(df['Status'])
    else:
        df['Status_Icon'] = "❓"

    resume_options = []
    try:
        api_url = f"http://web-api:4000/app_tracker/resumes/{st.session_state['student_id']}"
        response = requests.get(api_url)
        if response.status_code == 200:
            res_data = response.json()
            resume_options = [r['label'] for r in res_data if 'label' in r]
    except Exception as e:
        logger.error(f"Error fetching resumes: {e}")

    if not resume_options:
        resume_options = ["No Resumes Found"]

    if 'Resume_Used' in df.columns:
        existing_labels = set(df['Resume_Used'].dropna().unique())
        for label in existing_labels:
            if label not in resume_options:
                resume_options.append(label)

    cols_to_keep = ['Date_Applied', 'Company', 'Position', 'Status_Icon', 'Resume_Used', 'Job_Board', 'App_Portal']
    cols_to_display = [c for c in cols_to_keep if c in df.columns]
    
    display_df = df[cols_to_display]

    st.data_editor(
        display_df,
        column_config={
            "Date_Applied": st.column_config.DateColumn(
                "Date Applied", 
                format="YYYY-MM-DD"
            ),
            "Company": st.column_config.TextColumn("Company"),
            "Position": st.column_config.TextColumn("Position"),
            "Status_Icon": st.column_config.TextColumn(
                "Status", 
                help="Current Status"
            ),
            "Resume_Used": st.column_config.SelectboxColumn(
                "Resume Used",
                width="medium",
                options=resume_options,
                required=True
            ),
            "Job_Board": st.column_config.TextColumn("Job Board"),
            "App_Portal": st.column_config.LinkColumn(
                "App Portal",
                display_text="View Portal"
            )
            
        },
        
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        key=f"app_table_{len(display_df)}"
    )

    st.write("")
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
         if st.button("ADD MORE ➕", use_container_width=True):
             add_application_dialog()

    st.markdown(
        "<div style='text-align: center; color: grey; margin-top: 20px;'>"
        "Applied ✅ &nbsp;&nbsp; Interviewing 👀 &nbsp;&nbsp; Ghosted 👻 &nbsp;&nbsp; Offer 🎉 &nbsp;&nbsp; Rejected 😢"
        "</div>",
        unsafe_allow_html=True
    )

else:
    st.info("No applications found. Start tracking by clicking the Add More button!")
    if st.button("ADD MORE ➕"):
        add_application_dialog()