import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Student Profiles")

STUDENTS_URL = "http://web-api:4000/students"
STUDENT_DETAIL_URL = "http://web-api:4000/students"

try:
    response = requests.get(STUDENTS_URL)
    
    if response.status_code == 200:
        students = response.json()
        
        if not students:
            st.info("No students found.")
        else:
            st.subheader(f"Profiles for {len(students)} students")
            st.write("---")
            
            for student in students:
                student_id = student.get("student_id")
                
                if student_id:
                    # Fetch detailed student info with major and location details
                    detail_response = requests.get(f"{STUDENT_DETAIL_URL}/{student_id}")
                    
                    if detail_response.status_code == 200:
                        student_detail = detail_response.json()
                        
                        # Create expandable section for each student
                        with st.expander(f"{student_detail.get('name', 'Unknown')} - {student_detail.get('email', 'No email')}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("Basic Information")
                                st.write(f"**Name:** {student_detail.get('name', 'N/A')}")
                                st.write(f"**Email:** {student_detail.get('email', 'N/A')}")
                                st.write(f"**Graduation Year:** {student_detail.get('graduation_year', 'N/A')}")
                                
                                # Display major name if available
                                major_name = student_detail.get('major_name')
                                if major_name:
                                    st.write(f"**Major:** {major_name}")
                                elif student_detail.get('major_id'):
                                    st.write(f"**Major ID:** {student_detail.get('major_id')}")
                                else:
                                    st.write("**Major:** Not specified")
                            
                            with col2:
                                st.subheader("Location")
                                # Display location details if available
                                city = student_detail.get('city')
                                state = student_detail.get('state')
                                country = student_detail.get('country')
                                
                                if city or state or country:
                                    location_parts = [part for part in [city, state, country] if part]
                                    st.write(f"**Location:** {', '.join(location_parts)}")
                                elif student_detail.get('location_id'):
                                    st.write(f"**Location ID:** {student_detail.get('location_id')}")
                                else:
                                    st.write("**Location:** Not specified")
                            
                            # Profile summary
                            profile_summary = student_detail.get('profile_summary')
                            if profile_summary:
                                st.subheader("Profile Summary")
                                st.write(profile_summary)
                            
                            # Student ID for reference
                            st.caption(f"Student ID: {student_id}")
                    else:
                        # Fallback: display basic info if detail fetch fails
                        with st.expander(f"{student.get('name', 'Unknown')} - {student.get('email', 'No email')}"):
                            st.write(f"**Name:** {student.get('name', 'N/A')}")
                            st.write(f"**Email:** {student.get('email', 'N/A')}")
                            st.write(f"**Graduation Year:** {student.get('graduation_year', 'N/A')}")
                            st.warning("Could not fetch detailed information for this student.")
                            st.caption(f"Student ID: {student_id}")
                else:
                    st.warning(f"Student record missing student_id: {student}")
    else:
        st.error(f"Failed to fetch students from the API. Status code: {response.status_code}")
        if response.status_code == 500:
            error_data = response.json()
            st.error(f"Error: {error_data.get('error', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")

# Add a button to return to Alumni Home
if st.button("Return to Alumni Home"):
    st.switch_page("pages/00_Alumni_Home.py")
