from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# create a blueprint for trainer programs
trainer_programs = Blueprint("trainer_programs", __name__, url_prefix="/trainer/programs")


# FOR THE CLIENT ASSIGNED PROGRAMS
# GET all the client programs created by the trainer
@trainer_programs.route("/client-programs/<int:trainer_id>", methods=["GET"])
def get_client_programs(trainer_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)
        cursor.execute("""
            SELECT program_id, client_id, workout_id, name, description, created_at
            FROM Client_Specific_Workout_Program
            WHERE created_by = %s
        """, (trainer_id,))
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# POST - assign a program to client
@trainer_programs.route("/client-programs/<int:trainer_id>", methods=["POST"])
def assign_program(trainer_id):
    try:
        data = request.get_json()
        client_id = data.get("client_id")
        workout_id = data.get("workout_id")
        name = data.get("name")
        description = data.get("description")

        if not client_id or not workout_id or not name:
            return jsonify({"error": "Missing required fields"}), 400

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Client_Specific_Workout_Program (workout_id, created_by, client_id, name, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (workout_id, trainer_id, client_id, name, description))

        db.get_db().commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "Program assigned", "program_id": new_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# PUT - update assigned program
@trainer_programs.route("/client-programs/<int:program_id>", methods=["PUT"])
def update_client_program(program_id):
    try:
        data = request.get_json()
        fields = []
        params = []

        allowed = ["name", "description"]

        for field in allowed:
            if field in data:
                fields.append(f"{field} = %s")
                params.append(data[field])

        if not fields:
            return jsonify({"error": "No valid fields"}), 400

        params.append(program_id)

        cursor = db.get_db().cursor()
        cursor.execute(f"""
            UPDATE Client_Specific_Workout_Program
            SET {", ".join(fields)}
            WHERE program_id = %s
        """, params)

        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Program updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# DELETE client program
@trainer_programs.route("/client-programs/<int:program_id>", methods=["DELETE"])
def delete_client_program(program_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Client_Specific_Workout_Program WHERE program_id = %s", (program_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Program removed"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500