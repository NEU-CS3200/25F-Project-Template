import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from modules.nav import SideBarLinks
import logging
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Your Dashboard", page_icon="📊", layout="wide")
SideBarLinks()

# Get client info
if 'client_id' not in st.session_state:
    st.session_state.client_id = 1

BASE_URL = "http://web-api:4000"

st.title("📊 Workout Dashboard")
st.markdown("### Track your training history and progress")

st.markdown("---")

# Fetch recent workout logs - [Chester-2]
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Recent Completed Workouts")
    
    try:
        response = requests.get(
            f"{BASE_URL}/client/client_workout_log",
            params={"client_id": st.session_state.client_id}
        )
        
        if response.status_code == 200:
            logs = response.json()
            
            if logs:
                df = pd.DataFrame(logs)
                df['workout_date'] = pd.to_datetime(df['workout_date']).dt.strftime('%Y-%m-%d')
                
                # Display table
                st.dataframe(
                    df[['workout_date', 'workout_name', 'duration_minutes', 'completion_status']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "workout_date": "Date",
                        "workout_name": "Workout",
                        "duration_minutes": "Duration (min)",
                        "completion_status": "Status"
                    }
                )
                
                # Quick stats below table
                st.markdown("#### Quick Statistics")
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.metric("Total Workouts", len(df))
                
                with stat_col2:
                    avg_duration = df['duration_minutes'].mean()
                    st.metric("Avg Duration", f"{avg_duration:.0f} min")
                
                with stat_col3:
                    total_time = df['duration_minutes'].sum()
                    st.metric("Total Time", f"{total_time:.0f} min")
                
                with stat_col4:
                    completed = len(df[df['completion_status'] == 'completed'])
                    st.metric("Completed", completed)
                
            else:
                st.info("No completed workouts yet. Start logging to see your progress!")
        else:
            st.error("Failed to load workouts from API")
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        st.info("Make sure your Flask API is running on http://localhost:4000")

with col2:
    st.subheader("📈 Duration Trends")
    
    # Create a simple chart of workout durations
    if 'df' in locals() and not df.empty:
        fig = px.line(
            df.head(10),
            x='workout_date',
            y='duration_minutes',
            title='Recent Workout Durations',
            markers=True
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Duration (min)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Monthly Completion Comparison - [Chester-4]
st.subheader("📊 Monthly Workout Comparison")

col_a, col_b = st.columns([3, 2])

with col_a:
    try:
        response = requests.get(
            f"{BASE_URL}/client/client_workout_log/completion_rate/monthly",
            params={"client_id": st.session_state.client_id}
        )
        
        if response.status_code == 200:
            monthly_data = response.json()
            
            if monthly_data:
                monthly_df = pd.DataFrame(monthly_data)
                
                # Create bar chart
                fig = px.bar(
                    monthly_df,
                    x='month',
                    y='workouts_completed',
                    title='Workouts Completed by Month',
                    labels={'month': 'Month', 'workouts_completed': 'Workouts'},
                    color='workouts_completed',
                    color_continuous_scale='Blues',
                    text='workouts_completed'
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(showlegend=False)
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data for monthly comparison yet")
    except Exception as e:
        st.error(f"Error loading monthly data: {str(e)}")

with col_b:
    st.markdown("#### Monthly Breakdown")
    
    if 'monthly_df' in locals() and not monthly_df.empty:
        # Add month names
        month_names = {
            10: 'October', 11: 'November', 12: 'December',
            1: 'January', 2: 'February', 3: 'March',
            4: 'April', 5: 'May', 6: 'June',
            7: 'July', 8: 'August', 9: 'September'
        }
        monthly_df['month_name'] = monthly_df['month'].map(month_names)
        
        st.dataframe(
            monthly_df[['month_name', 'workouts_completed']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "month_name": "Month",
                "workouts_completed": "Workouts"
            }
        )
        
        # Show comparison if we have at least 2 months
        if len(monthly_df) >= 2:
            current_month = monthly_df.iloc[0]['workouts_completed']
            previous_month = monthly_df.iloc[1]['workouts_completed']
            change = current_month - previous_month
            
            st.metric(
                "This Month vs Last Month",
                f"{current_month} workouts",
                delta=f"{change:+d} workouts",
                delta_color="normal"
            )
            
            if change > 0:
                st.success(f"🎉 Great job! You increased your workout count by {change}!")
            elif change < 0:
                st.warning(f"You completed {abs(change)} fewer workouts. Let's get back on track!")
            else:
                st.info("You maintained the same workout count. Consistency is key!")

st.markdown("---")

# Navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("pages/21_Client_home.py")

with col2:
    if st.button("📝 Log a Workout", use_container_width=True):
        st.switch_page("pages/23_client_log_workout.py")

with col3:
    if st.button("🎯 View My Program", use_container_width=True):
        st.switch_page("pages/24_client_my_program.py")