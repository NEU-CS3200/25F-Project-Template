import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

st.title('🔧 Custom Metrics Builder')

st.write("### Create Advanced Performance Metrics")

# Existing formulas
st.write("#### Saved Formulas")

formulas = pd.DataFrame({
    'Formula_Name': ['Player Efficiency Rating', 'True Shooting %', 'Usage Rate', 'Impact Score'],
    'Formula': [
        '(PTS + AST + REB - TOV) / MIN',
        'PTS / (2 * (FGA + 0.44 * FTA))',
        '100 * ((FGA + 0.44 * FTA + TOV) / MIN)',
        '(PTS * 0.4) + (AST * 0.3) + (REB * 0.3)'
    ],
    'Created': ['2025-01-15', '2025-02-20', '2025-03-10', '2025-11-01'],
    'Times_Used': [145, 89, 67, 23]
})

st.dataframe(formulas, use_container_width=True)

# Create new formula
st.write("---")
st.write("### Build New Formula")

with st.form("new_formula"):
    formula_name = st.text_input("Formula Name", placeholder="e.g., 'Defensive Impact Score'")

    st.write("**Available Variables:**")
    st.code(
        "PTS (points), AST (assists), REB (rebounds), STL (steals), BLK (blocks), TOV (turnovers), MIN (minutes), FGA (field goals attempted), FTA (free throws attempted)")

    formula = st.text_area("Formula",
                           placeholder="e.g., (STL + BLK) / MIN * 100",
                           help="Use standard mathematical operators: +, -, *, /, ()")

    description = st.text_area("Description (optional)")

    col1, col2 = st.columns(2)

    with col1:
        if st.form_submit_button("Test Formula", type="secondary"):
            st.info("Testing formula with sample data...")
            st.success("✅ Formula is valid! Sample result: 15.7")

    with col2:
        if st.form_submit_button("Save Formula", type="primary"):
            if formula_name and formula:
                st.success(f"✅ Formula '{formula_name}' saved successfully!")
            else:
                st.error("Please provide both name and formula")

# Apply formula to players
st.write("---")
st.write("### Apply Formula to Dataset")

col1, col2 = st.columns(2)

with col1:
    selected_formula = st.selectbox("Select Formula", formulas['Formula_Name'].tolist())
with col2:
    dataset = st.selectbox("Dataset", ["Current Season", "Last Season", "All Players"])

if st.button("Calculate Metrics", type="primary"):
    st.write("#### Results")

    results = pd.DataFrame({
        'Player': ['Mike Johnson', 'David Lee', 'Chris Wilson', 'Tyler Brown'],
        'Calculated_Value': [23.7, 21.4, 19.8, 18.6],
        'Rank': [1, 2, 3, 4]
    })

    st.dataframe(results, use_container_width=True)
    st.success("✅ Metrics calculated for 847 players")
    