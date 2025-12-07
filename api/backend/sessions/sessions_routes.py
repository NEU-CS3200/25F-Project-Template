from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

sessions = Blueprint("sessions", __name__)

# Get all sessions with optional filtering by date, student, or alumni
# Streamlit: Use requests.get('http://web-api:4000/sessions') to get all sessions
#            Add ?student_id=5&status=scheduled for filtering
#            Display in a calendar or table format
@sessions.route("/sessions", methods=["GET"])
def get_all_sessions():
    try:
        current_app.logger.info('Starting get_all_sessions request')
        cursor = db.get_db().cursor()
        
        # Get optional query parameters for filtering
        student_id = request.args.get("student_id")
        alumni_id = request.args.get("alumni_id")
        status = request.args.get("status")
        session_date = request.args.get("session_date")
        
        current_app.logger.debug(f'Query parameters - student_id: {student_id}, alumni_id: {alumni_id}, status: {status}, session_date: {session_date}')
        
        # Base query
        query = "SELECT * FROM session WHERE 1=1"
        params = []
        
        # Add filters if provided
        if student_id:
            query += " AND student_id = %s"
            params.append(student_id)
        if alumni_id:
            query += " AND alumni_id = %s"
            params.append(alumni_id)
        if status:
            query += " AND status = %s"
            params.append(status)
        if session_date:
            query += " AND session_date = %s"
            params.append(session_date)
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        sessions = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(sessions)} sessions')
        return jsonify(sessions), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_sessions: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific session by ID with details and notes
# Streamlit: Use requests.get(f'http://web-api:4000/sessions/{session_id}')
#            Display session details with student/alumni info
#            Show notes in a text area
@sessions.route("/sessions/<int:session_id>", methods=["GET"])
def get_session(session_id):
    try:
        current_app.logger.info('Starting get_session request')
        cursor = db.get_db().cursor()

        query = """
            SELECT s.*, st.name as student_name, a.name as alumni_name
            FROM session s
            LEFT JOIN student st ON s.student_id = st.student_id
            LEFT JOIN alumni a ON s.alumni_id = a.alumni_id
            WHERE s.session_id = %s
        """
        cursor.execute(query, (session_id,))
        session = cursor.fetchone()

        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        cursor.close()

        current_app.logger.info("Successfully retrieved session")
        return jsonify(session), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_session: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new mentorship session
# Streamlit: Use st.form() with date/time pickers, then:
#            requests.post('http://web-api:4000/sessions', json={
#                "student_id": student_id, "alumni_id": alumni_id,
#                "session_date": "2025-12-10", "session_time": "14:00",
#                "topic": "Career advice"
#            })
#            Show success message with st.success()
@sessions.route("/sessions", methods=["POST"])
def create_session():
    try:
        data = request.get_json()
        
        # Required fields
        required_fields = ["student_id", "alumni_id", "session_date"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO session (student_id, alumni_id, session_date, session_time, topic, notes, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["student_id"],
            data["alumni_id"],
            data["session_date"],
            data.get("session_time"),
            data.get("topic"),
            data.get("notes"),
            data.get("status", "scheduled")
        ))
        
        db.get_db().commit()
        new_session_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Session created successfully", "session_id": new_session_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update session (notes, status, topic)
# Streamlit: Use st.form() to collect updates (notes after meeting), then:
#            requests.put(f'http://web-api:4000/sessions/{session_id}', json={
#                "notes": "Discussed internship opportunities...",
#                "status": "completed"
#            })
#            Show success with st.success()
@sessions.route("/sessions/<int:session_id>", methods=["PUT"])
def update_session(session_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if session exists
        cursor.execute("SELECT * FROM session WHERE session_id = %s", (session_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Session not found"}), 404

        # Build dynamic update query
        allowed_fields = ["session_date", "session_time", "topic", "notes", "status"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(session_id)

        query = f"UPDATE session SET {', '.join(update_fields)} WHERE session_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Session updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Cancel/delete session
# Streamlit: Add a confirmation dialog, then:
#            requests.delete(f'http://web-api:4000/sessions/{session_id}')
#            Show success/error message
@sessions.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM session WHERE session_id = %s", (session_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Session not found"}), 404
        
        cursor.execute("DELETE FROM session WHERE session_id = %s", (session_id,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Session deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500