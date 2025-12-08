import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("""
# Recipe Creator

This is where you will create and save new recipes.
""")

st.sidebar.header('Recipe Details')

#Recipe Title 
recipe_title = st.sidebar.text_input("Recipe Title")

#Photo Upload
photo = st.sidebar.file_uploader("Upload a photo of the dish", type=["jpg", "png"])

#Recipe Description
recipe_description = st.sidebar.text_area("Recipe Description", height=150) 

#Number of Ingredients
ingredient_count = st.sidebar.number_input(
    "How many ingredients?", 
    min_value=1, 
    max_value=20,
    value=5)

#Ingredient Inputs

st.subheader("Ingredients")

#Empty Ingredient table 
ingredient_data = {
    "Ingredient": ["" for _ in range(ingredient_count)],
    "Unit": ["" for _ in range(ingredient_count)],
    "Amount": ["" for _ in range(ingredient_count)]
}

df_ingredients = pd.DataFrame(ingredient_data)  

editable_ingredients = st.data_editor(df, num_rows="dynamic")

#Save button
if save: 
    st.success("Recipe saved!")
    st.write("## Recipe Summary")
    st.write(f"**Title:** {recipe_title}")
    st.write(f"**Description:** {recipe_description}")
    st.write("### Ingredients")
    st.dataframe(editable_ingredients)  

    if photo: 
        st.image(photo, caption="Uploaded Photo", width = 250)

