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

st.title("Produce Editor 🧺")

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
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Produce Key:")

    with st.popover("Open Produce Key"):
        st.write("All produce and their IDs:")
        try:
            resp = requests.get(f"{API_URL}/f/produce")
            if resp.status_code == 200:
                produce_list = resp.json()
                table_data = [{"Produce": p["name"], "ID": p["produceID"]} for p in produce_list]
                st.table(table_data)
            else:
                st.error("Could not load produce list.")
        except Exception as e:
            st.error(f"Error loading produce list: {str(e)}")

    st.subheader("Add Produce to Inventory")

    with st.form("inventory_add_form"):
        colA, colB, colC, colD, colE = st.columns([0.5, 1.5, 1, 0.7, 0.7])

        inventoryID = colA.text_input("Inventory ID", value=st.session_state.inventoryID, disabled=True)
        farmerID_input = colB.number_input("Farmer ID", min_value=1, value=int(farmerID))
        produceID = colC.number_input("Produce ID", min_value=1, step=1)
        quantity = colD.number_input("Quantity", min_value=1, step=1)
        unit = colE.selectbox("Unit", ["kg", "lbs", "pieces"])

        add_submit = st.form_submit_button("Add Produce")

    if add_submit:
        payload = {
            "inventoryID": int(inventoryID),
            "produceID": int(produceID),
            "quantity": int(quantity)
        }

        try:
            r = requests.post(f"{API_URL}/f/farmers/{farmerID_input}/inventory", json=payload)
            if r.status_code == 201:
                st.success("Produce added successfully!")
                st.session_state.inventoryID += 1
                st.rerun()
            else:
                st.error(f"Error: {r.json().get('error')}")
        except Exception as e:
            st.error(f"API error: {str(e)}")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Delete Inventory Entry")

    with st.form("inventory_delete_form"):
        colX, colY = st.columns([1, 1])

        delete_inventoryID = colX.number_input("Inventory ID to delete", min_value=1, step=1)
        delete_submit = st.form_submit_button("Delete")

    if delete_submit:
        try:
            r = requests.delete(f"{API_URL}/f/farmers/{farmerID}/inventory/{delete_inventoryID}")
            if r.status_code == 200:
                st.success("Inventory deleted.")
                st.rerun()
            elif r.status_code == 404:
                st.warning("Inventory ID not found.")
            else:
                st.error("Delete failed.")
        except Exception as e:
            st.error(f"API error: {str(e)}")