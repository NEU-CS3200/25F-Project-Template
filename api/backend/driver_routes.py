from flask import Blueprint, jsonify, request
from backend.db_connection import db

# Blueprint for driver-facing routes
driver_routes = Blueprint("driver_routes", __name__)

# Return all scheduled deliveries for driver
@driver_routes.route("/driver/<int:driverID>/order", methods=["GET"])
def get_all_deliveries(driverID):
    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            """
            SELECT orderID, orderDate, scheduledTime, deliveryAddress, status, quantityOrdered, DriverID, customerID
            FROM Orders 
            WHERE DriverID = %s
            ORDER BY CASE status
                WHEN 'out_for_delivery' THEN 1
                WHEN 'confirmed' THEN 2
                WHEN 'preparing' THEN 3
                WHEN 'pending' THEN 4
                ELSE 5
            END, scheduledTime
            """,
            (driverID,),
        )
        rows = cursor.fetchall()
        cursor.close()

        # Convert dict rows to JSON-serializable format (dates need string conversion)
        result = []
        for row in rows:
            result.append({
                'orderID': row['orderID'],
                'orderDate': str(row['orderDate']) if row['orderDate'] else None,
                'scheduledTime': str(row['scheduledTime']) if row['scheduledTime'] else None,
                'deliveryAddress': row['deliveryAddress'],
                'status': row['status'],
                'quantityOrdered': row['quantityOrdered'],
                'DriverID': row['DriverID'],
                'customerID': row['customerID']
            })

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Update driver order status 
@driver_routes.route("/driver/<int:driverID>/order/<int:orderID>", methods=["PUT"])
def update_order_status(driverID, orderID):
    try:
        data = request.get_json()

        allowed_fields = ["status"]
        update_fields = []
        params = []

        # Only allow updating a clear set of fields
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"`{field}` = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        # Make sure the order exists for this driver
        cursor.execute(
            "SELECT orderID FROM Orders WHERE DriverID = %s AND orderID = %s",
            (driverID, orderID,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Order not found for this driver"}), 404

        # Execute update
        params.append(driverID)
        params.append(orderID)
        query = f"UPDATE Orders SET {', '.join(update_fields)} WHERE DriverID = %s AND orderID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Order status updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#Log delivery issue 
@driver_routes.route("/driver/<int:orderID>/order/deliveryIssue", methods=["POST"])
def create_issue_report(orderID):
    try:
        data = request.get_json()

        required_fields = ["issueID", "timestamp", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO DeliveryIssue (issueID, timestamp, description, orderID)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                data["issueID"],
                data['timestamp'],
                data['description'], 
                orderID,
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Issure reported succesfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Conversation history between driver and admin 
@driver_routes.route("/driver/<int:driverID>/deliverymessage", methods=["GET"])
def get_message(driverID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT messageID, timestamp, content, DriverID
            FROM DeliveryMessage
            WHERE DriverID = %s
            ORDER BY timestamp ASC
            """,
            (driverID,),
        )
        rows = cursor.fetchall()
        cursor.close()

        # Convert to JSON-serializable format
        result = []
        for row in rows:
            result.append({
                'messageID': row['messageID'],
                'timestamp': str(row['timestamp']) if row['timestamp'] else None,
                'content': row['content'],
                'DriverID': row['DriverID']
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#Send message to admin  
@driver_routes.route("/driver/<int:driverID>/deliverymessage", methods=["POST"])
def send_message(driverID):
    try:
        data = request.get_json()

        required_fields = ["messageID", "timestamp", "content"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO DeliveryMessage (messageID, timestamp, content, driverID)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                data["messageID"],
                data['timestamp'],
                data['content'], 
                driverID,
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Message sent succesfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Driver availability
@driver_routes.route("/driver/<int:driverID>/driveravailability", methods=["GET"])
def get_availability(driverID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """SELECT availibilityID, availStartTime, availEndTime, date, isAvailable, DriverID
            FROM DriverAvailability
            WHERE DriverID = %s""",
            (driverID,),
            )
        rows = cursor.fetchall()
        cursor.close()

        # Convert timedelta and date objects to strings for JSON serialization
        result = []
        for row in rows:
            result.append({
                'availibilityID': row['availibilityID'],
                'availStartTime': str(row['availStartTime']) if row['availStartTime'] else None,
                'availEndTime': str(row['availEndTime']) if row['availEndTime'] else None,
                'date': str(row['date']) if row['date'] else None,
                'isAvailable': bool(row['isAvailable']),
                'DriverID': row['DriverID']
            })

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Update driver availability days (specific entry by availabilityID)
@driver_routes.route("/driver/<int:driverID>/driveravailability/<int:availabilityID>", methods=["PUT"])
def update_driver_availability(driverID, availabilityID):
    try:
        data = request.get_json()

        allowed_fields = ['availStartTime', 'availEndTime', 'date', 'isAvailable']
        update_fields = []
        params = []

        # Only allow updating specific fields
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        # Verify the entry exists and belongs to this driver
        cursor.execute(
            "SELECT availibilityID FROM DriverAvailability WHERE availibilityID = %s AND DriverID = %s",
            (availabilityID, driverID),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Availability entry not found"}), 404

        # Execute update
        params.append(availabilityID)
        params.append(driverID)
        query = f"UPDATE DriverAvailability SET {', '.join(update_fields)} WHERE availibilityID = %s AND DriverID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Availability updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Trafic for driver 
@driver_routes.route("/driver/<int:driverID>/traffic", methods=["GET"])
def get_driver_route(driverID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT locationID, timestamp, trafficLevels, notification, driverID
            FROM Traffic
            WHERE driverID = %s
            """,
            (driverID,),
        )
        traffic = cursor.fetchall()
        cursor.close()

        if not traffic:
            return jsonify({"error": "No traffic records found for this driver"}), 404

        return jsonify(traffic), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Post for adding availability to the database
@driver_routes.route("/driver/<int:driverID>/driveravailability", methods=["POST"])
def create_driver_availability(driverID):
    try:
        data = request.get_json()

        required_fields = ["date", "availStartTime", "availEndTime", "isAvailable"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT availibilityID FROM DriverAvailability WHERE `date` = %s AND DriverID = %s",
            (data["date"], driverID),
        )
        if cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Availability already exists for this date. Use PUT to update."}), 409

        query = """
            INSERT INTO DriverAvailability (availStartTime, availEndTime, `date`, isAvailable, DriverID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["availStartTime"],
                data["availEndTime"],
                data["date"],
                data["isAvailable"],
                driverID,
            ),
        )
        
        db.get_db().commit()
        new_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Availability created successfully", "availabilityID": new_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    