from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Blueprint for customer-facing routes
customer_routes = Blueprint("customer_routes", __name__)


#create a new customer account
@customer_routes.route("/customers", methods=["POST"])
def create_customer():
    try:
        data = request.get_json()

        required_fields = ["customerID", "firstName", "lastName",
                           "dietaryPref", "nutritionGoals", "email"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO Customer (customerID, firstName, lastName,
                                  dietaryPref, nutritionGoals, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["customerID"],
                data["firstName"],
                data["lastName"],
                data["dietaryPref"],
                data["nutritionGoals"],
                data["email"],
            ),
        )

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Customer created successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# return customer profile & nutrition goals
@customer_routes.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT customerID, firstName, lastName,
                   dietaryPref, nutritionGoals, email
            FROM Customer
            WHERE customerID = %s
            """,
            (customer_id,),
        )
        customer = cursor.fetchone()
        cursor.close()

        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify(customer), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Update nutrition goals and dietary preferences for the customer
@customer_routes.route("/customer/<int:customerID>", methods=["PUT"])
def update_nutrition_goals(customerID):
    try:
        data = request.get_json()

        allowed_fields = ['dietaryPref', 'nutritionGoals']
        update_fields = []
        params = []

        # Only allow updating a clear set of fields
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT customerID
            FROM Customer 
            WHERE customerID = %s
            """,
            (customerID,),
        )
        if not cursor.fetchall():
            cursor.close()
            return jsonify({"error": "Customer entry not found"}), 404

        # executes function 
        params.append(customerID)
        query = f"UPDATE Customer SET {', '.join(update_fields)} WHERE customerID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": " Updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Return delivery and new-menu notifications for a customer
@customer_routes.route("/customers/<int:customer_id>/notifications", methods=["GET"])
def get_menu_notifications(customer_id):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT notificationID, timestamp, message, farmerID, customerID
            FROM Notification
            WHERE customerID = %s
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (customer_id,))
        notifications = cursor.fetchall()
        cursor.close()

        return jsonify(notifications), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Return detailed recipe information and portioning
@customer_routes.route("/recipie/<int:recipe_id>", methods=["GET"])
def get_detailed_repice(recipeID):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT r.recipeID, r.name, r.description, r.nutritionInfo, r.cuisineType,
                   rp.produceID, rp.amountNeeded
            FROM Recipe r
            LEFT JOIN RecipeProduce rp ON r.recipeID = rp.recipeID
            WHERE r.recipeID = %s
        """
        cursor.execute(query, (recipeID,))
        recipe = cursor.fetchall()
        cursor.close()

        return jsonify(recipe), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Create a new order with selected pre-portioned ingredients/recipes
@customer_routes.route("/orders", methods=["POST"])
def create_order():
    try:
        data = request.get_json()

        required_fields = ["customerID", "deliveryAddress", "scheduledTime"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        recipes = data.get("recipes", [])
        produce_items = data.get("produce", [])

        cursor = db.get_db().cursor()

        create_order_query = """
            INSERT INTO `Order` (customerID, deliveryAddress, scheduledTime, status)
            VALUES (%s, %s, %s, 'Pending')
        """
        cursor.execute(
            create_order_query,
            (data["customerID"], data["deliveryAddress"], data["scheduledTime"])
        )

        orderID = cursor.lastrowid

        if recipes:
            recipe_query = """
                INSERT INTO OrderRecipe (orderID, recipeID)
                VALUES (%s, %s)
            """
            for recipeID in recipes:
                cursor.execute(recipe_query, (orderID, recipeID))

        if produce_items:
            produce_query = """
                INSERT INTO OrderProduce (orderID, produceID, quantityOrdered)
                VALUES (%s, %s, %s)
            """
            for item in produce_items:
                if "produceID" not in item or "quantityOrdered" not in item:
                    return jsonify({"error": "Each produce item must include produceID and quantityOrdered"}), 400
                cursor.execute(produce_query, (orderID, item["produceID"], item["quantityOrdered"]))

        db.get_db().commit()
        cursor.close()

        return jsonify({
            "message": "Order created successfully",
            "orderID": orderID,
            "recipesAdded": recipes,
            "produceAdded": produce_items
        }), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    
"""@customer_routes.route("/customers/<int:customer_id>", methods=["DELETE"])
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
        return jsonify({"error": str(e)}), 500"""

"""
@customer_routes.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    try:
        data = request.get_json()

        # Only allow updating a clear set of fields
        allowed_fields = ["dietaryPref", "nutritionGoals", "email"]
        update_fields = []
        params = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        # Make sure the customer exists
        cursor.execute(
            "SELECT customerID FROM Customer WHERE customerID = %s",
            (customer_id,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Customer not found"}), 404

        params.append(customer_id)
        query = f"UPDATE Customer SET {', '.join(update_fields)} WHERE customerID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Customer updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
"""

"""
@customer_routes.route("/customers/<int:customer_id>/messages", methods=["GET"])
def get_customer_messages(customer_id):
    try:
        cursor = db.get_db().cursor()

        query = 
            SELECT messageID, content, timestamp, customerID
            FROM CustomerMessage
            WHERE customerID = %s
            ORDER BY timestamp DESC

        cursor.execute(query, (customer_id,))
        messages = cursor.fetchall()
        cursor.close()

        return jsonify(messages), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
"""

"""
@customer_routes.route("/customers/<int:customer_id>/messages", methods=["POST"])
def create_customer_message(customer_id):
    try:
        data = request.get_json()

        required_fields = ["messageID", "content"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = 
            INSERT INTO CustomerMessage (messageID, content, timestamp, customerID)
            VALUES (%s, %s, NOW(), %s)
        cursor.execute(
            query,
            (
                data["messageID"],
                data["content"],
                customer_id,
            ),
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Message created successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
"""