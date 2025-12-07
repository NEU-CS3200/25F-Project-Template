from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for course routes
courses = Blueprint('courses', __name__)


# GET /courses
# Return list of all courses with codes, titles, credits, descriptions
@courses.route("/courses", methods=["GET"])
def get_courses():

    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            courseID      AS course_code,
            course_name   AS course_title,
            credits,
            description
        FROM Course
        ORDER BY courseID;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    cursor.close()
    
    return jsonify(theData)

# POST /courses
# Add new courses (single or bulk JSON)
@courses.route("/courses", methods=["POST"])
def add_courses():

    data = request.get_json()

    # If user sent ONE object, convert to list for bulk handling
    if isinstance(data, dict):
        data = [data]

    cursor = db.get_db().cursor()

    insert_query = '''
        INSERT INTO Course (courseID, course_name, semesters_offered, Status, credits, description, deptID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''

    for course in data:
        cursor.execute(insert_query, (
            course.get("courseID"),
            course.get("course_name"),
            course.get("semesters_offered"),
            course.get("Status", "Active"),
            course.get("credits"),
            course.get("description"),
            course.get("deptID")
        ))

    db.get_db().commit()
    cursor.close()

    return jsonify({
        "message": "Course(s) added successfully",
        "count": len(data)
    })
