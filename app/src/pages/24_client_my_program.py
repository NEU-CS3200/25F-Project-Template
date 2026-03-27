import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(page_title="My Program", page_icon="🎯", layout="wide")
SideBarLinks()

if 'client_id' not in st.session_state:
    st.session_state.client_id = 1
if 'client_name' not in st.session_state:
    st.session_state.client_name = "Chester Stone"

BASE_URL = "http://web-api:4000"

st.title("🎯 My Training Program")
st.markdown(f"### {st.session_state.client_name}'s Coach-Assigned Workout Plan")

st.markdown("---")

# Fetch assigned program - [Chester-3]
try:
    response = requests.get(
        f"{BASE_URL}/client/client_specific_workout_program/exercises",
        params={"client_id": st.session_state.client_id}
    )
    
    if response.status_code == 200:
        program_data = response.json()
        
        if program_data:
            df = pd.DataFrame(program_data)
            
            # Display program header
            program_name = df['program_name'].iloc[0] if 'program_name' in df.columns else "Your Workout Program"
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"📋 {program_name}")
                st.markdown("""
                This is your personalized workout program designed by your trainer. 
                Follow the prescribed sets, reps, and rest periods for optimal results.
                """)
            
            with col2:
                st.metric("Total Exercises", len(df))
                total_sets = df['sets'].sum()
                st.metric("Total Sets", total_sets)
            
            st.markdown("---")
            
            # Display exercises in expandable cards
            st.subheader("💪 Exercise Details")
            
            for idx, row in df.iterrows():
                with st.expander(f"**{idx + 1}. {row['exercise_name']}**", expanded=True):
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        st.metric("🔢 Sets", row['sets'])
                    
                    with col_b:
                        st.metric("🔁 Reps", row['reps'])
                    
                    with col_c:
                        st.metric("⏱️ Rest", f"{row['rest_period']}s")
                    
                    with col_d:
                        total_time = row['sets'] * (row['rest_period'] / 60)
                        st.metric("⏰ Est. Time", f"{total_time:.1f}min")
                    
                    # Add a workout tips section
                    st.markdown(f"""
                    **Workout Protocol:**
                    - Perform {row['sets']} sets of {row['reps']} repetitions
                    - Rest {row['rest_period']} seconds between sets
                    - Focus on proper form and controlled movement
                    """)
            
            st.markdown("---")
            
            # Summary table
            st.subheader("📊 Program Summary")
            
            summary_df = df[['exercise_name', 'sets', 'reps', 'rest_period']].copy()
            summary_df['total_reps'] = summary_df['sets'] * summary_df['reps']
            summary_df['est_time_min'] = (summary_df['sets'] * summary_df['rest_period'] / 60).round(1)
            
            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "exercise_name": "Exercise",
                    "sets": "Sets",
                    "reps": "Reps",
                    "rest_period": "Rest (sec)",
                    "total_reps": "Total Reps",
                    "est_time_min": "Est. Time (min)"
                }
            )
            
            # Program statistics
            st.markdown("---")
            st.subheader("📈 Program Statistics")
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("Exercises", len(df))
            
            with stat_col2:
                st.metric("Total Sets", df['sets'].sum())
            
            with stat_col3:
                total_reps = (df['sets'] * df['reps']).sum()
                st.metric("Total Reps", total_reps)
            
            with stat_col4:
                est_duration = (df['sets'] * df['rest_period']).sum() / 60
                st.metric("Est. Duration", f"{est_duration:.0f}min")
            
            st.markdown("---")
            
            # Export option
            st.subheader("📥 Export Program")
            
            col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
            
            with col_export1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Download as CSV",
                    data=csv,
                    file_name=f"{program_name.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_export2:
                # Create a printable version
                printable = f"""
                {program_name}
                {'=' * 50}
                
                """
                for _, row in df.iterrows():
                    printable += f"""
                {row['exercise_name']}
                - Sets: {row['sets']}
                - Reps: {row['reps']}
                - Rest: {row['rest_period']}s
                
                """
                
                st.download_button(
                    label="📄 Download as TXT",
                    data=printable,
                    file_name=f"{program_name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            # Training tips
            st.markdown("---")
            st.subheader("💡 Training Tips")
            
            st.markdown("""
            - **Warm up properly** before starting your workout
            - **Focus on form** over heavy weight
            - **Track your progress** by logging each workout
            - **Rest adequately** between workouts
            - **Stay hydrated** throughout your session
            - **Contact your trainer** if you have questions about any exercise
            """)
            
        else:
            st.info("📋 No program assigned yet. Please contact your trainer to get a personalized workout program!")
            
            st.markdown("""
            ### What to expect:
            
            Your trainer will create a customized workout program based on:
            - Your fitness goals
            - Current fitness level
            - Available equipment
            - Time commitment
            
            Once assigned, your program will appear here with detailed exercise instructions.
            """)
    
    else:
        st.error(f"Failed to load program data (Status: {response.status_code})")

except Exception as e:
    st.error(f"Error connecting to API: {str(e)}")
    st.info("Make sure your Flask API is running on http://localhost:4000")

st.markdown("---")

# Navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("pages/21_Client_home.py")

with col2:
    if st.button("📊 View Dashboard", use_container_width=True):
        st.switch_page("pages/22_client_dashboard.py")

with col3:
    if st.button("📝 Log Workout", use_container_width=True):
        st.switch_page("pages/23_client_log_workout.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>💪 FitFlow © 2025 | Questions about your program? Contact your trainer!</p>
</div>
""", unsafe_allow_html=True)