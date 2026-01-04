from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

connections = Blueprint("connections", __name__)

# Get all connections with optional filtering by status, student, or alumni
# Streamlit: Use requests.get('http://web-api:4000/connections') to get all connections
#            Add ?status=pending&student_id=5 for filtering
#            Display in a table showing student-alumni pairs
@connections.route("/connections", methods=["GET"])
def get_all_connections():
    try:
        current_app.logger.info('Starting get_all_connections request')
        cursor = db.get_db().cursor()
        
        # Get optional query parameters for filtering
        status = request.args.get("status")
        student_id = request.args.get("student_id")
        alumni_id = request.args.get("alumni_id")
        
        current_app.logger.debug(f'Query parameters - status: {status}, student_id: {student_id}, alumni_id: {alumni_id}')
        
        # Base query
        query = "SELECT * FROM connection WHERE 1=1"
        params = []
        
        # Add filters if provided
        if status:
            query += " AND status = %s"
            params.append(status)
        if student_id:
            query += " AND student_id = %s"
            params.append(student_id)
        if alumni_id:
            query += " AND alumni_id = %s"
            params.append(alumni_id)
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        connections = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(connections)} connections')
        return jsonify(connections), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_connections: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific connection by ID with student and alumni details
# Streamlit: Use requests.get(f'http://web-api:4000/connections/{connection_id}')
#            Display connection details with student and alumni names
@connections.route("/connections/<int:connection_id>", methods=["GET"])
def get_connection(connection_id):
    try:
        current_app.logger.info('Starting get_connection request')
        cursor = db.get_db().cursor()

        query = """
            SELECT c.*, s.name as student_name, s.email as student_email,
                   a.name as alumni_name, a.email as alumni_email
            FROM connection c
            LEFT JOIN student s ON c.student_id = s.student_id
            LEFT JOIN alumni a ON c.alumni_id = a.alumni_id
            WHERE c.connection_id = %s
        """
        cursor.execute(query, (connection_id,))
        connection = cursor.fetchone()

        if not connection:
            return jsonify({"error": "Connection not found"}), 404
        
        cursor.close()

        current_app.logger.info("Successfully retrieved connection")
        return jsonify(connection), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_connection: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new connection request (student requests mentorship from alumni)
# Streamlit: Use st.form() to select alumni, then:
#            requests.post('http://web-api:4000/connections', json={
#                "student_id": student_id, "alumni_id": alumni_id
#            })
#            Show success message with st.success()
@connections.route("/connections", methods=["POST"])
def create_connection():
    try:
        data = request.get_json()
        
        # Required fields
        required_fields = ["student_id", "alumni_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO connection (student_id, alumni_id, status)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            data["student_id"],
            data["alumni_id"],
            data.get("status", "pending")
        ))
        
        db.get_db().commit()
        new_connection_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Connection request created successfully", "connection_id": new_connection_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update connection status (accept/decline mentorship request)
# Streamlit: Use buttons for Accept/Decline, then:
#            requests.put(f'http://web-api:4000/connections/{connection_id}', json={
#                "status": "accepted"
#            })
#            Show success with st.success()
@connections.route("/connections/<int:connection_id>", methods=["PUT"])
def update_connection(connection_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if connection exists
        cursor.execute("SELECT * FROM connection WHERE connection_id = %s", (connection_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Connection not found"}), 404

        # Only status can be updated
        allowed_fields = ["status"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(connection_id)

        query = f"UPDATE connection SET {', '.join(update_fields)} WHERE connection_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Connection updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete/remove connection
# Streamlit: Add a confirmation dialog, then:
#            requests.delete(f'http://web-api:4000/connections/{connection_id}')
#            Show success/error message
@connections.route("/connections/<int:connection_id>", methods=["DELETE"])
def delete_connection(connection_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM connection WHERE connection_id = %s", (connection_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Connection not found"}), 404
        
        cursor.execute("DELETE FROM connection WHERE connection_id = %s", (connection_id,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Connection deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500