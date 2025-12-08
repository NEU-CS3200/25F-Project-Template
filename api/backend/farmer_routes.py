from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Blueprint for customer-facing routes
farmer_routes = Blueprint("farmer_routes", __name__)

#List all produce
@farmer_routes.route("/produce", methods=["GET"])
def get_all_produce():
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT produceID, name, expectedHarvestDate, quantityAvailable, unit " \
            "FROM Produce"
            )
        produce_list = cursor.fetchall()
        cursor.close()

        return jsonify(produce_list), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

@farmer_routes.route("/ingredient", methods=["GET"])
def get_all_ingredient():
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT * " \
            "FROM Ingredient"
            )
        ingredient_list = cursor.fetchall()
        cursor.close()

        return jsonify(ingredient_list), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#Farmer lists new produce item
@farmer_routes.route("/produce", methods=["POST"])
def create_produce():
    try:
        data = request.get_json()

        required_fields = ["produceID", "name", "expectedHarvestDate", "quantityAvailable", "unit"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO Produce (produceID, name, expectedHarvestDate, quantityAvailable, unit)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                data["produceID"],
                data['name'],
                data['expectedHarvestDate'], 
                data["quantityAvailable"], 
                data['unit']
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Produce created succesfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Return produce details
@farmer_routes.route("/produce/<int:produceID>", methods=["GET"])
def get_produce(produceID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT produceID, name, expectedHarvestDate, quantityAvailable, unit
            FROM Produce
            WHERE produceID = %s
            """,
            (produceID,),
        )
        produce = cursor.fetchone()
        cursor.close()

        if not produce:
            return jsonify({"error": "Produce not found"}), 404

        return jsonify(produce), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

#Update produce attributes
@farmer_routes.route("/produce/<int:produceID>", methods=["PUT"])
def update_produce(produceID):
    try:
        data = request.get_json()

        allowed_fields = ["name", "unit", "quantityAvailable", "expectedHarvestDate"]
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

        # Make sure the produce exists
        cursor.execute(
            "SELECT produceID " \
            "FROM Produce " \
            "WHERE produceID = %s",
            (produceID,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Produce entry not found"}), 404

        # executes function 
        params.append(produceID)
        query = f"UPDATE Produce SET {', '.join(update_fields)} WHERE produceID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Produce updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Return all recipes with filtering by popularity
@farmer_routes.route("/recipe", methods=["GET"])
def get_recipes():
    try:
        cursor = db.get_db().cursor()

        query = """
                SELECT recipeID, name, description, popularityScore
                FROM Recipe
                ORDER BY popularityScore DESC
            """
        cursor.execute(query)

        recipes = cursor.fetchall()
        cursor.close()

        if not recipes:
            return jsonify({"error": "No recipes found"}), 404

        return jsonify(recipes), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Inventory list for farmer
@farmer_routes.route("/farmers/<int:farmerID>/inventory", methods=["GET"])
def get_farmer_inventory(farmerID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT inventoryID, farmerID, produceID, dateUpdate, quantity
            FROM InventoryEntry
            WHERE farmerID = %s
            """,
            (farmerID,),
        )
        recipe = cursor.fetchall()
        cursor.close()

        if not recipe:
            return jsonify({"error": "Produce not found"}), 404

        return jsonify(recipe), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Add a new inventory entry
@farmer_routes.route("/farmers/<int:farmerID>/inventory", methods=["POST"])
def add_new_inventory_entry(farmerID):
    try:
        data = request.get_json()

        required_fields = ["inventoryID", "produceID", "quantity"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO InventoryEntry (inventoryID, farmerID, produceID, dateUpdate, quantity)
            VALUES (%s, %s, %s, NOW(), %s)
        """

        cursor.execute(
            query,
            (
                data["inventoryID"],
                farmerID,
                data["produceID"], 
                data['quantity']
            )
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Produce updated succesfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Add a new inventory entry
@farmer_routes.route("/farmers/<int:farmerID>/Inventory/<int:inventoryID>", methods=["PUT"])
def update_farmer_inventory(farmerID, inventoryID):
    try:
        data = request.get_json()

        if "quantity" not in data:
            return jsonify({"error": "Missing required field: quantity"}), 400
        
        cursor = db.get_db().cursor()

        # Make sure the produce exists
        cursor.execute(
            "SELECT inventoryID " \
            "FROM InventoryEntry " \
            "WHERE farmerID = %s AND inventoryID = %s",
            (farmerID,inventoryID,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Produce entry not found"}), 404
        
        cursor.execute(
            """
            UPDATE InventoryEntry
            SET quantity = %s, dateUpdate = NOW()
            WHERE farmerID = %s AND inventoryID = %s
            """,
            (data["quantity"], farmerID, inventoryID)
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Inventory updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Demand prediction
@farmer_routes.route("/demand/produce/<int:produceID>", methods=["GET"])
def get_demand(produceID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT produceID, forcastID, predictedDemand
            FROM Demand
            WHERE produceID = %s
            """,
            (produceID,),
        )
        recipe = cursor.fetchone()
        cursor.close()

        if not recipe:
            return jsonify({"error": "Demand not found"}), 404

        return jsonify(recipe), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# List all orders containing this farmer's produce
@farmer_routes.route("/order", methods=["GET"])
def get_inventory():
    try:
        farmerID = request.args.get("farmerID")
    
        if not farmerID:
            return jsonify({"error": "farmerID query parameter required"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT o.orderID, o.status, o.customerID, o.driverID
            FROM `Order` o
            JOIN OrderProduce op ON o.orderID = op.orderID
            JOIN InventoryEntry i ON op.produceID = i.produceID
            WHERE i.farmerID = %s

            """,
            (farmerID,),
        )
        recipe = cursor.fetchall()
        cursor.close()

        if not recipe:
            return jsonify({"error": "No orders found"}), 404

        return jsonify(recipe), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@farmer_routes.route("/debug-test")
def debug_test():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT COUNT(*) AS n FROM Recipe;")
        result = cursor.fetchone()
        return {"recipe_count": result["n"]}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
@farmer_routes.route("/inventory", methods=["GET"])
def get_all_inventory():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM InventoryEntry;")
        rows = cursor.fetchall()
        cursor.close()

        return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500