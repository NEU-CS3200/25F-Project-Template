import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import datetime

# Initialize sidebar
SideBarLinks()

API_URL = "http://web-api:4000"

def get_next_inventory_id():
    try:
        response = requests.get(f"{API_URL}/f/inventory")
        if response.status_code == 200:
            entries = response.json()

            if len(entries) == 0:
                return 1  # start at 1 if empty table

            # Find max ID
            max_id = max(item["inventoryID"] for item in entries)
            return max_id + 1
        else:
            st.error("Could not fetch inventory list")
            return 1
    except:
        st.error("API connection failed — cannot retrieve inventory IDs")
        return 1
        
if "inventoryID" not in st.session_state:
    st.session_state.inventoryID = get_next_inventory_id()

st.title("Produce Editor ")

col1, spacer, col2,  = st.columns([3,1, 3], vertical_alignment="bottom")

with col1:
    st.subheader("Find Farmer")

    with st.form("farmer_form", clear_on_submit=False):
        farmerID = st.number_input("Farmer ID", min_value=1, step=1)
        search = st.form_submit_button("Search")

with col2:
    if search:
        try:
            response = requests.get(f"{API_URL}/a/farmers")

            if response.status_code != 200:
                st.error("Could not fetch farmer list.")
                st.stop()

            farmers = response.json()

            # Look for the farmer with matching ID
            farmer = next((f for f in farmers if f["farmerID"] == int(farmerID)), None)

            if not farmer:
                st.error("Farmer not found.")
            else:
                st.markdown(f"""
                ### Farmer Information  
                **Name:** {farmer['name']}  
                **Email:** {farmer['email']}  
                **Contact Info:** {farmer['contactInfo']}  
                **Status:** {farmer['status']}  
                """)
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")


if search: 
    try:
        response = requests.get(f"{API_URL}/f/farmers/{int(farmerID)}/inventory")

        if response.status_code == 200:
            st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

        else:
            st.info("Farmer found but has no inventory yet. Add items below.")
        
        st.subheader("Produce Key:")

        with st.popover("Open Produce Key"):
            st.write("List of all produce and their IDs:")

            try:
                response = requests.get(f"{API_URL}/f/produce")

                if response.status_code == 200:
                    produce_list = response.json()

                    table_data = [
                        {"Produce Name": item["name"], "Produce ID": item["produceID"]}
                        for item in produce_list
                    ]

                    st.table(table_data)

                else:
                    st.error("Could not load produce list.")

            except Exception as e:
                st.error(f"Error loading produce list: {str(e)}")


        st.subheader("Insert Produce Information:")

        with st.form("inventory_form"):

                col1, col2, col3, col4, col5 = st.columns([.5, 1.5, 1, .5, .25], vertical_alignment="bottom", width="stretch")
                farmerID = col2.number_input("Farmer ID", min_value=1, step=1)
                inventoryID = col1.text_input(
                    "Inventory",
                    value=st.session_state.inventoryID,
                    disabled=True
                    )
                produceID = col3.number_input("Produce ID", min_value=1, step=1)
                quantity = col4.number_input("Quantity", min_value=1, step=1)
                unit = col5.selectbox( "Unit", ["kg", "lbs", "pieces"], key="produce_unit")
                submit = st.form_submit_button("Submit")

        if submit:
                if not all([farmerID, produceID, quantity]):
                        st.error("Please fill in all required fields.")
                else:
                    payload = {
                        "inventoryID": st.session_state.inventoryID,
                        "produceID": int(produceID),
                        "quantity": int(quantity)
                        }

                    try:
                        response = requests.post(
                            f"{API_URL}/f/farmers/{int(farmerID)}/inventory",
                            json=payload
                            )

                        if response.status_code == 201:
                            st.success("Produce added to inventory successfully!")
                            st.session_state.inventoryID += 1
                            st.rerun()

                        else:
                            st.error(f"Error: {response.json().get('error')}")

                    except Exception as e:
                        st.error(f"Error connecting to API: {str(e)}")
                
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")