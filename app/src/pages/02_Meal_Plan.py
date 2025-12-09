import logging
logger = logging.getLogger(__name__)

import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
from modules.nav import SideBarLinks
from datetime import date
import requests

st.set_page_config(layout='wide')

SideBarLinks()

# --- Styling ---
st.markdown("""
<style>

.meal-header {
    font-size: 2.2rem;
    font-weight: 700;
    padding: 0.8rem 1rem;
    background: #A0CFA0;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}

.day-title {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

.meal-card {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 0.7rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    position: relative;
}

.meal-name {
    font-size: 1.1rem;
    font-weight: 700;
}

.meal-sub {
    font-size: 0.85rem;
    color: #555;
}

.remove-btn {
    position: absolute;
    top: 6px;
    right: 8px;
    font-size: 1.2rem;
    cursor: pointer;
}

.recipe-card {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-left: 5px solid #5FA45F;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='meal-header'>MEALS</div>", unsafe_allow_html=True)

# -------------- GET RECIPES FROM API ----------------

API_URL = "http://web-api:4000"

try:
    recipe_response = requests.get(f"{API_URL}/f/recipe")
    recipe_response.raise_for_status()
    recipe_data = recipe_response.json()
except Exception as e:
    st.error(f"Could not load recipe list: {e}")
    recipe_data = []

# Format recipes into simplified objects expected by UI
formatted_recipes = []
for r in recipe_data:
    formatted_recipes.append({
        "id": r.get("recipeID"),
        "name": r.get("name"),
        "emoji": "🥗",    # default emoji placeholder
        "short": r.get("description")[:50] + "...",
        "desc": r.get("description"),
        "ingredients": r.get("nutritionInfo", "N/A")
    })

# ------------------ Meal Plan State ------------------
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {
        day: {meal: {"recipe": None, "date": None}
        for meal in ["Breakfast", "Lunch", "Dinner"]}
        for day in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    }

if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = None

# ------------------ Render Week Grid ------------------

week_days = list(st.session_state.meal_plan.keys())
cols = st.columns(7)

for i, day in enumerate(week_days):
    with cols[i]:
        st.markdown(f"<div class='day-title'>{day[:3].upper()}</div>", unsafe_allow_html=True)

        for meal in ["Breakfast","Lunch","Dinner"]:
            slot = st.session_state.meal_plan[day][meal]
            recipe = slot["recipe"]
            meal_date = slot["date"]

            st.markdown("<div class='meal-card'>", unsafe_allow_html=True)

            # Remove button
            if st.button("✖", key=f"remove-{day}-{meal}"):
                st.session_state.meal_plan[day][meal] = {"recipe": None, "date": None}
                st.rerun()

            st.markdown(f"<div class='meal-name'>{meal}</div>", unsafe_allow_html=True)

            st.markdown(f"<div class='meal-sub'>{recipe if recipe else 'Name'}</div>", unsafe_allow_html=True)

            if meal_date:
                st.markdown(f"<div class='meal-sub'>{meal_date.strftime('%m/%d/%Y')}</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ------------------ Available Recipes ------------------

st.subheader("Available Recipes")

recipe_cols = st.columns(5)

for idx, col in enumerate(recipe_cols):
    if idx >= len(formatted_recipes):
        continue

    r = formatted_recipes[idx]

    with col:
        st.markdown(f"""
        <div style="
            background:white; border-radius:14px; padding:1.2rem;
            text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.08);
            height:160px; display:flex; flex-direction:column; justify-content:center;
        ">
            <div style="font-size:2rem;">{r['emoji']}</div>
            <div style="font-weight:700; font-size:1.1rem; margin-top:0.4rem;">{r['name']}</div>
            <div style="font-size:0.85rem; color:#444;">{r['short']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("SELECT", key=f"select-recipe-{idx}"):
            st.session_state.selected_recipe = r["name"]
            st.success(f"Selected: {r['name']}")

st.divider()

# ---------------- Assign Recipe to Meal ----------------

st.subheader("Assign Selected Recipe to a Meal")

selected_recipe = st.session_state.selected_recipe

if not selected_recipe:
    st.info("Select a recipe above to assign it to a meal.")
else:
    day = st.selectbox("Day", week_days)
    meal = st.selectbox("Meal", ["Breakfast","Lunch","Dinner"])
    chosen_date = st.date_input("Date", value=date.today(), format="MM/DD/YYYY")

    if st.button("Assign Recipe"):
        st.session_state.meal_plan[day][meal] = {
            "recipe": selected_recipe,
            "date": chosen_date
        }
        st.success(f"Assigned '{selected_recipe}' to {meal} on {day}!")
        st.rerun()
