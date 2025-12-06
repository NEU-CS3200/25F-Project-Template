from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

# Blueprint for all professor / override routes
professors = Blueprint("professors", __name__)



def fetch_all_dicts(cursor):
    """
    Take cursor.fetchall() rows and turn them into a list of dicts
    using cursor.description for column names.
    """
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def fetch_one_dict(cursor):
    """
    Same as fetch_all_dicts, but for a single row (cursor.fetchone()).
    """
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))




# GET /professors/<prof_id>/sections
# Returns all sections (optionally filtered by term).
# NOTE: schema doesn't link Section to Professor, so we ignore prof_id for now.
@professors.route("/professors/<int:prof_id>/sections", methods=["GET"])
def get_professor_sections(prof_id):
    try:
        term = request.args.get("term")

        cursor = db.get_db().cursor()

        query = """
            SELECT s.CRN,
                   s.section_num,
                   s.day_of_week,
                   s.start_time,
                   s.end_time,
                   s.location,
                   s.semester,
                   s.capacity,
                   c.courseID,
                   c.course_name
            FROM Section s
            JOIN Course c ON s.CRN = c.courseID
        """
        params = []

        if term:
            query += " WHERE s.semester = %s"
            params.append(term)

        current_app.logger.info("GET professor sections query: %s", query)
        cursor.execute(query, params)
        rows = fetch_all_dicts(cursor)
        cursor.close()

        return jsonify(rows), 200

    except Error as e:
        current_app.logger.error(f"DB error in get_professor_sections: {e}")
        return jsonify({"error": str(e)}), 500


