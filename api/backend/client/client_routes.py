from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Client routes
client = Blueprint('client', __name__)


# Route 1: GET all completed workout logs for client
@client.route("/client_workout_log", methods=["GET"])
def get_client_workout_logs():
    """Return all completed workout logs for the authenticated client (last 10)"""
    try:
        current_app.logger.info('Starting get_client_workout_logs request')
        
        client_id = request.args.get('client_id', type=int)
        
        if not client_id:
            return jsonify({"error": "client_id is required"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
            SELECT 
                cwl.log_id,
                cwl.workout_date,
                wst.name AS workout_name,
                cwl.completion_status,
                cwl.duration_minutes
            FROM Client_Workout_Log cwl
            JOIN Workout_Session_Template wst ON cwl.workout_id = wst.workout_id
            WHERE cwl.client_id = %s
              AND cwl.completion_status = 'completed'
            ORDER BY cwl.workout_date DESC
            LIMIT 10;
        """
        
        current_app.logger.debug(f'Executing query with client_id={client_id}')
        cursor.execute(query, (client_id,))
        logs = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(logs)} workout logs')
        return jsonify(logs), 200
        
    except Error as e:
        current_app.logger.error(f'Database error in get_client_workout_logs: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Route 2: POST - Create a new workout log
@client.route("/client_workout_log", methods=["POST"])
def create_workout_log():
    """Create a new workout log entry with date, duration, completion_status, and notes"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['client_id', 'workout_id', 'date', 'completion_status', 'duration_minutes']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
            INSERT INTO Client_Workout_Log 
            (client_id, workout_id, workout_date, completion_status, duration_minutes, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            data['client_id'],
            data['workout_id'],
            data['date'],
            data['completion_status'],
            data['duration_minutes'],
            data.get('notes', '')
        ))
        
        db.get_db().commit()
        log_id = cursor.lastrowid
        cursor.close()
        
        current_app.logger.info(f'Successfully created workout log {log_id}')
        return jsonify({"message": "Workout log created successfully", "log_id": log_id}), 201
        
    except Error as e:
        current_app.logger.error(f'Database error in create_workout_log: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Route 3: PUT - Update a workout log's duration or notes
@client.route("/client_workout_log/<int:log_id>", methods=["PUT"])
def update_workout_log(log_id):
    """Update a workout log's duration or notes"""
    try:
        data = request.get_json()
        
        # Build dynamic update query
        update_fields = []
        values = []
        
        if 'duration_minutes' in data:
            update_fields.append("duration_minutes = %s")
            values.append(data['duration_minutes'])
        
        if 'notes' in data:
            update_fields.append("notes = %s")
            values.append(data['notes'])
        
        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400
        
        values.append(log_id)
        
        cursor = db.get_db().cursor()
        
        query = f"""
            UPDATE Client_Workout_Log
            SET {', '.join(update_fields)}
            WHERE log_id = %s
        """
        
        cursor.execute(query, values)
        db.get_db().commit()
        
        rows_affected = cursor.rowcount
        cursor.close()
        
        if rows_affected == 0:
            return jsonify({"error": "Workout log not found"}), 404
        
        current_app.logger.info(f'Successfully updated workout log {log_id}')
        return jsonify({"message": "Workout log updated successfully"}), 200
        
    except Error as e:
        current_app.logger.error(f'Database error in update_workout_log: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Route 4: DELETE - Delete incomplete workout logs
@client.route("/client_workout_log", methods=["DELETE"])
def delete_incomplete_logs():
    """Delete incomplete workout logs where completion_status = 'not_started'"""
    try:
        client_id = request.args.get('client_id', type=int)
        
        if not client_id:
            return jsonify({"error": "client_id is required"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
            DELETE FROM Client_Workout_Log
            WHERE client_id = %s
              AND completion_status = 'not_started'
        """
        
        cursor.execute(query, (client_id,))
        db.get_db().commit()
        
        rows_deleted = cursor.rowcount
        cursor.close()
        
        current_app.logger.info(f'Successfully deleted {rows_deleted} incomplete logs')
        return jsonify({
            "message": f"Deleted {rows_deleted} incomplete workout logs",
            "rows_deleted": rows_deleted
        }), 200
        
    except Error as e:
        current_app.logger.error(f'Database error in delete_incomplete_logs: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Route 5: GET - Monthly completion rate comparison
@client.route("/client_workout_log/completion_rate/monthly", methods=["GET"])
def get_monthly_completion_rate():
    """Return workout completion count: current month vs previous month"""
    try:
        client_id = request.args.get('client_id', type=int)
        
        if not client_id:
            return jsonify({"error": "client_id is required"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
            SELECT 
                MONTH(workout_date) AS month,
                COUNT(*) AS workouts_completed
            FROM Client_Workout_Log
            WHERE client_id = %s
              AND workout_date >= '2025-10-01'
              AND completion_status = 'completed'
            GROUP BY MONTH(workout_date)
            ORDER BY month DESC;
        """
        
        current_app.logger.debug(f'Executing query with client_id={client_id}')
        cursor.execute(query, (client_id,))
        completion_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved monthly completion rate')
        return jsonify(completion_data), 200
        
    except Error as e:
        current_app.logger.error(f'Database error in get_monthly_completion_rate: {str(e)}')
        return jsonify({"error": str(e)}), 500