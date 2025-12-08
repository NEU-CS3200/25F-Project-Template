from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app 

# create a blueprint for trainer feedback
trainer_feedback = Blueprint("trainer_feedback", __name__, url_prefix="/trainer/feedback")


# FOR TRAINER FEEDBACK 
# POST - create feedback
@trainer_feedback.route("/<int:trainer_id>", methods=["POST"])
def create_feedback(trainer_id):
    try:
        data = request.get_json()
        log_id = data.get("log_id")
        comment = data.get("comment")

        if not log_id or not comment:
            return jsonify({"error": "Missing required fields"}), 400

        cursor = db.get_db().cursor()
        cursor.execute("""
            INSERT INTO Trainer_Feedback (trainer_id, log_id, comment)
            VALUES (%s, %s, %s)
        """, (trainer_id, log_id, comment))

        db.get_db().commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "Feedback created", "feedback_id": new_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# DELETE a feedback entry 
@trainer_feedback.route("/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Trainer_Feedback WHERE feedback_id = %s", (feedback_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Feedback deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500