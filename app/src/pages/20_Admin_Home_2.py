import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('System Admin Dashboard')

# Status indicator
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**Status:** :green[Running]")
with col2:
    time_range = st.selectbox('Show:', ['Last 24 Hours', 'Last 7 Days', 'Last 30 Days', 'Last 90 Days'])

time_map = {
    'Last 24 Hours': 1,
    'Last 7 Days': 7,
    'Last 30 Days': 30,
    'Last 90 Days': 90
}
days = time_map[time_range]

try:
    response = requests.get('http://web-api:4000/app_tracker/sysadmin/alerts/unresolved')
    if response.status_code == 200:
        alerts = response.json()
        if alerts:
            critical_alerts = [a for a in alerts if a.get('severity') == 'Critical']
            if critical_alerts:
                st.error(f"⚠️ ALERT!! {len(critical_alerts)} critical system issue(s) detected")
except:
    pass

st.divider()

# Create tabs
tab1, tab2 = st.tabs(["System Management", "Data Security Management"])

with tab1:
    # Create left sidebar and main content area
    col_left, col_right = st.columns([1, 3])
    
    with col_left:
        st.markdown("### Performance Trackers")
        
        # Initialize session state for selected metric
        if 'selected_metric' not in st.session_state:
            st.session_state.selected_metric = 'response time'
        
        if st.button("DB Response Time Tracker", use_container_width=True, type="primary" if st.session_state.selected_metric == 'response time' else "secondary"):
            st.session_state.selected_metric = 'response time'
            st.rerun()
        
        if st.button("CPU Utilization Manager", use_container_width=True, type="primary" if st.session_state.selected_metric == 'cpu' else "secondary"):
            st.session_state.selected_metric = 'cpu'
            st.rerun()
        
        if st.button("Request Latency Tracker", use_container_width=True, type="primary" if st.session_state.selected_metric == 'latency' else "secondary"):
            st.session_state.selected_metric = 'latency'
            st.rerun()
        
        if st.button("DB Query Frequency", use_container_width=True, type="primary" if st.session_state.selected_metric == 'query frequency' else "secondary"):
            st.session_state.selected_metric = 'query frequency'
            st.rerun()
    
    with col_right:
        metric_type = st.session_state.selected_metric
        
        metric_names = {
            'response time': 'DB Query Response Time',
            'cpu': 'CPU Utilization',
            'latency': 'Request Latency',
            'query frequency': 'DB Query Frequency'
        }
        
        st.subheader(f"{metric_names.get(metric_type, 'Performance Metrics')}")
        
        try:
            response = requests.get(f'http://web-api:4000/app_tracker/sysadmin/stats/{metric_type}/{days}')
            if response.status_code == 200:
                data = response.json()
            
                # Display metrics in columns
                col1, col2, col3, col4 = st.columns(4)
            
                with col1:
                    st.metric(
                        label=f"Average ({data.get('unit', 'N/A')})",
                        value=f"{data.get('avg_val', 0):.2f}"
                    )
            
                with col2:
                    st.metric(
                        label=f"Maximum ({data.get('unit', 'N/A')})",
                        value=f"{data.get('max_val', 0):.2f}"
                    )
                
                with col3:
                    st.metric(
                        label=f"Minimum ({data.get('unit', 'N/A')})",
                        value=f"{data.get('min_val', 0):.2f}"
                    )
                
                with col4:
                    st.metric(
                        label="Measurements",
                        value=f"{data.get('measurement_count', 0)}"
                    )
                
                st.info(f"📊 Showing data from the {time_range.lower()}")
            else:
                st.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            st.error(f"Unexpected error: No data available for the selected time period")

    st.divider()

    st.subheader("📊 Resource Usage Trends")
    
    try:
        response = requests.get(f'http://web-api:4000/app_tracker/sysadmin/resource-usage/{days}')
        if response.status_code == 200:
            usage_data = response.json()
            
            if usage_data:
                # Calculate overall averages
                total_users = sum(float(day.get('avg_active_users', 0)) for day in usage_data)
                total_apps = sum(float(day.get('avg_applications', 0)) for day in usage_data)
                total_cpu = sum(float(day.get('avg_cpu_usage', 0)) for day in usage_data)
                count = len(usage_data)
                
                # Display summary metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Avg Active Users", f"{total_users/count:.0f}")
                
                with col2:
                    st.metric("Avg Applications", f"{total_apps/count:.0f}")
                
                with col3:
                    st.metric("Avg CPU Usage", f"{total_cpu/count:.1f}%")
                
                st.divider()
                
                # Display data as table (without pandas)
                st.markdown("#### Daily Breakdown")
                
                # Create header
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                with col1:
                    st.markdown("**Date**")
                with col2:
                    st.markdown("**Avg Users**")
                with col3:
                    st.markdown("**Max Users**")
                with col4:
                    st.markdown("**Avg Apps**")
                with col5:
                    st.markdown("**Avg CPU %**")
                
                st.divider()
                
                # Display each row
                for day in usage_data:
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                    with col1:
                        st.write(day.get('usg_date', 'N/A'))
                    with col2:
                        st.write(f"{float(day.get('avg_active_users', 0)):.0f}")
                    with col3:
                        st.write(f"{float(day.get('max_active_users', 0)):.0f}")
                    with col4:
                        st.write(f"{float(day.get('avg_applications', 0)):.0f}")
                    with col5:
                        st.write(f"{float(day.get('avg_cpu_usage', 0)):.1f}")
            else:
                st.info("No resource usage data available")
        
    except Exception as e:
        st.error(f"Error fetching resource usage: {str(e)}")

