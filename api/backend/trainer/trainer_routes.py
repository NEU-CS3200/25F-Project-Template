from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error

trainer = Blueprint("trainer", __name__)

# ============================================================
# 1) WORKOUT-SPECIFIC EXERCISES
# ============================================================

# CREATE a workout-specific exercise
@trainer.route("/create-workout-exercises", methods=["POST"])
def create_workout_exercise():
    try:
        data = request.get_json()
        workout_id = data.get("workout_id")
        exercise_id = data.get("exercise_id")
        sets = data.get("sets")
        reps = data.get("reps")
        rest = data.get("rest_period")

        if not workout_id or not exercise_id:
            return jsonify({"error": "workout_id and exercise_id required"}), 400

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Workout_Specific_Exercise
                (workout_id, exercise_id, sets, reps, rest_period)
            VALUES (%s, %s, %s, %s, %s)
        """, (workout_id, exercise_id, sets, reps, rest))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Workout-specific exercise created"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# GET workout-specific exercises
@trainer.route("/workout-exercises", methods=["GET"])
def get_workout_exercises():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT 
                wse.workout_exercise_id,
                wse.workout_id,
                wse.exercise_id,
                e.name AS exercise_name,
                e.category,
                wse.sets,
                wse.reps,
                wse.rest_period
            FROM Workout_Specific_Exercise wse
            JOIN Exercise e ON wse.exercise_id = e.exercise_id
        """)

        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 2) WORKOUT TEMPLATES (CRUD)
# ============================================================

# CREATE workout template
@trainer.route("/create-templates/<int:trainer_id>", methods=["POST"])
def create_template(trainer_id):
    try:
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        duration = data.get("duration_minutes")
        difficulty = data.get("difficulty")  # ENUM('Easy','Medium','Hard')

        if not name or not difficulty:
            return jsonify({"error": "name and difficulty required"}), 400

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Workout_Session_Template 
                (trainer_id, name, description, duration_minutes, difficulty)
            VALUES (%s, %s, %s, %s, %s)
        """, (trainer_id, name, description, duration, difficulty))

        db.get_db().commit()
        template_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Template created", "template_id": template_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# GET all templates created by trainer
@trainer.route("/view-all-templates/<int:trainer_id>", methods=["GET"])
def get_templates(trainer_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT *
            FROM Workout_Session_Template
            WHERE trainer_id = %s
        """, (trainer_id,))

        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# UPDATE template
@trainer.route("/update-template/<int:template_id>", methods=["PUT"])
def update_template(template_id):
    try:
        data = request.get_json()

        cursor = db.get_db().cursor()
        cursor.execute("""
            UPDATE Workout_Session_Template
            SET name = %s,
                description = %s,
                duration_minutes = %s,
                difficulty = %s
            WHERE workout_id = %s
        """, (data["name"], data["description"],
              data["duration_minutes"], data["difficulty"], template_id))

        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Template updated"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# DELETE template
@trainer.route("/delete-template/<int:template_id>", methods=["DELETE"])
def delete_template(template_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Workout_Session_Template WHERE workout_id = %s", (template_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Template deleted"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 3) CLIENT PROGRAMS (CRUD)
# ============================================================

# ASSIGN workout template to client as workout programs
@trainer.route("/programs/<int:trainer_id>", methods=["POST"])
def assign_program(trainer_id):
    try:
        data = request.get_json()
        client_id = data.get("client_id")
        workout_id = data.get("workout_id")  # correct FK
        name = data.get("name")
        description = data.get("description")

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Client_Specific_Workout_Program
                (workout_id, created_by, client_id, name, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (workout_id, trainer_id, client_id, name, description))

        db.get_db().commit()
        program_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Program assigned", "program_id": program_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# GET list of assigned programs (by trainer)
@trainer.route("/programs/<int:trainer_id>", methods=["GET"])
def get_programs(trainer_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT *
            FROM Client_Specific_Workout_Program
            WHERE created_by = %s
        """, (trainer_id,))

        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# UPDATE assigned program
@trainer.route("/programs/update/<int:program_id>", methods=["PUT"])
def update_program(program_id):
    try:
        data = request.get_json()

        cursor = db.get_db().cursor()
        cursor.execute("""
            UPDATE Client_Specific_Workout_Program
            SET name = %s,
                description = %s
            WHERE program_id = %s
        """, (data["name"], data["description"], program_id))

        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Program updated"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# DELETE assigned program
@trainer.route("/programs/<int:program_id>", methods=["DELETE"])
def delete_program(program_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Client_Specific_Workout_Program WHERE program_id = %s", (program_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Program removed"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 4) CLIENT LOGS / COMPLETED FILTER / PROGRESS METRICS
# ============================================================

# GET all completed logs
@trainer.route("/client-logs", methods=["GET"])
def completed_logs():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT *
            FROM Client_Workout_Log
            WHERE completion_status = 'completed'
            ORDER BY workout_date DESC
        """)

        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# CLIENT progress metrics
@trainer.route("/progress/<int:client_id>", methods=["GET"])
def client_progress(client_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT 
                client_id,
                COUNT(*) AS total_workouts,
                SUM(completion_status = 'completed') AS completed,
                ROUND(SUM(completion_status='completed') / COUNT(*), 2) AS completion_rate
            FROM Client_Workout_Log
            WHERE client_id = %s
        """, (client_id,))

        row = cursor.fetchone()
        cursor.close()
        return jsonify(row), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# 5) FEEDBACK
# ============================================================
# ============================================================
# 🔹 GET all feedback for a log
# ============================================================

@trainer.route("/getfeedback/<int:log_id>", methods=["GET"])
def get_feedback(log_id):
    try:
        cursor = db.get_db().cursor(d)

        cursor.execute("""
            SELECT 
                feedback_id,
                trainer_id,
                log_id,
                comment,
                created_at
            FROM Trainer_Feedback
            WHERE log_id = %s
            ORDER BY created_at DESC
        """, (log_id,))

        feedback = cursor.fetchall()
        cursor.close()

        return jsonify(feedback), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# CREATE feedback
@trainer.route("/createfeedback/<int:log_id>", methods=["POST"])
def create_feedback(log_id):
    try:
        data = request.get_json()
        trainer_id = data.get("trainer_id")
        comment = data.get("comment")

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Trainer_Feedback (log_id, trainer_id, comment)
            VALUES (%s, %s, %s)
        """, (log_id, trainer_id, comment))

        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Feedback added"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# DELETE feedback
@trainer.route("/deletefeedback/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Trainer_Feedback WHERE feedback_id = %s", (feedback_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Feedback deleted"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
