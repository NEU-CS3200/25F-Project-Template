from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app


# create a blueprint for workout specific exercise 
trainer_workout_exercises = Blueprint("trainer_workout_exercises", __name__, url_prefix="/trainer")

# GET all workout-specific exercises
@trainer_workout_exercises.route("/workout-exercises", methods=["GET"])
def get_workout_exercises():
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        query = """
            SELECT wse.workout_exercise_id,
                   wse.exercise_id,
                   e.name AS exercise_name,
                   e.category,
                   wse.sets,
                   wse.reps,
                   wse.rest_period
            FROM Workout_Specific_Exercise wse
            JOIN Exercise e ON wse.exercise_id = e.exercise_id
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        return jsonify(result), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# POST create workout-specific exercise
@trainer_workout_exercises.route("/workout-exercises", methods=["POST"])
def create_workout_exercise():
    try:
        data = request.get_json()
        exercise_id = data.get("exercise_id")
        sets = data.get("sets")
        reps = data.get("reps")
        rest = data.get("rest_period")

        if not exercise_id or not sets or not reps:
            return jsonify({"error": "Missing required fields"}), 400

        conn = db.get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Workout_Specific_Exercise (exercise_id, sets, reps, rest_period)
            VALUES (%s, %s, %s, %s)
        """, (exercise_id, sets, reps, rest))

        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "Workout exercise created", "workout_exercise_id": new_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500