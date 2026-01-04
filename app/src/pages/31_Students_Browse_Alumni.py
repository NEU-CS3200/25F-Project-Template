import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import date, time as dt_time

st.set_page_config(layout='wide')
SideBarLinks()

st.title('🔍 Alumni Discovery')
st.write('Browse and connect with alumni mentors')

# Get current student ID from session state
current_student_id = int(st.session_state.get('user_id', 1))

# Search and filter section
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input('🔍 Search by name, field, or role', placeholder='e.g., Software Engineer, Data Science')

with col2:
    # Field filter
    fields = ['All Fields', 'Software Engineering', 'Data Science', 'Product Management', 
              'Consulting', 'Finance', 'Marketing', 'Technology', 'Healthcare']
    field_filter = st.selectbox('Field Filter', fields)

st.write('')

# Fetch alumni data from API
try:
    # Use query parameters for filtering at API level
    params = {}
    if field_filter != 'All Fields':
        params['field'] = field_filter
    
    response = requests.get('http://web-api:4000/alumni', params=params)
    
    if response.status_code == 200:
        alumni_list = response.json()
        
        # Client-side search filter
        filtered_alumni = alumni_list
        
        if search_query:
            filtered_alumni = [a for a in filtered_alumni if 
                             search_query.lower() in a.get('name', '').lower() or
                             search_query.lower() in a.get('field', '').lower() or
                             search_query.lower() in a.get('current_role', '').lower()]
        
        st.write(f'**{len(filtered_alumni)} results**')
        st.write('')
        
        # Display alumni cards
        for alumni in filtered_alumni:
            with st.container():
                col_left, col_right = st.columns([4, 1])
                
                with col_left:
                    st.subheader(f"👤 {alumni.get('name', 'N/A')}")
                    st.write(f"**{alumni.get('current_role', 'N/A')}**")
                    st.write(f"🎓 Class of {alumni.get('graduation_year', 'N/A')}")
                    st.write(f"📍 Field: {alumni.get('field', 'N/A')}")
                    
                    # Show availability
                    availability = alumni.get('availability_status', 'unavailable')
                    if availability == 'available':
                        st.success('✅ Available for mentorship')
                    else:
                        st.warning('⏸️ Currently unavailable')
                
                with col_right:
                    # Schedule meeting button for available alumni
                    availability = alumni.get('availability_status', 'unavailable')
                    if availability == 'available':
                        if st.button('📅 Schedule Meeting', key=f"schedule_{alumni['alumni_id']}", 
                                   type='primary', use_container_width=True):
                            st.session_state['schedule_with_alumni'] = alumni['alumni_id']
                            st.session_state['alumni_name'] = alumni.get('name', 'N/A')
                            st.rerun()
                    
                    # Check if already connected
                    try:
                        conn_response = requests.get(f"http://web-api:4000/connections?student_id={current_student_id}&alumni_id={alumni['alumni_id']}")
                        if conn_response.status_code == 200:
                            connections = conn_response.json()
                            is_connected = len(connections) > 0
                            
                            if is_connected:
                                st.success('Connected ✓')
                            else:
                                if st.button('Connect', key=f"connect_{alumni['alumni_id']}", 
                                           use_container_width=True):
                                    # Create connection request
                                    connection_data = {
                                        'student_id': current_student_id,
                                        'alumni_id': alumni['alumni_id'],
                                        'status': 'pending'
                                    }
                                    create_response = requests.post('http://web-api:4000/connections', 
                                                                   json=connection_data)
                                    if create_response.status_code == 201:
                                        st.success('Connection request sent!')
                                        st.rerun()
                                    else:
                                        st.error('Failed to send connection request')
                    except:
                        pass
                
                # Show scheduling form if this alumni is selected
                if st.session_state.get('schedule_with_alumni') == alumni['alumni_id']:
                    st.write('---')
                    st.write(f"### 📅 Schedule Meeting with {st.session_state.get('alumni_name')}")
                    
                    with st.form(f"schedule_form_{alumni['alumni_id']}"):
                        meeting_date = st.date_input('Meeting Date', min_value=date.today())
                        meeting_time = st.time_input('Meeting Time')
                        meeting_topic = st.text_input('Topic', placeholder='e.g., Career advice, Resume review')
                        meeting_notes = st.text_area('Notes', placeholder='What would you like to discuss?')
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            submitted = st.form_submit_button('Send Request', type='primary', use_container_width=True)
                        with col_cancel:
                            canceled = st.form_submit_button('Cancel', use_container_width=True)
                        
                        if submitted:
                            session_data = {
                                'student_id': current_student_id,
                                'alumni_id': alumni['alumni_id'],
                                'session_date': meeting_date.strftime('%Y-%m-%d'),
                                'session_time': meeting_time.strftime('%H:%M:%S'),
                                'topic': meeting_topic,
                                'notes': meeting_notes,
                                'status': 'scheduled'
                            }
                            
                            try:
                                session_response = requests.post('http://web-api:4000/sessions', json=session_data)
                                if session_response.status_code == 201:
                                    st.success('✅ Meeting scheduled successfully!')
                                    st.session_state['schedule_with_alumni'] = None
                                    st.rerun()
                                else:
                                    st.error('Failed to schedule meeting')
                            except Exception as e:
                                st.error(f'Error: {str(e)}')
                        
                        if canceled:
                            st.session_state['schedule_with_alumni'] = None
                            st.rerun()
                
                st.divider()
    
    else:
        st.error('Failed to load alumni data')
        
except Exception as e:
    st.error(f'Error connecting to server: {str(e)}')
    logger.error(f'Error in Browse_Alumni: {str(e)}')

# Quick actions at bottom
st.write('')
st.write('---')
st.write('### Quick Actions')
col1, col2 = st.columns(2)
with col1:
    if st.button('📅 My Sessions', use_container_width=True):
        st.switch_page('pages/32_Students_My_Sessions.py')
with col2:
    if st.button('👤 My Profile', use_container_width=True):
        st.switch_page('pages/33_Students_My_Profile.py')