import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('👤 My Profile')

# Get current student ID from session state
current_student_id = int(st.session_state.get('user_id', 1))

try:
    # Fetch student profile
    response = requests.get(f'http://web-api:4000/students/{current_student_id}')
    
    if response.status_code == 200:
        student = response.json()
        
        # Edit mode toggle
        col1, col2 = st.columns([3, 1])
        with col2:
            edit_mode = st.toggle('✏️ Edit Profile')
        
        st.write('')
        
        if edit_mode:
            st.write('### Edit Your Profile')
            
            # Fetch majors for dropdown
            majors = []
            try:
                majors_response = requests.get('http://web-api:4000/majors')
                if majors_response.status_code == 200:
                    majors = majors_response.json()
            except:
                pass
            
            # Fetch locations for dropdown
            locations = []
            try:
                locations_response = requests.get('http://web-api:4000/locations')
                if locations_response.status_code == 200:
                    locations = locations_response.json()
            except:
                pass
            
            with st.form('profile_form'):
                st.write('#### Basic Information')
                
                name = st.text_input('Full Name *', value=student.get('name', ''))
                email = st.text_input('Email *', value=student.get('email', ''))
                
                col1, col2 = st.columns(2)
                with col1:
                    # Major selection
                    if majors:
                        major_names = [m['major_name'] for m in majors]
                        current_major_name = student.get('major_name', '')
                        current_index = major_names.index(current_major_name) if current_major_name in major_names else 0
                        selected_major = st.selectbox('Major *', major_names, index=current_index)
                        selected_major_id = next((m['major_id'] for m in majors if m['major_name'] == selected_major), None)
                    else:
                        st.text_input('Major *', value=student.get('major_name', ''))
                        selected_major_id = student.get('major_id')
                
                with col2:
                    graduation_year = st.number_input('Graduation Year *', 
                                                     min_value=2020, 
                                                     max_value=2030, 
                                                     value=student.get('graduation_year', 2025))
                
                # Location selection
                if locations:
                    location_strings = [f"{l['city']}, {l['state']}" for l in locations]
                    current_location = f"{student.get('city', '')}, {student.get('state', '')}"
                    current_loc_index = location_strings.index(current_location) if current_location in location_strings else 0
                    selected_location = st.selectbox('Location *', location_strings, index=current_loc_index)
                    selected_location_id = locations[location_strings.index(selected_location)]['location_id']
                else:
                    st.text_input('Location *', value=f"{student.get('city', '')}, {student.get('state', '')}")
                    selected_location_id = student.get('location_id')
                
                st.write('#### Profile Summary')
                profile_summary = st.text_area('Tell mentors about yourself, your goals, and what you\'re looking for *',
                                              value=student.get('profile_summary', ''),
                                              height=150,
                                              help='This helps alumni understand your background and how they can help you')
                
                st.caption('* Required fields')
                
                st.write('')
                col_save, col_cancel = st.columns(2)
                with col_save:
                    submitted = st.form_submit_button('💾 Save Changes', type='primary', use_container_width=True)
                with col_cancel:
                    canceled = st.form_submit_button('Cancel', use_container_width=True)
                
                if submitted:
                    # Validate required fields
                    if not name or not email or not profile_summary:
                        st.error('Please fill in all required fields')
                    else:
                        # Update student profile
                        update_data = {
                            'name': name,
                            'email': email,
                            'major_id': selected_major_id,
                            'location_id': selected_location_id,
                            'graduation_year': graduation_year,
                            'profile_summary': profile_summary
                        }
                        
                        try:
                            update_response = requests.put(f'http://web-api:4000/students/{current_student_id}', 
                                                          json=update_data)
                            if update_response.status_code == 200:
                                st.success('✅ Profile updated successfully!')
                                st.rerun()
                            else:
                                st.error('Failed to update profile')
                        except Exception as e:
                            st.error(f'Error updating profile: {str(e)}')
                
                if canceled:
                    st.rerun()
        
        else:
            # View mode
            st.write('### Your Profile')
            
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                # Basic info
                st.write('#### Basic Information')
                info_container = st.container()
                with info_container:
                    st.write(f"**Name:** {student.get('name', 'N/A')}")
                    st.write(f"**Email:** {student.get('email', 'N/A')}")
                    st.write(f"**Major:** {student.get('major_name', 'N/A')}")
                    st.write(f"**Department:** {student.get('department', 'N/A')}")
                    st.write(f"**Graduation Year:** {student.get('graduation_year', 'N/A')}")
                    
                    location_str = f"{student.get('city', 'N/A')}, {student.get('state', 'N/A')}"
                    st.write(f"**Location:** {location_str}")
                
                st.write('')
                st.write('#### Profile Summary')
                summary_container = st.container()
                with summary_container:
                    st.write(student.get('profile_summary', 'No profile summary yet'))
                
                st.write('')
                st.caption(f"Member since: {student.get('created_at', 'N/A')}")
            
            with col_right:
                # Profile stats
                st.write('#### Your Activity')
                
                # Get connection count
                try:
                    conn_response = requests.get(f'http://web-api:4000/connections/student/{current_student_id}')
                    if conn_response.status_code == 200:
                        connections = conn_response.json()
                        active_connections = [c for c in connections if c.get('status') == 'accepted']
                        pending_connections = [c for c in connections if c.get('status') == 'pending']
                        
                        st.metric('Active Connections', len(active_connections))
                        st.metric('Pending Requests', len(pending_connections))
                except:
                    st.metric('Active Connections', 'N/A')
                
                # Get session count
                try:
                    sessions_response = requests.get(f'http://web-api:4000/sessions/student/{current_student_id}')
                    if sessions_response.status_code == 200:
                        sessions = sessions_response.json()
                        st.metric('Total Sessions', len(sessions))
                except:
                    st.metric('Total Sessions', 'N/A')
        
        # Profile completion reminder
        if not student.get('profile_summary') or len(student.get('profile_summary', '')) < 50:
            st.write('')
            st.warning('💡 **Tip:** Complete your profile summary to help alumni understand how they can best help you!')
    
    else:
        st.error('Failed to load profile')

except Exception as e:
    st.error(f'Error: {str(e)}')
    logger.error(f'Error in My_Profile: {str(e)}')

# Quick actions
st.write('')
st.write('---')
st.write('### Quick Actions')
col1, col2 = st.columns(2)
with col1:
    if st.button('🔍 Browse Alumni', use_container_width=True):
        st.switch_page('pages/31_Students_Browse_Alumni.py')
with col2:
    if st.button('📅 My Sessions', use_container_width=True):
        st.switch_page('pages/32_Students_My_Sessions.py')