with tab2:
    st.subheader("Data Security Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Backup Status & Operations")
        try:
            response = requests.get('http://web-api:4000/app_tracker/sysadmin/backups/latest')
            if response.status_code == 200:
                backup = response.json()
                st.info(f"**Last Backup:** {backup.get('datePerformed', 'N/A')}")
                st.info(f"**Status:** {backup.get('status', 'Unknown')}")
                st.info(f"**Health:** {backup.get('health', 'Unknown')}")
                if backup.get('size'):
                    st.info(f"**Size:** {backup.get('size')} GB")
            else:
                st.warning("No backup history available")
        except Exception as e:
            st.warning(f"Could not fetch backup status: {str(e)}")
        
        st.divider()
        
        # Manual backup button
        if st.button("🔄 Run Manual Backup", use_container_width=True, type="primary"):
            try:
                response = requests.post('http://web-api:4000/app_tracker/sysadmin/backup/1')
                
                if response.status_code == 201:
                    result = response.json()
                    st.success(f"✅ {result['message']}")
                    st.info(f"Backup ID: {result['backupID']}")
                else:
                    st.error(f"Backup failed: {response.status_code}")
                
            except Exception as e:
                st.error(f"Failed to initiate backup: {str(e)}")
        
        st.divider()
        
        # Show recent backups
        st.markdown("#### Recent Backups")
        try:
            response = requests.get(f'http://web-api:4000/app_tracker/sysadmin/backups/{days}')
            if response.status_code == 200:
                backups = response.json()
                if backups:
                    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
                    with col1:
                        st.markdown("**ID**")
                    with col2:
                        st.markdown("**Date**")
                    with col3:
                        st.markdown("**Status**")
                    with col4:
                        st.markdown("**Health**")
                    
                    st.divider()
                    
                    for backup in backups:
                        col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
                        with col1:
                            st.write(backup.get('backupID', 'N/A'))
                        with col2:
                            st.write(backup.get('datePerformed', 'N/A'))
                        with col3:
                            st.write(backup.get('status', 'N/A'))
                        with col4:
                            health = backup.get('health', 'N/A')
                            if health == 'Healthy':
                                st.write(f"✅ {health}")
                            else:
                                st.write(f"❌ {health}")
                else:
                    st.info("No recent backups")
            else:
                st.error(f"Error fetching backups: {response.status_code}")
        except Exception as e:
            st.error(f"Error fetching backups: {str(e)}")
    
    with col2:
        st.markdown("### 📋 Audit Log")
        
        # Hour selector for audit logs
        hours = st.selectbox("Show logs from last:", [24, 48, 72, 168], 
                            format_func=lambda x: f"{x} hours ({x//24} days)")
        
        try:
            response = requests.get(f'http://web-api:4000/app_tracker/sysadmin/audit-logs/{hours}')
            
            if response.status_code == 200:
                logs = response.json()
                
                if logs:
                    st.write(f"**Total entries:** {len(logs)}")
                    
                    # Display header
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                    with col1:
                        st.markdown("**Time**")
                    with col2:
                        st.markdown("**Action**")
                    with col3:
                        st.markdown("**Table**")
                    with col4:
                        st.markdown("**Summary**")
                    
                    st.divider()
                    
                    # Display first 20 logs
                    for log in logs[:20]:
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                        with col1:
                            st.write(log.get('timeStamp', 'N/A'))
                        with col2:
                            st.write(log.get('action', 'N/A'))
                        with col3:
                            st.write(log.get('tableName', 'N/A'))
                        with col4:
                            st.write(log.get('summary', 'N/A'))
                    
                    if len(logs) > 20:
                        st.info(f"Showing 20 of {len(logs)} entries")
                else:
                    st.info("No audit log entries found")
            else:
                st.error(f"Error fetching audit logs: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error fetching audit logs: {str(e)}")

st.divider()