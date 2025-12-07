from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)

from backend.db_connection import db

# Create a Blueprint for career_coach
career_coach = Blueprint("career_coach", __name__)

@career_coach.route("/career_coach/<int:coach_id>/active_students", methods=["GET"])
def get_active_students(coach_id):
    try:
        cursor = db.get_db().cursor()

        # Query to count Active Students
        cursor.execute("""
        SELECT COUNT(*) AS Active_Students
        FROM Student s
        JOIN CareerCoach cc ON s.coachID = cc.coachID
        WHERE cc.coachID = %s AND s.status = 'Active'
        """, (coach_id,))
        active_students = cursor.fetchall()
        cursor.close()

        # Return the result as a JSON response
        return jsonify(active_students), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@career_coach.route("/career_coach/<int:coach_id>/roles_secured", methods=["GET"])
def get_roles_secured(coach_id):
    try:
        cursor = db.get_db().cursor()

        # Query to count Roles Secured (Stage = 'Offered')
        cursor.execute("""
        SELECT COUNT(DISTINCT ja.studentID) AS Roles_Secured
        FROM JobApplication ja
        JOIN Student s ON ja.studentID = s.studentID
        JOIN CareerCoach cc ON s.coachID = cc.coachID
        WHERE cc.coachID = %s AND ja.stage = 'Offered'
        """, (coach_id,))
        roles_secured = cursor.fetchall()
        cursor.close()

        # Return the result as a JSON response
        return jsonify(roles_secured), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@career_coach.route("/career_coach/<int:coach_id>/in_progress", methods=["GET"])
def get_in_progress(coach_id):
    try:
        cursor = db.get_db().cursor()

        # Query to count In Progress (Stage = 'Applied' or 'Interviewing')
        cursor.execute("""
        SELECT COUNT(DISTINCT ja.studentID) AS In_Progress
        FROM JobApplication ja
        JOIN Student s ON ja.studentID = s.studentID
        JOIN CareerCoach cc ON s.coachID = cc.coachID
        WHERE cc.coachID = %s AND ja.stage IN ('Applied', 'Interviewing')
        """, (coach_id,))
        in_progress = cursor.fetchall()
        cursor.close()

        # Return the result as a JSON response
        return jsonify(in_progress), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# # Get all student metrics
# @career_coach.route("/career_coach/<int:coach_id>/metrics", methods=["GET"])
# def get_coach_metrics(coach_id):
#     try:
#         cursor = db.get_db().cursor()

#         # Query to count Active Students
#         cursor.execute("""
#         SELECT COUNT(*) AS Active_Students
#         FROM Student s
#         JOIN CareerCoach cc ON s.coachID = cc.coachID
#         WHERE cc.coachID = %s AND s.status = 'Active'
#         """, (coach_id,))
#         active_students = cursor.fetchone()

#         # Query to count Roles Secured (Stage = 'Offered')
#         cursor.execute("""
#         SELECT COUNT(DISTINCT ja.studentID) AS Roles_Secured
#         FROM JobApplication ja
#         JOIN Student s ON ja.studentID = s.studentID
#         JOIN CareerCoach cc ON s.coachID = cc.coachID
#         WHERE cc.coachID = %s AND ja.stage = 'Offered'
#         """, (coach_id,))
#         roles_secured = cursor.fetchone()

#         # Query to count In Progress (Stage = 'Applied' or 'Interviewing')
#         cursor.execute("""
#         SELECT COUNT(DISTINCT ja.studentID) AS In_Progress
#         FROM JobApplication ja
#         JOIN Student s ON ja.studentID = s.studentID
#         JOIN CareerCoach cc ON s.coachID = cc.coachID
#         WHERE cc.coachID = %s AND ja.stage IN ('Applied', 'Interviewing')
#         """, (coach_id,))
#         in_progress = cursor.fetchone()

#         cursor.close()

#         # combine the results
#         metrics = {
#             "Active_Students": active_students[0],
#             "Roles_secured": roles_secured[0],
#             "In_Progress": in_progress[0],
#         }
#         return jsonify(metrics), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# Get all students for a specific career coach
@career_coach.route("/career_coach/<int:coach_id>/students", methods=["GET"])
def get_coach_students(coach_id):
    try:
        cursor = db.get_db().cursor()
        query = """
        SELECT 
            s.studentID AS Student_ID,
            s.firstName AS First_Name,
            s.lastName AS Last_Name,
            s.email AS Email
        FROM Student s
        JOIN CareerCoach cc ON s.coachID = cc.coachID
        WHERE cc.coachID = %s
        """
        cursor.execute(query, (coach_id,))
        students = cursor.fetchall()
        cursor.close()

        return jsonify(students), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@career_coach.route("/career_coach/all", methods=["GET"])
def get_all_coaches():
    try:
        cursor = db.get_db().cursor()

        # Query to get all coaches with their details
        cursor.execute("""
        SELECT 
            coachID, firstName, lastName, email
        FROM CareerCoach
        """)

        coaches = cursor.fetchall()
        cursor.close()

        # Check if coaches are found
        if coaches:
            # Return the list of coaches as JSON
            return jsonify(coaches), 200
        else:
            return jsonify({"message": "No coaches found."}), 404

    except Exception as e:
        # Return an error message if the query fails
        return jsonify({"error": str(e)}), 500
