from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error

# Blueprint for admin-facing routes
admin_routes = Blueprint("admin_routes", __name__)

# deleting customer account uppon request 
@admin_routes.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT customerID FROM Customer WHERE customerID = %s",
            (customer_id,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Customer not found"}), 404

        cursor.execute("DELETE FROM Customer WHERE customerID = %s", (customer_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Customer deleted successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# message history retur between admin and customer 
@admin_routes.route("/customer/<int:customerID>/customermessages", methods=["GET"])
def get_customer_message_history(customerID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT messageID, content, timestamp, customerID
            FROM CustomerMessages 
            WHERE customerID = %s
            """,
            (customerID,),
            )
        order_list = cursor.fetchall()
        cursor.close()

        return jsonify(order_list), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

# admin sends a new message 
@admin_routes.route("/customer/<int:customerID>/customermessages", methods=["POST"])
def send_message(customerID):
    try:
        data = request.get_json()

        required_fields = ["messageID", "content", "timestamp"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO CustomerMessages (messageID, content, timestamp, customerID)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                data["messageID"],
                data['content'],
                data['timestamp'], 
                customerID,
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Message sent succesfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# creates new recipe
@admin_routes.route("/recipe/", methods=["POST"])
def create_recipe():
    try:
        data = request.get_json()

        required_fields = ["recipeID", "name", "description", "nutritionInfo", "popularityScore", "isActive", "suitibleFor", "cuisineType"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO Recipe (recipeID, name, description, nutritionInfo, popularityScore, isActive, suitibleFor, cuisineType)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                data["recipeID"],
                data['name'],
                data['description'], 
                data['nutritionInfo'],
                data['popularityScore'], 
                data['isActive'], 
                data['suitibleFor'], 
                data['cuisineType']
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Recipe created succesfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# deleting unpopular recipe
@admin_routes.route("/recipe/<int:recipeID>", methods=["DELETE"])
def delete_recipe(recipeID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT recipeID FROM Recipe WHERE recipeID = %s",
            (recipeID,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Recipe not found"}), 404

        cursor.execute("DELETE FROM Recipe WHERE recipeID = %s", (recipeID,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Recipe deleted successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Get all recipes
@admin_routes.route("/recipes", methods=["GET"])
def get_all_recipes():
    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            """
            SELECT recipeID, name, description, nutritionInfo, popularityScore, isActive, suitibleFor, cuisineType
            FROM Recipe
            ORDER BY name
            """
        )
        rows = cursor.fetchall()
        cursor.close()

        result = []
        for row in rows:
            result.append({
                'recipeID': row['recipeID'],
                'name': row['name'],
                'description': row['description'],
                'nutritionInfo': row['nutritionInfo'],
                'popularityScore': row['popularityScore'],
                'isActive': bool(row['isActive']),
                'suitableFor': row['suitibleFor'],
                'cuisineType': row['cuisineType']
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get recipes for a specific weekly menu
@admin_routes.route("/weeklymenu/<int:menuID>/recipes", methods=["GET"])
def get_menu_recipes(menuID):
    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            """
            SELECT r.recipeID, r.name, r.description, r.cuisineType, r.popularityScore, r.isActive
            FROM Recipe r
            JOIN Recipe_WeeklyMenu rwm ON r.recipeID = rwm.recipeID
            WHERE rwm.menuID = %s
            ORDER BY r.name
            """,
            (menuID,)
        )
        rows = cursor.fetchall()
        cursor.close()

        result = []
        for row in rows:
            result.append({
                'recipeID': row['recipeID'],
                'name': row['name'],
                'description': row['description'],
                'cuisineType': row['cuisineType'],
                'popularityScore': row['popularityScore'],
                'isActive': bool(row['isActive'])
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add recipe to weekly menu
@admin_routes.route("/weeklymenu/<int:menuID>/recipe/<int:recipeID>", methods=["POST"])
def add_recipe_to_menu(menuID, recipeID):
    try:
        cursor = db.get_db().cursor()

        # Check if menu exists
        cursor.execute("SELECT menuID FROM weeklyMenu WHERE menuID = %s", (menuID,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Menu not found"}), 404

        # Check if recipe exists
        cursor.execute("SELECT recipeID FROM Recipe WHERE recipeID = %s", (recipeID,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Recipe not found"}), 404

        # Check if already in menu
        cursor.execute(
            "SELECT * FROM Recipe_WeeklyMenu WHERE menuID = %s AND recipeID = %s",
            (menuID, recipeID)
        )
        if cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Recipe already in this menu"}), 409

        # Add recipe to menu
        cursor.execute(
            "INSERT INTO Recipe_WeeklyMenu (menuID, recipeID) VALUES (%s, %s)",
            (menuID, recipeID)
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Recipe added to menu successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Remove recipe from weekly menu
@admin_routes.route("/weeklymenu/<int:menuID>/recipe/<int:recipeID>", methods=["DELETE"])
def remove_recipe_from_menu(menuID, recipeID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT * FROM Recipe_WeeklyMenu WHERE menuID = %s AND recipeID = %s",
            (menuID, recipeID)
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Recipe not in this menu"}), 404

        cursor.execute(
            "DELETE FROM Recipe_WeeklyMenu WHERE menuID = %s AND recipeID = %s",
            (menuID, recipeID)
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Recipe removed from menu successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# return list of farmers
@admin_routes.route("/farmers", methods=["GET"])
def get_farmers():
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT farmerID, name, status, email, contactInfo
            FROM Farmer 
            """,
            )
        order_list = cursor.fetchall()
        cursor.close()

        return jsonify(order_list), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Update farmer status
@admin_routes.route("/farmer/<int:farmerID>", methods=["PUT"])
def update_farmer(farmerID):
    try:
        data = request.get_json()

        allowed_fields = ["status"]
        update_fields = []
        params = []
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT farmerID 
            FROM Farmer 
            WHERE farmerID = %s
            """,
            (farmerID,),
        )
        if not cursor.fetchall():
            cursor.close()
            return jsonify({"error": "Farmer entry not found"}), 404

        # executes function 
        params.append(farmerID)
        query = f"UPDATE Farmer SET {', '.join(update_fields)} WHERE farmerID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Farmer status updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# return weekly menu 
@admin_routes.route("/weekly_menu/", methods=["GET"])
def get_weekly_menu():
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT *
            FROM weeklyMenu; 
            """,
            )
        order_list = cursor.fetchall()
        cursor.close()

        return jsonify(order_list), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

# creates new weekly menu
@admin_routes.route("/weeklymenu", methods=["POST"])
def create_weekly_menu():
    try:
        data = request.get_json()

        required_fields = ["menuID", "weekNumber"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO weeklyMenu (menuID, weekNumber)
            VALUES (%s, %s)
        """

        cursor.execute(
            query,
            (
                data["menuID"],
                data['weekNumber'],
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Weekly Menu set up succesfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Update/adjust weekly menu
@admin_routes.route("/weeklymenu/<int:menuID>", methods=["PUT"])
def update_weekly_menu(menuID):
    try:
        data = request.get_json()

        allowed_fields = ["menuID", 'weekNumber']
        update_fields = []
        params = []
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT menuID
            FROM WeeklyMenu 
            WHERE menuID = %s
            """,
            (menuID,),
        )
        if not cursor.fetchall():
            cursor.close()
            return jsonify({"error": "Menu ID not found"}), 404

        # executes function 
        params.append(menuID)
        query = f"UPDATE WeeklyMenu SET {', '.join(update_fields)} WHERE menuID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "week menu updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Get list of all customers
@admin_routes.route("/admin/customers", methods=["GET"])
def get_all_customers():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT customerID, firstName, lastName, email
            FROM Customer
        """)
        
        customers = cursor.fetchall()
        cursor.close()

        return jsonify(customers), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
