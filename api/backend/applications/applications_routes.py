from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

applications = Blueprint("applications", __name__)

# Get all applications with optional filtering by status
# Streamlit: Use requests.get('http://web-api:4000/applications') to get all applications
#            Add ?status=pending for filtering
#            Display in a table for admin review
@applications.route("/applications", methods=["GET"])
def get_all_applications():
    try:
        current_app.logger.info('Starting get_all_applications request')
        cursor = db.get_db().cursor()
        
        # Get optional query parameter for filtering
        status = request.args.get("status")
        
        current_app.logger.debug(f'Query parameter - status: {status}')
        
        # Base query
        query = "SELECT * FROM application WHERE 1=1"
        params = []
        
        # Add filter if provided
        if status:
            query += " AND status = %s"
            params.append(status)
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        applications = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(applications)} applications')
        return jsonify(applications), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_applications: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific application by ID
# Streamlit: Use requests.get(f'http://web-api:4000/applications/{application_id}')
#            Display application details for admin review
@applications.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):
    try:
        current_app.logger.info('Starting get_application request')
        cursor = db.get_db().cursor()

        query = """
            SELECT ap.*, s.name as student_name, s.email as student_email
            FROM application ap
            LEFT JOIN student s ON ap.student_id = s.student_id
            WHERE ap.application_id = %s
        """
        cursor.execute(query, (application_id,))
        application = cursor.fetchone()

        if not application:
            return jsonify({"error": "Application not found"}), 404
        
        cursor.close()

        current_app.logger.info("Successfully retrieved application")
        return jsonify(application), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_application: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Submit new student application
# Streamlit: Use st.form() to collect student info, then:
#            requests.post('http://web-api:4000/applications', json={
#                "student_id": student_id
#            })
#            Show success message with st.success()
@applications.route("/applications", methods=["POST"])
def create_application():
    try:
        data = request.get_json()
        
        # Required field
        required_fields = ["student_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO application (student_id, status, admin_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            data["student_id"],
            data.get("status", "pending"),
            data.get("admin_id")
        ))
        
        db.get_db().commit()
        new_application_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Application submitted successfully", "application_id": new_application_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update application status (approve/decline)
# Streamlit: Use buttons for Approve/Decline, then:
#            requests.put(f'http://web-api:4000/applications/{application_id}', json={
#                "status": "approved", "admin_id": admin_id
#            })
#            Show success with st.success()
@applications.route("/applications/<int:application_id>", methods=["PUT"])
def update_application(application_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if application exists
        cursor.execute("SELECT * FROM application WHERE application_id = %s", (application_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Application not found"}), 404

        # Build dynamic update query
        allowed_fields = ["status", "admin_id"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(application_id)

        query = f"UPDATE application SET {', '.join(update_fields)} WHERE application_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Application updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500