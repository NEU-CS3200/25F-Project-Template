from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
import os


resumes = Blueprint("resumes", __name__)

# Fetch all resumes for a specific student
@resumes.route("/resumes/<int:student_id>", methods=["GET"])
def get_student_resumes(student_id):
    try:
        cursor = db.get_db().cursor()
        
        query = "SELECT resumeID, label, imageURl FROM Resume WHERE studentID = %s"
        cursor.execute(query, (student_id,))
        
        data = cursor.fetchall()
        cursor.close()
        
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Upload a new resume
@resumes.route("/resumes/upload", methods=["POST"])
def upload_resume():
    try:
        file = request.files.get('file')
        student_id = request.form.get('studentID')
        label = request.form.get('label')

        if not file or not student_id or not label:
            return jsonify({"error": "Missing file, studentID, or label"}), 400

        cursor = db.get_db().cursor()

        cursor.execute("SELECT MAX(resumeID) AS max_id FROM Resume")
        row = cursor.fetchone() 

        current_max = row['max_id'] if (row and row['max_id']) else 0
        new_resume_id = current_max + 1

        query = """
        INSERT INTO Resume (imageURl, label, resumeID, studentID)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (file.filename, label, new_resume_id, student_id))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Resume uploaded successfully", "resumeID": new_resume_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500