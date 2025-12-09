
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

# -------- HERO / TITLE --------
st.markdown("""
    <div style="
        background: linear-gradient(135deg, #E8F0FE, #FFFFFF);
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.07);
    ">
        <h1 style="color:#1a237e; font-size: 42px;">About Fresh Route</h1>
        <p style="font-size:18px; color:#424242; max-width:800px; margin:auto;">
            A data-driven grocery and meal-kit platform connecting customers, farmers, drivers, 
            and administrators to create a smarter, more sustainable food system.
        </p>
    </div>
""", unsafe_allow_html=True)

# -------- PROBLEM STATEMENT --------
st.subheader("🌱 Our Mission & Problem Statement")

st.markdown("""
Grocery shopping is rarely anyone’s favorite weekly chore, and meal prepping consumes valuable time.  
Fresh Route was created to change that.

We deliver **farm-fresh ingredients and curated recipes** directly to households through a smart, subscription-
based platform.  

Customers set dietary preferences and receive tailored meals each week.  
Farmers input what produce they have available and use **real-time analytics** to understand demand and plan harvests 
more efficiently.  
Delivery drivers receive optimized routes and clear schedules.  
Administrators oversee recipe creations, orders, and platform operations.

By transforming ordinary food purchasing into a **transparent data ecosystem**, Fresh Route empowers communities to eat 
healthier, support local agriculture, and build sustainable supply chains.
""")

st.markdown("---")

# -------- AUTHORS AS TILES --------
st.subheader("👩‍💻 Meet the Authors")

st.write("Our project team consists of five CS3200 who collaborated to build the Fresh Route platform:")

# Tile style
tile_style = """
    background-color: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    border: 1px solid #e0e0e0;
"""

# Create 5 columns (3 on top row, 2 on second)
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

with col1:
    st.markdown(f"""
        <div style="{tile_style}">
            <h3>Katherine Datlow</h3>
            <p>2nd Year Fintech + Accounting Student with a Data Science Minor</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="{tile_style}">
            <h3>Brianna Fountain</h3>
            <p>Computer Science and Finance Student</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="{tile_style}">
            <h3>Emma Kulla</h3>
            <p>2nd Year Data Science and Finance Student</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div style="{tile_style}">
            <h3>Massimo Prag</h3>
            <p>2nd Year Data Science and Finance Student</p>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div style="{tile_style}">
            <h3>Maria Samos Rivas</h3>
            <p>2nd Year Data Science and Finance Student</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------- RETURN BUTTON --------
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
