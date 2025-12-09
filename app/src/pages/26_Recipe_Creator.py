import streamlit as st
import requests
from datetime import datetime
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Recipe Creator")

SideBarLinks()

st.markdown("""
<style>
.recipe-header {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
}

.recipe-header h1 {
    color: white;
    margin: 0;
}

.recipe-header p {
    color: #a0a0a0;
    margin: 0.5rem 0 0 0;
}

.recipe-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #28a745;
}

.recipe-card.inactive {
    border-left-color: #dc3545;
    opacity: 0.7;
}

.menu-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #007bff;
}

.stats-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.stats-number {
    font-size: 2rem;
    font-weight: bold;
    color: #1a1a2e;
}

.stats-label {
    font-size: 0.85rem;
    color: #6c757d;
}

.cuisine-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    background: #e9ecef;
    color: #495057;
}

.cuisine-mediterranean { background: #d4edda; color: #155724; }
.cuisine-asian { background: #fff3cd; color: #856404; }
.cuisine-mexican { background: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="recipe-header">
    <h1>📖 Recipe Creator & Menu Manager</h1>
    <p>Create recipes, manage weekly menus, and promote seasonal ingredients</p>
</div>
""", unsafe_allow_html=True)

API_BASE = "http://web-api:4000/a"

@st.cache_data(ttl=30)
def fetch_recipes():
    try:
        response = requests.get(f"{API_BASE}/recipes")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching recipes: {e}")
        return []

@st.cache_data(ttl=30)
def fetch_weekly_menus():
    try:
        response = requests.get(f"{API_BASE}/weekly_menu/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching menus: {e}")
        return []

@st.cache_data(ttl=30)
def fetch_menu_recipes(menu_id):
    try:
        response = requests.get(f"{API_BASE}/weeklymenu/{menu_id}/recipes")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

recipes = fetch_recipes()
menus = fetch_weekly_menus()

active_recipes = [r for r in recipes if r.get('isActive')]
inactive_recipes = [r for r in recipes if not r.get('isActive')]

stat_cols = st.columns(4)
with stat_cols[0]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #28a745;">{len(active_recipes)}</div>
        <div class="stats-label">Active Recipes</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[1]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #dc3545;">{len(inactive_recipes)}</div>
        <div class="stats-label">Inactive Recipes</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[2]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #007bff;">{len(menus)}</div>
        <div class="stats-label">Weekly Menus</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[3]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number" style="color: #6c757d;">{len(recipes)}</div>
        <div class="stats-label">Total Recipes</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab_recipes, tab_create, tab_menus = st.tabs(["📋 Manage Recipes", "➕ Create Recipe", "📅 Weekly Menus"])

