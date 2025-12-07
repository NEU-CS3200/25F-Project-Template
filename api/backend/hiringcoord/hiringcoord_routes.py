from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error

# Create a Blueprint for hiring coordinator routes
hiring_coord = Blueprint("hiring_coord", __name__)


# Get all the job postings for a coordinator
@hiring_coord.route("/coordinator/<int:coordinator_id>/postings", methods=["GET"])
def get_coordinator_postings(coordinator_id):
    try:
        if not coordinator_id:
            return jsonify({"error": "Invalid coordinator ID"}), 400

        cursor = db.get_db().cursor()
        query = """
        SELECT
            jp.postingID,
            jp.title,
            jp.roleType,
            jp.location,
            jp.department,
            jp.status,
            jp.datePosted,
            jp.dateClosed,
            COUNT(DISTINCT ja.applicationID) AS totalApplicants
        FROM JobPosting jp
        LEFT JOIN JobApplication ja ON jp.postingID = ja.postingID
        WHERE jp.coordinatorID = %s
        GROUP BY jp.postingID, jp.title, jp.roleType, jp.location, 
                 jp.department, jp.status, jp.datePosted, jp.dateClosed
        ORDER BY jp.datePosted DESC
        """
        cursor.execute(query, (coordinator_id,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return jsonify({"message": "Postings not found for this coordinator"}), 404

        return jsonify(result), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Create a new job posting
@hiring_coord.route("/coordinator/<int:coordinator_id>/postings", methods=["POST"])
def create_job_posting(coordinator_id):
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['title', 'roleType', 'location', 'department']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()
        query = """
        INSERT INTO JobPosting (
            title,
            roleType,
            location,
            department,
            status,
            datePosted,
            coordinatorID
        )
        VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """
        cursor.execute(query, (
            data['title'],
            data['roleType'],
            data['location'],
            data['department'],
            data.get('status', 'Open'),
            coordinator_id
        ))
        db.get_db().commit()
        posting_id = cursor.lastrowid
        cursor.close()

        if not posting_id:
            return jsonify({"message": "Job posting creation failed"}), 404

        return jsonify({
            "message": "Job posting has been created successfully",
            "postingID": posting_id
        }), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update Job Postings
@hiring_coord.route("/postings/<int:posting_id>/status", methods=["PUT"])
def update_posting_status(posting_id):
    try:
        data = request.get_json()

        if 'status' not in data:
            return jsonify({"error": "Missing 'status' field"}), 400

        cursor = db.get_db().cursor()

        # Depending on if status is closed, cater queries
        if data['status'] == 'Closed':
            query = """
            UPDATE JobPosting
            SET status = %s, dateClosed = NOW()
            WHERE postingID = %s
            """
        else:
            query = """
            UPDATE JobPosting
            SET status = %s
            WHERE postingID = %s
            """

        cursor.execute(query, (data['status'], posting_id))
        db.get_db().commit()
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected == 0:
            return jsonify({"message": "Posting not found"}), 404

        return jsonify({
            "message": "Status of posting has been updated successfully",
            "postingID": posting_id,
            "newStatus": data['status']
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get the platform analytics
@hiring_coord.route("/coordinator/<int:coordinator_id>/platform-analytics", methods=["GET"])
def get_platform_analytics(coordinator_id):
    try:
        cursor = db.get_db().cursor()
        query = """
        SELECT
            p.name AS platformName,
            p.platformID,
            COUNT(DISTINCT ja.applicationID) AS totalApplicants,
            COUNT(DISTINCT CASE WHEN ja.stage = 'Hired' THEN ja.applicationID END) AS totalHires,
            ROUND(COUNT(DISTINCT CASE WHEN ja.stage = 'Hired' THEN ja.applicationID END) * 100.0 / 
                  NULLIF(COUNT(DISTINCT ja.applicationID), 0), 2) AS hireRate
        FROM Platform p
        JOIN JobListing jl ON p.platformID = jl.platformID
        JOIN JobPosting jp ON jl.postingID = jp.postingID
        LEFT JOIN JobApplication ja ON jl.listingID = ja.listingID
        WHERE jp.coordinatorID = %s
        GROUP BY p.platformID, p.name
        ORDER BY totalHires DESC
        """
        cursor.execute(query, (coordinator_id,))
        result = cursor.fetchall()
        cursor.close()

        return jsonify(result), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get the expiring listing notifications
@hiring_coord.route("/coordinator/<int:coordinator_id>/expiring-listings", methods=["GET"])
def get_expiring_listings(coordinator_id):
    try:
        # Find the days parameter (defaulted at 7 days)
        days = request.args.get('days', 7, type=int)

        cursor = db.get_db().cursor()
        query = """
        SELECT
            jl.listingID,
            jp.postingID,
            jp.title,
            p.name AS platformName,
            jl.expiresOn,
            jl.listingStatus,
            DATEDIFF(jl.expiresOn, NOW()) AS daysUntilExpiry
        FROM JobListing jl
        JOIN JobPosting jp ON jl.postingID = jp.postingID
        JOIN Platform p ON jl.platformID = p.platformID
        WHERE jp.coordinatorID = %s
          AND jl.listingStatus = 'Active'
          AND jl.expiresOn IS NOT NULL
          AND jl.expiresOn <= DATE_ADD(NOW(), INTERVAL %s DAY)
        ORDER BY jl.expiresOn ASC
        """
        cursor.execute(query, (coordinator_id, days))
        result = cursor.fetchall()
        cursor.close()

        return jsonify(result), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete a job posting
@hiring_coord.route("/postings/<int:posting_id>", methods=["DELETE"])
def delete_job_posting(posting_id):
    try:
        cursor = db.get_db().cursor()
        query = """
        DELETE FROM JobPosting
        WHERE postingID = %s
        """
        cursor.execute(query, (posting_id,))
        db.get_db().commit()
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected == 0:
            return jsonify({"message": "Posting not found"}), 404

        return jsonify({
            "message": "Job posting has been deleted successfully",
            "postingID": posting_id
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500