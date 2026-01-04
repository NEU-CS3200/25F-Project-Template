from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

alumni = Blueprint("alumni", __name__)

# Get all alumni with optional filtering by field
# Streamlit: Use requests.get('http://web-api:4000/alumni') to get all alumni
#            Add ?field=Technology for filtering
#            Display in a table or dropdown for selection
@alumni.route("/alumni", methods=["GET"])
def get_all_alumni():
    try:
        current_app.logger.info('Starting get_all_alumni request')
        cursor = db.get_db().cursor()
        
        # Get optional query parameters for filtering
        field = request.args.get("field")
        graduation_year = request.args.get("graduation_year")
        location_id = request.args.get("location_id")
        
        current_app.logger.debug(f'Query parameters - field: {field}, graduation_year: {graduation_year}, location_id: {location_id}')
        
        # Base query
        query = "SELECT * FROM alumni WHERE 1=1"
        params = []
        
        # Add filters if provided
        if field:
            query += " AND field = %s"
            params.append(field)
        if graduation_year:
            query += " AND graduation_year = %s"
            params.append(graduation_year)
        if location_id:
            query += " AND location_id = %s"
            params.append(location_id)
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        alumni_list = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(alumni_list)} alumni')
        return jsonify(alumni_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_alumni: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific alumni by ID with company and location info
# Streamlit: Use requests.get(f'http://web-api:4000/alumni/{alumni_id}')
#            to get detailed info including bio, experience
#            Display profile with company and location details
@alumni.route("/alumni/<int:alumni_id>", methods=["GET"])
def get_alumni(alumni_id):
    try:
        current_app.logger.info('Starting get_alumni request')
        cursor = db.get_db().cursor()

        query = """
            SELECT a.*, c.company_name, c.industry, l.city, l.state, l.country
            FROM alumni a
            LEFT JOIN company c ON a.company_id = c.company_id
            LEFT JOIN location l ON a.location_id = l.location_id
            WHERE a.alumni_id = %s
        """
        cursor.execute(query, (alumni_id,))
        alumni = cursor.fetchone()

        if not alumni:
            return jsonify({"error": "Alumni not found"}), 404
        
        cursor.close()

        current_app.logger.info("Successfully retrieved alumni")
        return jsonify(alumni), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_alumni: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new alumni profile
# Streamlit: Use st.form() to collect input, then:
#            requests.post('http://web-api:4000/alumni', json={
#                "name": name, "email": email, "field": field, ...
#            })
#            Show success message with st.success()
@alumni.route("/alumni", methods=["POST"])
def create_alumni():
    try:
        data = request.get_json()
        
        # All fields required
        required_fields = ["name", "email", "graduation_year", "current_role", "company_id", "field", "bio", "location_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["name"],
            data["email"],
            data["graduation_year"],
            data["current_role"],
            data["company_id"],
            data["field"],
            data["bio"],
            data["location_id"],
            data.get("availability_status", "available")
        ))
        
        db.get_db().commit()
        new_alumni_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Alumni created successfully", "alumni_id": new_alumni_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update alumni profile (role, company, field, bio)
# Streamlit: Use st.form() to collect updates, then:
#            requests.put(f'http://web-api:4000/alumni/{alumni_id}', json={
#                "current_role": new_role, "bio": updated_bio, ...
#            })
#            Show success with st.success()
@alumni.route("/alumni/<int:alumni_id>", methods=["PUT"])
def update_alumni(alumni_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if alumni exists
        cursor.execute("SELECT * FROM alumni WHERE alumni_id = %s", (alumni_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Alumni not found"}), 404

        # Build dynamic update query
        allowed_fields = ["name", "email", "graduation_year", "current_role", "company_id", "field", "bio", "location_id", "availability_status"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(alumni_id)

        query = f"UPDATE alumni SET {', '.join(update_fields)} WHERE alumni_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Alumni updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete alumni account
# Streamlit: Add a confirmation dialog, then:
#            requests.delete(f'http://web-api:4000/alumni/{alumni_id}')
#            Show success/error message
@alumni.route("/alumni/<int:alumni_id>", methods=["DELETE"])
def delete_alumni(alumni_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM alumni WHERE alumni_id = %s", (alumni_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Alumni not found"}), 404
        
        cursor.execute("DELETE FROM alumni WHERE alumni_id = %s", (alumni_id,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Alumni deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get alumni availability schedule
# Streamlit: Use requests.get(f'http://web-api:4000/alumni/{alumni_id}/availability')
#            Display schedule in a calendar or table format
@alumni.route("/alumni/<int:alumni_id>/availability", methods=["GET"])
def get_alumni_availability(alumni_id):
    try:
        cursor = db.get_db().cursor()

        # Check if alumni exists
        cursor.execute("SELECT * FROM alumni WHERE alumni_id = %s", (alumni_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Alumni not found"}), 404

        # Get availability schedule
        cursor.execute("SELECT * FROM availability_schedule WHERE alumni_id = %s", (alumni_id,))
        schedule = cursor.fetchall()
        cursor.close()

        return jsonify(schedule), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Create new availability slots for alumni
# Streamlit: Use st.form() with day/time selectors, then:
#            requests.post(f'http://web-api:4000/alumni/{alumni_id}/availability', json={
#                "day_of_week": "Monday", "start_time": "09:00", "end_time": "12:00"
#            })
@alumni.route("/alumni/<int:alumni_id>/availability", methods=["POST"])
def create_availability(alumni_id):
    try:
        data = request.get_json()
        
        required_fields = ["day_of_week", "start_time", "end_time"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        # Check if alumni exists
        cursor.execute("SELECT * FROM alumni WHERE alumni_id = %s", (alumni_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Alumni not found"}), 404
        
        query = """
        INSERT INTO availability_schedule (alumni_id, day_of_week, start_time, end_time)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (alumni_id, data["day_of_week"], data["start_time"], data["end_time"]))
        
        db.get_db().commit()
        new_schedule_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Availability created successfully", "schedule_id": new_schedule_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update availability slots
# Streamlit: requests.put(f'http://web-api:4000/alumni/{alumni_id}/availability/{schedule_id}', json=...)
@alumni.route("/alumni/<int:alumni_id>/availability/<int:schedule_id>", methods=["PUT"])
def update_availability(alumni_id, schedule_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if schedule exists for this alumni
        cursor.execute("SELECT * FROM availability_schedule WHERE schedule_id = %s AND alumni_id = %s", (schedule_id, alumni_id))
        if not cursor.fetchone():
            return jsonify({"error": "Availability schedule not found"}), 404

        allowed_fields = ["day_of_week", "start_time", "end_time"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(schedule_id)

        query = f"UPDATE availability_schedule SET {', '.join(update_fields)} WHERE schedule_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Availability updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete availability slots
# Streamlit: requests.delete(f'http://web-api:4000/alumni/{alumni_id}/availability/{schedule_id}')
@alumni.route("/alumni/<int:alumni_id>/availability/<int:schedule_id>", methods=["DELETE"])
def delete_availability(alumni_id, schedule_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM availability_schedule WHERE schedule_id = %s AND alumni_id = %s", (schedule_id, alumni_id))
        if not cursor.fetchone():
            return jsonify({"error": "Availability schedule not found"}), 404
        
        cursor.execute("DELETE FROM availability_schedule WHERE schedule_id = %s", (schedule_id,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Availability deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500