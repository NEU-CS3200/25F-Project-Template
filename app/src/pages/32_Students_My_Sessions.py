import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime, date, time

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📅 My Sessions')
st.write('Manage your mentorship sessions')

# Get current student ID from session state
current_student_id = int(st.session_state.get('user_id', 1))

try:
    # Fetch all sessions for this student using query parameters
    response = requests.get(f'http://web-api:4000/sessions?student_id={current_student_id}')
    
    if response.status_code == 200:
        sessions = response.json()
        
        # Separate sessions by time
        today = datetime.now().date()
        upcoming = [s for s in sessions if datetime.strptime(s['session_date'], '%Y-%m-%d').date() >= today]
        past = [s for s in sessions if datetime.strptime(s['session_date'], '%Y-%m-%d').date() < today]
        
        # Sort upcoming by date
        upcoming.sort(key=lambda x: x['session_date'])
        # Sort past by date (most recent first)
        past.sort(key=lambda x: x['session_date'], reverse=True)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Total Sessions', len(sessions))
        with col2:
            st.metric('Upcoming', len(upcoming))
        with col3:
            st.metric('Completed', len(past))
        
        st.write('')
        
        # Tabs
        tab1, tab2 = st.tabs(['📅 Upcoming Sessions', '📝 Past Sessions'])
        
        with tab1:
            st.write('### Upcoming Sessions')
            
            if upcoming:
                for session in upcoming:
                    alumni_id = session.get('alumni_id')
                    
                    # Fetch alumni details
                    alumni_name = 'Unknown'
                    alumni_role = 'N/A'
                    try:
                        alumni_response = requests.get(f'http://web-api:4000/alumni/{alumni_id}')
                        if alumni_response.status_code == 200:
                            alumni = alumni_response.json()
                            alumni_name = alumni.get('name', 'Unknown')
                            alumni_role = alumni.get('current_role', 'N/A')
                    except:
                        pass
                    
                    with st.container():
                        # Session card
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.subheader(f"Meeting with {alumni_name}")
                            st.write(f"**{alumni_role}**")
                            st.write(f"📅 **Date:** {session['session_date']}")
                            st.write(f"⏰ **Time:** {session.get('session_time', 'TBD')}")
                            st.write(f"📌 **Topic:** {session.get('topic', 'No topic specified')}")
                            
                            # Status badge
                            status = session.get('status', 'scheduled')
                            if status == 'scheduled':
                                st.success('✅ Confirmed')
                            elif status == 'pending':
                                st.warning('⏳ Awaiting confirmation')
                            elif status == 'cancelled':
                                st.error('❌ Cancelled')
                            
                            # Notes
                            if session.get('notes'):
                                with st.expander('📝 Session Notes'):
                                    st.write(session['notes'])
                        
                        with col2:
                            st.write('')
                            st.write('')
                            
                            if st.button('Cancel Session', key=f"cancel_{session['session_id']}", 
                                       use_container_width=True):
                                # Update session status to cancelled
                                update_data = {'status': 'cancelled'}
                                update_response = requests.put(f"http://web-api:4000/sessions/{session['session_id']}", 
                                                              json=update_data)
                                if update_response.status_code == 200:
                                    st.success('Session cancelled')
                                    st.rerun()
                                else:
                                    st.error('Failed to cancel session')
                        
                        st.divider()
            else:
                st.info('No upcoming sessions scheduled')
                if st.button('Browse Alumni to Schedule a Session'):
                    st.switch_page('pages/31_Students_Browse_Alumni.py')
        
        with tab2:
            st.write('### Past Sessions')
            
            if past:
                for session in past:
                    alumni_id = session.get('alumni_id')
                    
                    # Fetch alumni details
                    alumni_name = 'Unknown'
                    alumni_role = 'N/A'
                    try:
                        alumni_response = requests.get(f'http://web-api:4000/alumni/{alumni_id}')
                        if alumni_response.status_code == 200:
                            alumni = alumni_response.json()
                            alumni_name = alumni.get('name', 'Unknown')
                            alumni_role = alumni.get('current_role', 'N/A')
                    except:
                        pass
                    
                    with st.expander(f"📅 {session['session_date']} - {alumni_name} - {session.get('topic', 'No topic')}"):
                        st.write(f"**Mentor:** {alumni_name}")
                        st.write(f"**Role:** {alumni_role}")
                        st.write(f"**Time:** {session.get('session_time', 'N/A')}")
                        st.write(f"**Topic:** {session.get('topic', 'No topic')}")
                        
                        st.write('')
                        st.write('**Session Notes:**')
                        if session.get('notes'):
                            st.write(session['notes'])
                        else:
                            st.caption('No notes recorded')
                        
                        st.write('')
                        
                        # Add/edit notes
                        with st.form(f"notes_form_{session['session_id']}"):
                            st.write('**Add Follow-up Notes:**')
                            additional_notes = st.text_area('Record key takeaways, advice, or action items', 
                                                           key=f"notes_input_{session['session_id']}")
                            
                            if st.form_submit_button('Save Notes'):
                                # Append to existing notes
                                current_notes = session.get('notes', '')
                                updated_notes = f"{current_notes}\n\n---\nFollow-up ({datetime.now().strftime('%Y-%m-%d')}):\n{additional_notes}"
                                
                                update_data = {'notes': updated_notes}
                                update_response = requests.put(f"http://web-api:4000/sessions/{session['session_id']}", 
                                                              json=update_data)
                                if update_response.status_code == 200:
                                    st.success('Notes saved!')
                                    st.rerun()
                                else:
                                    st.error('Failed to save notes')
            else:
                st.info('No past sessions yet')
    
    else:
        st.error('Failed to load sessions')

except Exception as e:
    st.error(f'Error: {str(e)}')
    logger.error(f'Error in My_Sessions: {str(e)}')

# Quick actions
st.write('')
st.write('---')
st.write('### Quick Actions')
col1, col2 = st.columns(2)
with col1:
    if st.button('🔍 Browse Alumni', use_container_width=True):
        st.switch_page('pages/31_Students_Browse_Alumni.py')
with col2:
    if st.button('👤 My Profile', use_container_width=True):
        st.switch_page('pages/33_Students_My_Profile.py')