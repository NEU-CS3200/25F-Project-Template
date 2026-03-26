import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📈 Platform Reports')

# Summary metrics
st.write("### Platform Overview")

try:
    # Get system statistics from API
    stats_response = requests.get('http://api:4000/admin/statistics')

    if stats_response.status_code == 200:
        stats = stats_response.json()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Players", stats.get('total_players', 0))
        with col2:
            st.metric("Total Scouts", stats.get('total_scouts', 0))
        with col3:
            st.metric("Total Games", stats.get('total_games', 0))
        with col4:
            st.metric("Flagged Accounts", stats.get('flagged_accounts', 0))
    else:
        # Fallback metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", "5,460", "+12%")
        with col2:
            st.metric("Active Players", "3,847", "+8%")
        with col3:
            st.metric("Active Scouts", "247", "+5%")
        with col4:
            st.metric("Flagged Accounts", "27", "-3")

except Exception as e:
    st.error(f"Error loading statistics: {str(e)}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", "5,460", "+12%")
    with col2:
        st.metric("Active Players", "3,847", "+8%")
    with col3:
        st.metric("Active Scouts", "247", "+5%")
    with col4:
        st.metric("Flagged Accounts", "27", "-3")

# User growth chart
st.write("---")
st.write("### User Growth (Last 6 Months)")

growth_data = pd.DataFrame({
    'Month': ['July', 'August', 'September', 'October', 'November', 'December'],
    'Players': [3200, 3350, 3500, 3650, 3800, 3847],
    'Scouts': [210, 220, 225, 235, 242, 247]
})

fig = px.line(growth_data, x='Month', y=['Players', 'Scouts'],
              title='User Growth Trend',
              labels={'value': 'Number of Users', 'variable': 'User Type'})
st.plotly_chart(fig, use_container_width=True)

# Activity report
st.write("---")
st.write("### Activity Report")

col1, col2 = st.columns(2)

with col1:
    st.write("**Games Tracked This Month:** 156")
    st.write("**Stats Entries This Month:** 2,340")
    st.write("**Videos Uploaded This Month:** 428")

with col2:
    st.write("**Scout Reports Generated:** 89")
    st.write("**Verifications Processed:** 112")
    st.write("**Flagged Content Reviewed:** 34")

# View existing reports
st.write("---")
st.write("### Existing Reports")

try:
    # Get all reports from API
    reports_response = requests.get('http://api:4000/reports')

    if reports_response.status_code == 200:
        reports_data = reports_response.json()

        if reports_data:
            reports_df = pd.DataFrame(reports_data)
            display_df = reports_df[['reportID', 'reportName', 'reportType', 'createdDate', 'status']].copy()
            display_df.columns = ['ID', 'Name', 'Type', 'Created', 'Status']
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No reports found")
    else:
        st.warning("Could not load existing reports")

except Exception as e:
    st.warning(f"Could not load existing reports: {str(e)}")

# Generate custom report
st.write("---")
st.write("### Generate Custom Report")

with st.form("custom_report"):
    col1, col2 = st.columns(2)

    with col1:
        report_name = st.text_input("Report Name", value="Monthly Activity Report")
        report_type = st.selectbox("Report Type",
                                   ["User Activity", "Game Statistics", "Scout Performance", "System Health"])
        start_date = st.date_input("Start Date")

    with col2:
        format_type = st.selectbox("Export Format", ["PDF", "CSV", "Excel"])
        end_date = st.date_input("End Date")
        description = st.text_area("Description", value="System-generated report")

    if st.form_submit_button("Generate Report", type="primary"):
        try:
            # Create report via API
            report_data = {
                'reportName': report_name,
                'reportType': report_type,
                'createdBy': 1,  # Admin ID
                'description': description,
                'status': 'active'
            }

            create_response = requests.post('http://api:4000/reports', json=report_data)

            if create_response.status_code in [200, 201]:
                st.success(f"✅ {report_type} report generated successfully!")

                # Also create export request
                export_data = {
                    'requestedBy': 1,
                    'requestedUserType': 'admin',
                    'format': format_type,
                    'dataType': report_type,
                    'status': 'completed'
                }

                export_response = requests.post('http://api:4000/analytics/datasets/export', json=export_data)

                if export_response.status_code in [200, 201]:
                    st.download_button(
                        label="📥 Download Report",
                        data=f"Report: {report_name}\nType: {report_type}\nPeriod: {start_date} to {end_date}\n\nGenerated report data would be here.",
                        file_name=f"report_{report_type.lower().replace(' ', '_')}.{format_type.lower()}",
                        mime="text/plain"
                    )
                    st.rerun()
            else:
                st.error(f"Failed to generate report: {create_response.status_code}")

        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            # Still show download button with sample data
            st.download_button(
                label="📥 Download Report",
                data="Sample report data",
                file_name=f"report_{report_type.lower().replace(' ', '_')}.{format_type.lower()}",
                mime="text/plain"
            )
