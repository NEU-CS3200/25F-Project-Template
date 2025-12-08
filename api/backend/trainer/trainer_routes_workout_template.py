from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create a blueprint for trainer workout templates
trainer_templates = Blueprint("trainer_templates", __name__, url_prefix="/trainer/templates")

# FOR WORKOUT TEMPLATE 
# GET all the workout templates created by the trainer
@trainer_templates.route("/workout_session_template/<int:trainer_id>", methods=["GET"])
def get_trainer_templates(trainer_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)
        cursor.execute("""
            SELECT workout_id, name, description, duration_minutes, difficulty, date_created
            FROM Workout_Session_Template
            WHERE trainer_id = %s
        """, (trainer_id,))
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# POST - create a new workout template
@trainer_templates.route("/workout_session_template/<int:trainer_id>", methods=["POST"])
def create_template(trainer_id):
    try:
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        duration = data.get("duration_minutes")
        difficulty = data.get("difficulty")

        if not name or not difficulty:
            return jsonify({"error": "Missing required fields"}), 400

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Workout_Session_Template (trainer_id, name, description, duration_minutes, difficulty)
            VALUES (%s, %s, %s, %s, %s)
        """, (trainer_id, name, description, duration, difficulty))

        db.get_db().commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "Template created", "workout_id": new_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# PUT - update a created template 
@trainer_templates.route("/workout_session_template/<int:workout_id>", methods=["PUT"])
def update_template(workout_id):
    try:
        data = request.get_json()
        fields = []
        params = []

        allowed = ["name", "description", "duration_minutes", "difficulty"]
        for field in allowed:
            if field in data:
                fields.append(f"{field} = %s")
                params.append(data[field])

        if not fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(workout_id)

        cursor = db.get_db().cursor()
        cursor.execute(f"""
            UPDATE Workout_Session_Template
            SET {", ".join(fields)}
            WHERE workout_id = %s
        """, params)

        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Template updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# DELETE a workout template 
@trainer_templates.route("/workout_session_template/<int:workout_id>", methods=["DELETE"])
def delete_template(workout_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Workout_Session_Template WHERE workout_id = %s", (workout_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Template deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500