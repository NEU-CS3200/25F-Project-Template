from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

job_postings = Blueprint("job_postings", __name__)

# Get all job postings with optional filtering
# Streamlit: Use requests.get('http://web-api:4000/job-postings')
#            Add ?preferred_major=Computer Science for filtering
#            Display job board for students
@job_postings.route("/job-postings", methods=["GET"])
def get_all_job_postings():
    try:
        current_app.logger.info('Starting get_all_job_postings request')
        cursor = db.get_db().cursor()
        
        # Get optional query parameters for filtering
        preferred_major = request.args.get("preferred_major")
        status = request.args.get("status")
        alumni_id = request.args.get("alumni_id")
        
        current_app.logger.debug(f'Query parameters - preferred_major: {preferred_major}, status: {status}, alumni_id: {alumni_id}')
        
        # Base query
        query = "SELECT * FROM job_posting WHERE 1=1"
        params = []
        
        # Add filters if provided
        if preferred_major:
            query += " AND preferred_major = %s"
            params.append(preferred_major)
        if status:
            query += " AND status = %s"
            params.append(status)
        if alumni_id:
            query += " AND alumni_id = %s"
            params.append(alumni_id)
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        job_postings = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(job_postings)} job postings')
        return jsonify(job_postings), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_job_postings: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific job posting by ID
# Streamlit: Use requests.get(f'http://web-api:4000/job-postings/{posting_id}')
#            Display full job posting details with alumni info
@job_postings.route("/job-postings/<int:posting_id>", methods=["GET"])
def get_job_posting(posting_id):
    try:
        current_app.logger.info('Starting get_job_posting request')
        cursor = db.get_db().cursor()

        query = """
            SELECT jp.*, a.name as alumni_name, a.email as alumni_email, 
                   a.current_role, c.company_name
            FROM job_posting jp
            LEFT JOIN alumni a ON jp.alumni_id = a.alumni_id
            LEFT JOIN company c ON a.company_id = c.company_id
            WHERE jp.posting_id = %s
        """
        cursor.execute(query, (posting_id,))
        job_posting = cursor.fetchone()

        if not job_posting:
            return jsonify({"error": "Job posting not found"}), 404
        
        cursor.close()

        current_app.logger.info("Successfully retrieved job posting")
        return jsonify(job_posting), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_job_posting: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create new job posting
# Streamlit: Use st.form() to create posting, then:
#            requests.post('http://web-api:4000/job-postings', json={
#                "alumni_id": alumni_id, "title": "Software Engineer Intern",
#                "description": "Looking for...", "preferred_major": "Computer Science"
#            })
@job_postings.route("/job-postings", methods=["POST"])
def create_job_posting():
    try:
        data = request.get_json()
        
        # Required fields
        required_fields = ["alumni_id", "title", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO job_posting (alumni_id, title, description, preferred_major, preferred_year, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["alumni_id"],
            data["title"],
            data["description"],
            data.get("preferred_major"),
            data.get("preferred_year"),
            data.get("status", "active")
        ))
        
        db.get_db().commit()
        new_posting_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Job posting created successfully", "posting_id": new_posting_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update job posting
# Streamlit: Use st.form() to edit posting, then:
#            requests.put(f'http://web-api:4000/job-postings/{posting_id}', json={
#                "status": "closed"
#            })
@job_postings.route("/job-postings/<int:posting_id>", methods=["PUT"])
def update_job_posting(posting_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if job posting exists
        cursor.execute("SELECT * FROM job_posting WHERE posting_id = %s", (posting_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Job posting not found"}), 404

        # Build dynamic update query
        allowed_fields = ["title", "description", "preferred_major", "preferred_year", "status"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(posting_id)

        query = f"UPDATE job_posting SET {', '.join(update_fields)} WHERE posting_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Job posting updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete job posting
# Streamlit: Add confirmation, then:
#            requests.delete(f'http://web-api:4000/job-postings/{posting_id}')
@job_postings.route("/job-postings/<int:posting_id>", methods=["DELETE"])
def delete_job_posting(posting_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM job_posting WHERE posting_id = %s", (posting_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Job posting not found"}), 404
        
        cursor.execute("DELETE FROM job_posting WHERE posting_id = %s", (posting_id,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Job posting deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500