from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from datetime import datetime

# Create a Blueprint for applications
applications = Blueprint("applications", __name__)

# Get all applications for a specific student
@applications.route("/applications/<int:student_id>", methods=["GET"])
def get_student_applications(student_id):
    try:
        cursor = db.get_db().cursor()
        query = """
        SELECT 
            ja.dateApplied AS Date_Applied,
            ja.companyName AS Company, 
            ja.position AS Position,
            ja.stage AS Status, 
            r.label AS Resume_Used, 
            COALESCE(ja.jobBoard, p.name, 'Manual Add') AS Job_Board, 
            COALESCE(jl.postingURL, '') AS App_Portal
        FROM JobApplication ja
        JOIN Resume r ON ja.resumeID = r.resumeID AND ja.studentID = r.studentID
        LEFT JOIN JobListing jl ON ja.listingID = jl.listingID AND ja.postingID = jl.postingID
        LEFT JOIN Platform p ON jl.platformID = p.platformID
        WHERE ja.studentID = %s
        """
        cursor.execute(query, (student_id,))
        column_names = [i[0] for i in cursor.description]
        apps = cursor.fetchall()
        cursor.close()

        return jsonify(apps), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Add a new job application for a specific student
@applications.route("/applications/<int:student_id>", methods=["POST"])
def add_application(student_id):
    try:
        data = request.get_json()
        
        company = data.get('company')
        position = data.get('position')
        stage = data.get('stage')
        date_applied = data.get('date_applied')
        resume_id = data.get('resume_id')
        job_board_name = data.get('job_board')
        
        if not company or not position or not stage:
             return jsonify({"error": "Missing required fields"}), 400

        cursor = db.get_db().cursor()

        cursor.execute("SELECT platformID FROM Platform WHERE name = %s", (job_board_name,))
        row = cursor.fetchone()
        
        if row:
            platform_id = row['platformID']
        else:
            cursor.execute("INSERT INTO Platform (name, platformType, baseURL) VALUES (%s, 'Manual', '#')", (job_board_name,))
            platform_id = cursor.lastrowid

        cursor.execute("SELECT coordinatorID FROM HiringCoordinator WHERE companyName = %s", (company,))
        row = cursor.fetchone()
        
        if row:
            coordinator_id = row['coordinatorID']
        else:
            dummy_email = f"hiring@{company.replace(' ', '').lower()}.com"
            cursor.execute("""
                INSERT INTO HiringCoordinator (fName, lName, email, companyName)
                VALUES ('Manual', 'Entry', %s, %s)
            """, (dummy_email, company))
            coordinator_id = cursor.lastrowid

        cursor.execute("""
            SELECT postingID FROM JobPosting 
            WHERE title = %s AND coordinatorID = %s
        """, (position, coordinator_id))
        row = cursor.fetchone()
        
        if row:
            posting_id = row['postingID']
        else:
            # Create new Posting
            cursor.execute("""
                INSERT INTO JobPosting (title, roleType, location, department, datePosted, coordinatorID)
                VALUES (%s, %s, 'Unknown', 'Unknown', %s, %s)
            """, (position, position, date_applied, coordinator_id))
            posting_id = cursor.lastrowid

        cursor.execute("""
            SELECT listingID FROM JobListing 
            WHERE postingID = %s AND platformID = %s
        """, (posting_id, platform_id))
        row = cursor.fetchone()
        
        if row:
            listing_id = row['listingID']
        else:
            cursor.execute("SELECT MAX(listingID) as max_l FROM JobListing")
            res = cursor.fetchone()
            new_listing_id = (res['max_l'] + 1) if (res and res['max_l']) else 100000
            
            cursor.execute("""
                INSERT INTO JobListing (listingID, postingID, platformID, listingStatus, datePublished, postingURL)
                VALUES (%s, %s, %s, 'Active', %s, '#')
            """, (new_listing_id, posting_id, platform_id, date_applied))
            listing_id = new_listing_id

        cursor.execute("SELECT MAX(applicationID) AS max_id FROM JobApplication")
        row = cursor.fetchone()
        new_app_id = (row['max_id'] if row and row['max_id'] else 0) + 1
        
        query = """
        INSERT INTO JobApplication 
        (
            applicationID, studentID, companyName, position, stage, jobBoard,
            dateApplied, lastUpdated, resumeID, listingID, postingID
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            new_app_id, student_id, company, position, stage, job_board_name,
            date_applied, datetime.now(), resume_id, listing_id, posting_id
        ))
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Application linked and added!", "appID": new_app_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500