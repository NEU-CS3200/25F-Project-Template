import streamlit as st
import pandas as pd
import requests
import logging
logger = logging.getLogger(__name__)

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Appli-Tracker - Upload")

SideBarLinks()

if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'James'
if 'student_id' not in st.session_state:
    st.session_state['student_id'] = 888881 

col_title, col_user = st.columns([4, 1])

with col_title:
    st.title("Resume Upload Menu")

with col_user:
    st.write("")
    st.write("")
    st.write(f"**Logged In As:** {st.session_state['first_name']}")
    if st.button("Go to Applications", type="secondary"):
        st.switch_page("pages/01_Application_Status.py") 



try:
    api_url = f"http://web-api:4000/app_tracker/resumes/{st.session_state['student_id']}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
    else:
        st.error(f"Failed to fetch resumes. Status code: {response.status_code}")
        df = pd.DataFrame()


except Exception as e:
    st.error(f"Error connecting to backend: {e}")
    df = pd.DataFrame()

# Table
if not df.empty:
    df_display = df.rename(columns={
        "label": "Resume Label",
        "imageURl": "Links to View"
    })

    st.data_editor(
        df_display,
        column_config={
            "Uploaded Resumes": st.column_config.TextColumn(
                "Uploaded Resumes",
                help="The specific role this resume targets",
                width="medium"
            ),
            "Links to View": st.column_config.LinkColumn(
                "Links to View",
                display_text="View PDF",
                help="Click to open resume"
            )
        },
        hide_index=True,
        use_container_width=True,
        disabled=True
    )
else:
    st.info("No resumes found. Upload your first one below!")

st.write("")
st.write("")

# Upload Section
st.markdown("### Upload New Resume")

with st.container(border=True):
    with st.form("resume_upload_form", clear_on_submit=True):
        
        col_input, col_file = st.columns(2)
        
        with col_input:
            resume_label = st.text_input("Resume Label", 
                                        placeholder="Ex. Software Engineer")
        with col_file:
            uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

        st.write("")
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submitted = st.form_submit_button("UPLOAD ⬆️", use_container_width=True)

        if submitted:
            if uploaded_file is not None:
                try:
                    upload_url = "http://web-api:4000/app_tracker/resumes/upload"
                    files = {'file': uploaded_file}
                    data = {
                        'studentID': st.session_state['student_id'],
                        'label': resume_label
                    }
                    response = requests.post(upload_url, data=data, files=files)
                    
                    if response.status_code == 201:
                        st.success(f"Successfully uploaded {uploaded_file.name} as '{resume_label}'!")
                        st.rerun()
                    else:
                        st.error(f"Failed to upload. Server responded: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error during upload: {e}")
            else:
                st.warning("Please attach a PDF file first.")