# GET /professors/<prof_id>/ratings
# Returns all ratings + average rating for that professor
@professors.route("/professors/<int:prof_id>/ratings", methods=["GET"])
def get_professor_ratings(prof_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT
                rated_num,
                created_aT AS created_at,
                rating,
                comment
            FROM Rating
            WHERE profID = %s
            ORDER BY created_aT DESC
            """,
            (prof_id,),
        )

        rating_rows = fetch_all_dicts(cursor)

        avg_rating = None
        if rating_rows:
            total = sum(float(r["rating"]) for r in rating_rows)
            avg_rating = total / len(rating_rows)

        cursor.close()

        data = {
            "profID": prof_id,
            "average_rating": avg_rating,
            "num_ratings": len(rating_rows),
            "ratings": rating_rows,
        }

        return jsonify(data), 200

    except Error as e:
        current_app.logger.error(f"DB error in get_professor_ratings: {e}")
        return jsonify({"error": str(e)}), 500


# GET /sections/<CRN>/overriderequests
# Returns all override requests for a specific section, including student info
@professors.route("/sections/<int:crn>/overriderequests", methods=["GET"])
def get_section_override_requests(crn):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT
                o.request_id,
                o.request_date,
                o.status,
                o.student_message,
                o.decision_date,
                o.studentID,
                s.f_name,
                s.l_name,
                s.email
            FROM OverrideRequest o
            JOIN Student s ON o.studentID = s.studentID
            WHERE o.CRN = %s
            ORDER BY o.request_date DESC
        """

        cursor.execute(query, (crn,))
        rows = fetch_all_dicts(cursor)
        cursor.close()

        return jsonify(rows), 200

    except Error as e:
        current_app.logger.error(
            f"DB error in get_section_override_requests: {e}"
        )
        return jsonify({"error": str(e)}), 500


# GET /overriderequests/<request_id>
# Returns full details for a single override request
@professors.route("/overriderequests/<int:request_id>", methods=["GET"])
def get_single_override_request(request_id):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT
                o.request_id,
                o.request_date,
                o.status,
                o.student_message,
                o.decision_date,
                o.studentID,
                o.CRN,
                s.f_name,
                s.l_name,
                s.email
            FROM OverrideRequest o
            JOIN Student s ON o.studentID = s.studentID
            WHERE o.request_id = %s
        """

        cursor.execute(query, (request_id,))
        row = fetch_one_dict(cursor)
        cursor.close()

        if not row:
            return jsonify({"error": "Override request not found"}), 404

        return jsonify(row), 200

    except Error as e:
        current_app.logger.error(
            f"DB error in get_single_override_request: {e}"
        )
        return jsonify({"error": str(e)}), 500


# PUT /overriderequests/<request_id>
# Updates the status of an override request
@professors.route("/overriderequests/<int:request_id>", methods=["PUT"])
def update_override_request_status(request_id):
    try:
        data = request.get_json()

        if not data or "status" not in data:
            return jsonify({"error": "Missing 'status' in request body"}), 400

        new_status = data["status"]

        cursor = db.get_db().cursor()

        query = """
            UPDATE OverrideRequest
            SET status = %s,
                decision_date = CURRENT_DATE
            WHERE request_id = %s
        """

        cursor.execute(query, (new_status, request_id))
        db.get_db().commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Override request not found"}), 404

        cursor.close()
        return jsonify({"message": "Override request updated"}), 200

    except Error as e:
        current_app.logger.error(
            f"DB error in update_override_request_status: {e}"
        )
        return jsonify({"error": str(e)}), 500


# DELETE /overriderequests/<request_id>
# Cancels or removes an override request
@professors.route("/overriderequests/<int:request_id>", methods=["DELETE"])
def delete_override_request(request_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "DELETE FROM OverrideRequest WHERE request_id = %s",
            (request_id,),
        )
        db.get_db().commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Override request not found"}), 404

        cursor.close()
        return jsonify({"message": "Override request deleted"}), 200

    except Error as e:
        current_app.logger.error(
            f"DB error in delete_override_request: {e}"
        )
        return jsonify({"error": str(e)}), 500


# GET /professors/<prof_id>/overriderequests
# Returns all override requests (schema doesn't track which prof teaches which section)
@professors.route(
    "/professors/<int:prof_id>/overriderequests", methods=["GET"]
)
def get_professor_override_requests(prof_id):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT
                o.request_id,
                o.request_date,
                o.status,
                o.student_message,
                o.decision_date,
                o.studentID,
                o.CRN
            FROM OverrideRequest o
            ORDER BY o.request_date DESC
        """

        cursor.execute(query)
        rows = fetch_all_dicts(cursor)
        cursor.close()

        return jsonify(rows), 200

    except Error as e:
        current_app.logger.error(
            f"DB error in get_professor_override_requests: {e}"
        )
        return jsonify({"error": str(e)}), 500


# PUT /professors/<prof_id>/overriderequests
# Bulk update multiple override requests at once
@professors.route(
    "/professors/<int:prof_id>/overriderequests", methods=["PUT"]
)
def bulk_update_professor_override_requests(prof_id):
    try:
        data = request.get_json()

        if not data or "updates" not in data:
            return jsonify({"error": "Missing 'updates' in request body"}), 400

        updates = data["updates"]
        if not isinstance(updates, list) or len(updates) == 0:
            return jsonify({"error": "'updates' must be a non-empty list"}), 400

        cursor = db.get_db().cursor()

        query = """
            UPDATE OverrideRequest
            SET status = %s,
                decision_date = CURRENT_DATE
            WHERE request_id = %s
        """

        affected_total = 0
        for u in updates:
            req_id = u.get("request_id")
            status = u.get("status")
            if req_id is None or status is None:
                continue
            cursor.execute(query, (status, req_id))
            affected_total += cursor.rowcount

        db.get_db().commit()
        cursor.close()

        return (
            jsonify(
                {
                    "message": "Bulk override update complete",
                    "rows_affected": affected_total,
                }
            ),
            200,
        )

    except Error as e:
        current_app.logger.error(
            f"DB error in bulk_update_professor_override_requests: {e}"
        )
        return jsonify({"error": str(e)}), 500


# GET /students/<student_id>
# Returns basic student info for an override request
@professors.route("/students/<int:student_id>", methods=["GET"])
def get_basic_student_info(student_id):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT studentID,
                   f_name,
                   l_name,
                   email,
                   mobile,
                   year,
                   credits_completed
            FROM Student
            WHERE studentID = %s
        """
        cursor.execute(query, (student_id,))
        row = fetch_one_dict(cursor)
        cursor.close()

        if not row:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(row), 200

    except Error as e:
        current_app.logger.error(
            f"DB error in get_basic_student_info: {e}"
        )
        return jsonify({"error": str(e)}), 500