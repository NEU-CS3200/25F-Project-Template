from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create a blueprint for trainer logs
trainer_logs = Blueprint("trainer_logs", __name__, url_prefix="/trainer/logs")

# FOR THE CLIENT LOGS
# GET all logs where completion_status = completed
@trainer_logs.route("/client-logs/completed", methods=["GET"])
def get_completed_logs():
    try:
        cursor = db.get_db().cursor(dictionary=True)
        cursor.execute("""
            SELECT cwl.*, c.first_name, c.last_name
            FROM Client_Workout_Log cwl
            JOIN Client c ON cwl.client_id = c.client_id
            WHERE completion_status = 'completed'
        """)
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# GET the percent of completed workouts (completed / total)
# GET the PR record for a client 
@trainer_logs.route("/clients/<int:client_id>/progress", methods=["GET"])
def get_client_progress(client_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        # Completion stats
        cursor.execute("""
            SELECT 
                COUNT(*) AS total,
                SUM(completion_status = 'completed') AS completed
            FROM Client_Workout_Log
            WHERE client_id = %s
        """, (client_id,))
        stats = cursor.fetchone()

        # PR records
        cursor.execute("""
            SELECT workout_date, PR
            FROM Client_Workout_Log
            WHERE client_id = %s AND PR IS NOT NULL
            ORDER BY workout_date DESC
        """, (client_id,))
        prs = cursor.fetchall()

        cursor.close()

        return jsonify({
            "total_sessions": stats["total"],
            "completed_sessions": stats["completed"],
            "consistency_rate": stats["completed"] / stats["total"] if stats["total"] > 0 else 0,
            "prs": prs
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500