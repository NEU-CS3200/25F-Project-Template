from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

students = Blueprint("students", __name__)

# Get all students with optional filtering
# Streamlit: Use requests.get('http://web-api:4000/students') to get all students
#            Add ?major_id=1&graduation_year=2025 for filtering
#            Display in a table or dropdown for selection
@students.route("/students", methods=["GET"])
def get_all_students():
    try:
        current_app.logger.info('Starting get_all_students request')
        cursor = db.get_db().cursor()
        
        # Get optional query parameters for filtering
        major_id = request.args.get("major_id")
        graduation_year = request.args.get("graduation_year")
        location_id = request.args.get("location_id")
        
        current_app.logger.debug(f'Query parameters - major_id: {major_id}, graduation_year: {graduation_year}, location_id: {location_id}')
        
        # Base query
        query = "SELECT * FROM student WHERE 1=1"
        params = []
        
        # Add filters if provided
        if major_id:
            query += " AND major_id = %s"
            params.append(major_id)
        if graduation_year:
            query += " AND graduation_year = %s"
            params.append(graduation_year)
        if location_id:
            query += " AND location_id = %s"
            params.append(location_id)
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        students = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(students)} students')
        return jsonify(students), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_students: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Get specific student by ID with major and location info
# Streamlit: Use requests.get(f'http://web-api:4000/students/{student_id}')
#            to get detailed info for a specific student
#            Display profile with st.write() or create a profile card
@students.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    try:
        current_app.logger.info('Starting get_student request')
        cursor = db.get_db().cursor()

        query = "SELECT s.*, m.major_name, l.city, l.state, l.country FROM student s LEFT JOIN major m ON s.major_id = m.major_id LEFT JOIN location l ON s.location_id = l.location_id WHERE s.student_id = %s"  # Changed to LEFT JOIN and s.student_id
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        cursor.close()

        current_app.logger.info("Successfully retrieved student")
        return jsonify(student), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_student: {str(e)}')  # Changed from get_all_students
        return jsonify({"error": str(e)}), 500
    
    
# Create a new student
# Streamlit: Use st.form() to collect input, then:
#            requests.post('http://web-api:4000/students', json={
#                "name": name, "email": email, "major_id": major_id, ...
#            })
#            Show success message with st.success()
@students.route("/students", methods=["POST"])  # /students not /student
def create_student():
    try:
        data = request.get_json()
        
        # All fields required
        required_fields = ["name", "email", "major_id", "location_id", "graduation_year", "profile_summary"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO student (name, email, major_id, location_id, graduation_year, profile_summary)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["name"],
            data["email"],
            data["major_id"],
            data["location_id"],
            data["graduation_year"],
            data["profile_summary"]
        ))
        
        db.get_db().commit()
        new_student_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Student created successfully", "student_id": new_student_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Update student profile
# Streamlit: Use st.form() to collect updates, then:
#            requests.put(f'http://web-api:4000/students/{student_id}', json={
#                "profile_summary": new_summary, ...
#            })
#            Show success with st.success()
@students.route("/students/<int:student_id>", methods=["PUT"])  # /students not /student
def update_student(student_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if student exists
        cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404

        allowed_fields = ["name", "email", "major_id", "location_id", "graduation_year", "profile_summary"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(student_id)

        query = f"UPDATE student SET {', '.join(update_fields)} WHERE student_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Student updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Delete student
# Streamlit: Add a confirmation dialog, then:
#            requests.delete(f'http://web-api:4000/students/{student_id}')
#            Show success/error message
@students.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404
        
        query = "DELETE FROM student WHERE student_id = %s"
        cursor.execute(query, (student_id,))

        db.get_db().commit()
        cursor.close()
        return jsonify({"message": f"Student deleted succesfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    