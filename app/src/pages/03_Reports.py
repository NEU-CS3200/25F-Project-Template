import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📈 Platform Reports')

# Summary metrics
st.write("### Platform Overview")

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

# Generate custom report
st.write("---")
st.write("### Generate Custom Report")

with st.form("custom_report"):
    col1, col2 = st.columns(2)

    with col1:
        report_type = st.selectbox("Report Type",
                                   ["User Activity", "Game Statistics", "Scout Performance", "System Health"])
        start_date = st.date_input("Start Date")

    with col2:
        format_type = st.selectbox("Export Format", ["PDF", "CSV", "Excel"])
        end_date = st.date_input("End Date")

    if st.form_submit_button("Generate Report", type="primary"):
        st.success(f"✅ {report_type} report generated in {format_type} format")
        st.download_button(
            label="📥 Download Report",
            data="Sample report data",
            file_name=f"report_{report_type.lower().replace(' ', '_')}.{format_type.lower()}",
            mime="text/plain"
        )