with tab_recipes:
    st.subheader("All Recipes")
    
    # Filters
    filter_cols = st.columns([2, 2, 2])
    with filter_cols[0]:
        filter_status = st.selectbox("Filter by Status", ["All", "Active", "Inactive"])
    with filter_cols[1]:
        cuisine_types = list(set([r.get('cuisineType', '') for r in recipes if r.get('cuisineType')]))
        filter_cuisine = st.selectbox("Filter by Cuisine", ["All"] + cuisine_types)
    with filter_cols[2]:
        search_term = st.text_input("Search recipes", placeholder="Recipe name...")

    # Apply filters
    filtered_recipes = recipes
    if filter_status == "Active":
        filtered_recipes = [r for r in filtered_recipes if r.get('isActive')]
    elif filter_status == "Inactive":
        filtered_recipes = [r for r in filtered_recipes if not r.get('isActive')]
    
    if filter_cuisine != "All":
        filtered_recipes = [r for r in filtered_recipes if r.get('cuisineType') == filter_cuisine]
    
    if search_term:
        filtered_recipes = [r for r in filtered_recipes if search_term.lower() in r.get('name', '').lower()]

    st.markdown(f"**Showing {len(filtered_recipes)} recipes**")
    
    if filtered_recipes:
        for recipe in filtered_recipes:
            recipe_id = recipe.get('recipeID')
            name = recipe.get('name', 'Unknown')
            description = recipe.get('description', '')[:100] + '...' if len(recipe.get('description', '')) > 100 else recipe.get('description', '')
            cuisine = recipe.get('cuisineType', 'N/A')
            score = recipe.get('popularityScore', 0)
            is_active = recipe.get('isActive', False)
            suitable_for = recipe.get('suitibleFor', 'N/A')
            
            status_class = "" if is_active else "inactive"
            cuisine_class = f"cuisine-{cuisine.lower()}" if cuisine.lower() in ['mediterranean', 'asian', 'mexican'] else ""
            
            with st.container():
                st.markdown(f"""
                <div class="recipe-card {status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <strong style="font-size: 1.1rem;">{name}</strong>
                            <span class="cuisine-badge {cuisine_class}" style="margin-left: 0.5rem;">{cuisine}</span>
                            {'<span style="margin-left: 0.5rem; color: #28a745;">✓ Active</span>' if is_active else '<span style="margin-left: 0.5rem; color: #dc3545;">✗ Inactive</span>'}
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 0.9rem;">⭐ {score}</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; color: #6c757d; font-size: 0.9rem;">
                        {description}
                    </div>
                    <div style="margin-top: 0.25rem; font-size: 0.8rem; color: #888;">
                        Suitable for: {suitable_for}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                btn_cols = st.columns([1, 5])
                
                with btn_cols[0]:
                    if st.button("🗑️ Delete", key=f"delete_{recipe_id}", use_container_width=True):
                        st.session_state[f'confirm_delete_{recipe_id}'] = True
                
                if st.session_state.get(f'confirm_delete_{recipe_id}', False):
                    st.warning(f"Are you sure you want to delete '{name}'?")
                    confirm_cols = st.columns(2)
                    with confirm_cols[0]:
                        if st.button("Yes, Delete", key=f"confirm_yes_{recipe_id}"):
                            try:
                                response = requests.delete(f"{API_BASE}/recipe/{recipe_id}")
                                if response.status_code == 200:
                                    st.success("Recipe deleted!")
                                    st.session_state[f'confirm_delete_{recipe_id}'] = False
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error("Failed to delete")
                            except Exception as e:
                                st.error(f"Error: {e}")
                    with confirm_cols[1]:
                        if st.button("Cancel", key=f"confirm_no_{recipe_id}"):
                            st.session_state[f'confirm_delete_{recipe_id}'] = False
                            st.rerun()
                
                st.markdown("---")
    else:
        st.info("No recipes found matching your filters.")


with tab_create:
    st.subheader("Create New Recipe")
    
    with st.form("create_recipe_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Recipe Name *", placeholder="Enter recipe name")
            new_cuisine = st.selectbox("Cuisine Type *", ['mediterranean', 'asian', 'mexican', 'american', 'italian', 'indian', 'french'])
            new_suitable = st.text_input("Suitable For", placeholder="e.g., vegetarian, vegan, gluten-free")
            new_score = st.slider("Initial Popularity Score", 0, 100, 50)
        
        with col2:
            new_description = st.text_area("Description *", placeholder="Describe the recipe...", height=100)
            new_nutrition = st.text_area("Nutrition Info *", placeholder="Calories, protein, carbs, etc.", height=100)
            new_active = st.checkbox("Set as Active", value=True)
        
        submitted = st.form_submit_button("📗 Create Recipe", use_container_width=True)
        
        if submitted:
            if not new_name or not new_description or not new_nutrition:
                st.error("Please fill in all required fields (marked with *)")
            else:
                try:
                    max_id = max([r.get('recipeID', 0) for r in recipes]) if recipes else 0
                    new_id = max_id + 1
                    
                    response = requests.post(
                        f"{API_BASE}/recipe/",
                        json={
                            "recipeID": new_id,
                            "name": new_name,
                            "description": new_description,
                            "nutritionInfo": new_nutrition,
                            "popularityScore": new_score,
                            "isActive": 1 if new_active else 0,
                            "suitibleFor": new_suitable or "all",
                            "cuisineType": new_cuisine
                        }
                    )
                    
                    if response.status_code == 201:
                        st.success(f"Recipe '{new_name}' created successfully!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Failed to create recipe: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")


with tab_menus:
    st.subheader("Weekly Menu Management")
    st.markdown("Design weekly menus using seasonal ingredients to promote freshness and variety.")
    
    current_week = datetime.now().isocalendar()[1]
    week_options = {f"Week {m.get('weekNumber', m.get('menuID', 0))}": m.get('menuID', m.get('weekNumber', 0)) for m in menus}
    
    if week_options:
        selected_week_label = st.selectbox(
            "Select Week to Manage",
            list(week_options.keys()),
            index=min(current_week - 1, len(week_options) - 1) if current_week <= len(week_options) else 0
        )
        selected_menu_id = week_options[selected_week_label]
        
        menu_recipes = fetch_menu_recipes(selected_menu_id)
        
        st.markdown(f"### {selected_week_label} Menu")
        st.markdown(f"**{len(menu_recipes)} recipes** in this menu")
        
        if menu_recipes:
            st.markdown("#### Current Recipes in Menu")
            for mr in menu_recipes:
                col1, col2 = st.columns([4, 1])
                with col1:
                    status_icon = "✓" if mr.get('isActive') else "✗"
                    st.markdown(f"""
                    <div class="menu-card">
                        <strong>{mr.get('name', 'Unknown')}</strong>
                        <span style="margin-left: 0.5rem; font-size: 0.8rem; color: #6c757d;">
                            {mr.get('cuisineType', '')} | ⭐ {mr.get('popularityScore', 0)} | {status_icon}
                        </span>
                        <div style="font-size: 0.85rem; color: #6c757d; margin-top: 0.25rem;">
                            {mr.get('description', '')[:80]}...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Remove", key=f"remove_{selected_menu_id}_{mr.get('recipeID')}"):
                        try:
                            response = requests.delete(
                                f"{API_BASE}/weeklymenu/{selected_menu_id}/recipe/{mr.get('recipeID')}"
                            )
                            if response.status_code == 200:
                                st.success("Recipe removed from menu!")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("Failed to remove")
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.info("No recipes in this menu yet. Add some below!")
        
        st.markdown("---")
        
        # Add recipe to menu
        st.markdown("#### ➕ Add Recipe to Menu")
        
        # Get recipes not in this menu
        menu_recipe_ids = [mr.get('recipeID') for mr in menu_recipes]
        available_recipes = [r for r in recipes if r.get('recipeID') not in menu_recipe_ids and r.get('isActive')]
        
        if available_recipes:
            # Group by cuisine for seasonal planning
            cuisine_filter = st.selectbox(
                "Filter by Cuisine (for seasonal variety)",
                ["All"] + list(set([r.get('cuisineType', '') for r in available_recipes if r.get('cuisineType')]))
            )
            
            if cuisine_filter != "All":
                available_recipes = [r for r in available_recipes if r.get('cuisineType') == cuisine_filter]
            
            recipe_options = {f"{r.get('name')} ({r.get('cuisineType')}) - ⭐{r.get('popularityScore')}": r.get('recipeID') for r in available_recipes}
            
            if recipe_options:
                selected_recipe = st.selectbox("Select Recipe to Add", list(recipe_options.keys()))
                selected_recipe_id = recipe_options[selected_recipe]
                
                if st.button("➕ Add to Menu", use_container_width=True):
                    try:
                        response = requests.post(
                            f"{API_BASE}/weeklymenu/{selected_menu_id}/recipe/{selected_recipe_id}"
                        )
                        if response.status_code == 201:
                            st.success("Recipe added to menu!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Failed to add: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.info("No recipes available for this cuisine filter.")
        else:
            st.info("All active recipes are already in this menu!")
    else:
        st.warning("No weekly menus found. Create one first.")

st.divider()
col_back, col_refresh = st.columns([1, 1])
with col_back:
    if st.button("← Back to Admin Home"):
        st.switch_page("pages/25_Admin_Home.py")
with col_refresh:
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()

