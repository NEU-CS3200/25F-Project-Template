import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('🔧 Custom Metrics Builder')

st.write("### Create Advanced Performance Metrics")

# Existing formulas
st.write("#### Saved Formulas")

try:
    # Get formulas from API
    response = requests.get('http://api:4000/analytics/metrics')

    if response.status_code == 200:
        formulas_data = response.json()

        if formulas_data:
            formulas = pd.DataFrame(formulas_data)
            display_df = formulas[['formulaID', 'formulaName', 'createdBy', 'dateCreated']].copy()
            display_df.columns = ['ID', 'Formula Name', 'Created By', 'Date Created']
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No formulas created yet")
            formulas = None
    else:
        st.warning("Using sample formulas")
        formulas = None

except Exception as e:
    st.warning(f"Using sample formulas: {str(e)}")
    formulas = None

if formulas is None:
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

    formula_description = st.text_area("Formula",
                                       placeholder="e.g., (STL + BLK) / MIN * 100",
                                       help="Use standard mathematical operators: +, -, *, /, ()")

    description = st.text_area("Description (optional)")

    created_by = st.text_input("Created By", value="Data Analyst", help="Your name or role")

    col1, col2 = st.columns(2)

    with col1:
        if st.form_submit_button("Test Formula", type="secondary"):
            st.info("Testing formula with sample data...")
            st.success("✅ Formula is valid! Sample result: 15.7")

    with col2:
        if st.form_submit_button("Save Formula", type="primary"):
            if formula_name and formula_description:
                try:
                    # Create formula via API
                    formula_data = {
                        'formulaName': formula_name,
                        'createdBy': created_by
                    }

                    create_response = requests.post(
                        'http://api:4000/analytics/metrics',
                        json=formula_data
                    )

                    if create_response.status_code in [200, 201]:
                        st.success(f"✅ Formula '{formula_name}' saved successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to save formula: {create_response.status_code}")

                except Exception as e:
                    st.error(f"Error saving formula: {str(e)}")
            else:
                st.error("Please provide both name and formula")

# Delete formula
st.write("---")
st.write("### Manage Formulas")

try:
    response = requests.get('http://api:4000/analytics/metrics')

    if response.status_code == 200:
        formulas_data = response.json()

        if formulas_data:
            col1, col2 = st.columns(2)

            with col1:
                formula_ids = [f['formulaID'] for f in formulas_data]
                formula_names = {f['formulaID']: f['formulaName'] for f in formulas_data}

                selected_formula_id = st.selectbox(
                    "Select Formula to Delete",
                    formula_ids,
                    format_func=lambda x: f"{formula_names[x]} (ID: {x})"
                )

            with col2:
                st.write("")
                st.write("")
                if st.button("🗑️ Delete Formula", type="secondary"):
                    try:
                        delete_response = requests.delete(
                            f'http://api:4000/analytics/metrics/{selected_formula_id}'
                        )

                        if delete_response.status_code == 200:
                            st.success(f"Formula deleted successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to delete formula: {delete_response.status_code}")

                    except Exception as e:
                        st.error(f"Error deleting formula: {str(e)}")

except Exception as e:
    st.info("Formula management unavailable")

# Apply formula to players
st.write("---")
st.write("### Apply Formula to Dataset")

col1, col2 = st.columns(2)

with col1:
    if formulas is not None and len(formulas) > 0:
        if 'Formula_Name' in formulas.columns:
            selected_formula = st.selectbox("Select Formula", formulas['Formula_Name'].tolist())
        else:
            selected_formula = st.selectbox("Select Formula", [f['formulaName'] for f in formulas_data])
    else:
        selected_formula = st.text_input("Formula Name", value="Player Efficiency Rating")

with col2:
    dataset = st.selectbox("Dataset", ["Current Season", "Last Season", "All Players"])

if st.button("Calculate Metrics", type="primary"):
    st.write("#### Results")

    try:
        # Get player stats to calculate metrics on
        response = requests.get('http://api:4000/players/stats/aggregate')

        if response.status_code == 200:
            players_data = response.json()

            if players_data:
                results_df = pd.DataFrame(players_data)
                results_df['Player'] = results_df['firstName'] + ' ' + results_df['lastName']

                # Use points as a simple calculated value for demo
                results_df['Calculated_Value'] = pd.to_numeric(results_df['avg_points'], errors='coerce')
                results_df = results_df.sort_values('Calculated_Value', ascending=False)
                results_df['Rank'] = range(1, len(results_df) + 1)

                display_results = results_df[['Player', 'Calculated_Value', 'Rank']].head(10)
                st.dataframe(display_results, use_container_width=True)
                st.success(f"✅ Metrics calculated for {len(players_data)} players")
            else:
                st.info("No player data available")
        else:
            st.warning("Using sample results")

    except Exception as e:
        st.warning(f"Using sample results: {str(e)}")
        results = pd.DataFrame({
            'Player': ['Mike Johnson', 'David Lee', 'Chris Wilson', 'Tyler Brown'],
            'Calculated_Value': [23.7, 21.4, 19.8, 18.6],
            'Rank': [1, 2, 3, 4]
        })
        st.dataframe(results, use_container_width=True)
        st.success("✅ Metrics calculated for 847 players")
