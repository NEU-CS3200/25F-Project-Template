import streamlit as st
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Initialize sidebar
SideBarLinks()

# ---- Styling ----
st.markdown("""
<style>
.calendar-header {
    background: linear-gradient(135deg, #EEF5FF, #F7FAFF);
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
}

.day-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.available {
    border-left: 4px solid #28a745;
}

.unavailable {
    border-left: 4px solid #dc3545;
}

.settings-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown(f"""
<div class="calendar-header">
    <h1>Availability Calendar</h1>
    <p>Manage your driving schedule, {st.session_state.get('first_name', 'Driver')}!</p>
</div>
""", unsafe_allow_html=True)

# Get driver ID from session
driver_id = st.session_state.get('driver_id')

if not driver_id:
    st.error("No driver ID found. Please log in again.")
    if st.button("Return to Home"):
        st.switch_page("Home.py")
    st.stop()

# API Base URL
API_BASE = f"http://web-api:4000/d/driver/{driver_id}/driveravailability"

# ---- Fetch existing availability ----
@st.cache_data(ttl=60)
def fetch_availability(driver_id):
    try:
        response = requests.get(f"http://web-api:4000/d/driver/{driver_id}/driveravailability")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

# Get current availability data
availability_data = fetch_availability(driver_id)
availability_by_date = {}
for entry in availability_data:
    # Handle different date formats
    # Column order: availibilityID, availStartTime, availEndTime, date, isAvailable, DriverID
    date_val = entry[3] if isinstance(entry, (list, tuple)) else entry.get('date')
    if date_val:
        # Convert to string if needed
        if hasattr(date_val, 'strftime'):
            date_str = date_val.strftime('%Y-%m-%d')
        else:
            date_str = str(date_val)[:10]
        availability_by_date[date_str] = {
            'id': entry[0] if isinstance(entry, (list, tuple)) else entry.get('availibilityID'),
            'start': entry[1] if isinstance(entry, (list, tuple)) else entry.get('availStartTime'),
            'end': entry[2] if isinstance(entry, (list, tuple)) else entry.get('availEndTime'),
            'available': entry[4] if isinstance(entry, (list, tuple)) else entry.get('isAvailable')
        }

# ---- Layout: Calendar + Settings ----
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Select Dates")
    
    # Date selector
    selected_date = st.date_input(
        "Choose a date to view or edit",
        value=datetime.now().date(),
        min_value=datetime.now().date(),
        max_value=datetime.now().date() + timedelta(days=90)
    )
    
    selected_date_str = selected_date.strftime('%Y-%m-%d')
    
    # Check if this date has existing availability
    existing_entry = availability_by_date.get(selected_date_str)
    
    st.divider()
    
    if existing_entry:
        st.success(f"You have availability set for {selected_date_str}")
        is_editing = True
        availability_id = existing_entry['id']
        
        # Parse existing times
        default_start = datetime.strptime(str(existing_entry['start'])[:8], '%H:%M:%S').time() if existing_entry['start'] else datetime.strptime('09:00:00', '%H:%M:%S').time()
        default_end = datetime.strptime(str(existing_entry['end'])[:8], '%H:%M:%S').time() if existing_entry['end'] else datetime.strptime('17:00:00', '%H:%M:%S').time()
        default_available = bool(existing_entry['available'])
    else:
        st.info(f"No availability set for {selected_date_str}. Create one below.")
        is_editing = False
        availability_id = None
        default_start = datetime.strptime('09:00:00', '%H:%M:%S').time()
        default_end = datetime.strptime('17:00:00', '%H:%M:%S').time()
        default_available = True

with col2:
    st.subheader("⚙️ Availability Settings")
    
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    
    # Toggle availability
    is_available = st.toggle("Available to work", value=default_available)
    
    st.write("**Working Hours**")
    
    # Time inputs
    start_time = st.time_input("Start Time", value=default_start)
    end_time = st.time_input("End Time", value=default_end)
    
    # Validate times
    if start_time >= end_time:
        st.warning("End time must be after start time")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Save/Update Button ----
st.divider()

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    if is_editing:
        # UPDATE existing entry
        if st.button("Update Availability", type="primary", use_container_width=True):
            update_data = {
                "date": selected_date_str,
                "availStartTime": start_time.strftime('%H:%M:%S'),
                "availEndTime": end_time.strftime('%H:%M:%S'),
                "isAvailable": is_available
            }
            
            try:
                response = requests.put(
                    f"{API_BASE}/{availability_id}",
                    json=update_data
                )
                
                if response.status_code == 200:
                    st.success("Availability updated successfully!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Failed to update: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
    else:
        # CREATE new entry
        if st.button("➕ Add Availability", type="primary", use_container_width=True):
            new_data = {
                "date": selected_date_str,
                "availStartTime": start_time.strftime('%H:%M:%S'),
                "availEndTime": end_time.strftime('%H:%M:%S'),
                "isAvailable": is_available
            }
            
            try:
                response = requests.post(API_BASE, json=new_data)
                
                if response.status_code == 201:
                    st.success("Availability added successfully!")
                    st.cache_data.clear()
                    st.rerun()
                elif response.status_code == 409:
                    st.warning("This date already has availability. Refreshing...")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Failed to add: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")

# ---- Upcoming Availability List ----
st.divider()
st.subheader("Your Upcoming Availability")

if availability_data:
    # Sort by date
    sorted_entries = sorted(availability_by_date.items(), key=lambda x: x[0])
    
    # Filter to future dates
    today_str = datetime.now().strftime('%Y-%m-%d')
    future_entries = [(d, e) for d, e in sorted_entries if d >= today_str]
    
    if future_entries:
        for date_str, entry in future_entries[:10]:  # Show next 10
            status_class = "available" if entry['available'] else "unavailable"
            status_icon = "✅" if entry['available'] else "❌"
            status_text = "Available" if entry['available'] else "Unavailable"
            
            st.markdown(f"""
            <div class="day-card {status_class}">
                <strong>{date_str}</strong> {status_icon} {status_text}<br>
                <small>🕐 {str(entry['start'])[:5]} - {str(entry['end'])[:5]}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No upcoming availability set. Use the form above to add your schedule.")
else:
    st.info("No availability data found. Start by adding your first available day!")

# ---- Footer ----
st.divider()
col_back, col_spacer = st.columns([1, 3])
with col_back:
    if st.button("← Back to Driver Home"):
        st.switch_page("pages/22_Driver_Home.py")
