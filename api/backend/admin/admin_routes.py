from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

admin = Blueprint("admin", __name__)

# Get all reports with optional filtering by status
# Streamlit: Use requests.get('http://web-api:4000/reports') to get queue of reports
#            Add ?status=pending for filtering
#            Display in a table for admin review
@admin.route("/reports", methods=["GET"])
def get_all_reports():
    try:
        current_app.logger.info('Starting get_all_reports request')
        cursor = db.get_db().cursor()
        
        # Get optional query parameter for filtering
        status = request.args.get("status")
        
        current_app.logger.debug(f'Query parameter - status: {status}')
        
        # Base query
        query = "SELECT * FROM report WHERE 1=1"
        params = []
        
        # Add filter if provided
        if status:
            query += " AND status = %s"
            params.append(status)
        
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        reports = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(reports)} reports')
        return jsonify(reports), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_reports: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific report by ID
# Streamlit: Use requests.get(f'http://web-api:4000/reports/{report_id}')
#            Display report details for admin review
@admin.route("/reports/<int:report_id>", methods=["GET"])
def get_report(report_id):
    try:
        current_app.logger.info('Starting get_report request')
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM report WHERE report_id = %s", (report_id,))
        report = cursor.fetchone()

        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        cursor.close()

        current_app.logger.info("Successfully retrieved report")
        return jsonify(report), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_report: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create new report
# Streamlit: Use st.form() to collect report info, then:
#            requests.post('http://web-api:4000/reports', json={
#                "reporter_id": user_id, "reporter_type": "student",
#                "reported_user_id": bad_user_id, "reported_user_type": "alumni",
#                "reason": "Inappropriate behavior"
#            })
@admin.route("/reports", methods=["POST"])
def create_report():
    try:
        data = request.get_json()
        
        # Required fields
        required_fields = ["reporter_id", "reporter_type", "reported_user_id", "reported_user_type", "reason"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, admin_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["reporter_id"],
            data["reporter_type"],
            data["reported_user_id"],
            data["reported_user_type"],
            data["reason"],
            data.get("status", "pending"),
            data.get("admin_id")
        ))
        
        db.get_db().commit()
        new_report_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Report created successfully", "report_id": new_report_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update report status/resolution
# Streamlit: Use buttons for Resolve/Dismiss, then:
#            requests.put(f'http://web-api:4000/reports/{report_id}', json={
#                "status": "resolved", "admin_id": admin_id
#            })
@admin.route("/reports/<int:report_id>", methods=["PUT"])
def update_report(report_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check if report exists
        cursor.execute("SELECT * FROM report WHERE report_id = %s", (report_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Report not found"}), 404

        # Build dynamic update query
        allowed_fields = ["status", "admin_id"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(report_id)

        query = f"UPDATE report SET {', '.join(update_fields)} WHERE report_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Report updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all community guidelines
# Streamlit: Use requests.get('http://web-api:4000/guidelines')
#            Display guidelines list for users
@admin.route("/guidelines", methods=["GET"])
def get_all_guidelines():
    try:
        current_app.logger.info('Starting get_all_guidelines request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM community_guideline")
        guidelines = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(guidelines)} guidelines')
        return jsonify(guidelines), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_guidelines: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific guideline
# Streamlit: Use requests.get(f'http://web-api:4000/guidelines/{guideline_id}')
@admin.route("/guidelines/<int:guideline_id>", methods=["GET"])
def get_guideline(guideline_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM community_guideline WHERE guideline_id = %s", (guideline_id,))
        guideline = cursor.fetchone()

        if not guideline:
            return jsonify({"error": "Guideline not found"}), 404
        
        cursor.close()
        return jsonify(guideline), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Create new guideline
# Streamlit: Use st.form() to collect guideline text, then:
#            requests.post('http://web-api:4000/guidelines', json={
#                "guideline_text": "Be respectful to all users",
#                "created_by_admin_id": admin_id
#            })
@admin.route("/guidelines", methods=["POST"])
def create_guideline():
    try:
        data = request.get_json()
        
        required_fields = ["guideline_text", "created_by_admin_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO community_guideline (guideline_text, created_by_admin_id)
        VALUES (%s, %s)
        """
        cursor.execute(query, (data["guideline_text"], data["created_by_admin_id"]))
        
        db.get_db().commit()
        new_guideline_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Guideline created successfully", "guideline_id": new_guideline_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update guideline text
# Streamlit: Use st.form() to edit text, then:
#            requests.put(f'http://web-api:4000/guidelines/{guideline_id}', json={
#                "guideline_text": "Updated guideline text"
#            })
@admin.route("/guidelines/<int:guideline_id>", methods=["PUT"])
def update_guideline(guideline_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM community_guideline WHERE guideline_id = %s", (guideline_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Guideline not found"}), 404

        if "guideline_text" not in data:
            return jsonify({"error": "guideline_text is required"}), 400

        cursor.execute("UPDATE community_guideline SET guideline_text = %s WHERE guideline_id = %s", 
                      (data["guideline_text"], guideline_id))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Guideline updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete guideline
# Streamlit: Add confirmation, then:
#            requests.delete(f'http://web-api:4000/guidelines/{guideline_id}')
@admin.route("/guidelines/<int:guideline_id>", methods=["DELETE"])
def delete_guideline(guideline_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM community_guideline WHERE guideline_id = %s", (guideline_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Guideline not found"}), 404
        
        cursor.execute("DELETE FROM community_guideline WHERE guideline_id = %s", (guideline_id,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Guideline deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all announcements
# Streamlit: Use requests.get('http://web-api:4000/announcements')
#            Display announcements for all users
@admin.route("/announcements", methods=["GET"])
def get_all_announcements():
    try:
        current_app.logger.info('Starting get_all_announcements request')
        cursor = db.get_db().cursor()
        
        # Optional filter by target audience
        target_audience = request.args.get("target_audience")
        
        query = "SELECT * FROM announcement WHERE 1=1"
        params = []
        
        if target_audience:
            query += " AND target_audience = %s"
            params.append(target_audience)
        
        cursor.execute(query, params)
        announcements = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(announcements)} announcements')
        return jsonify(announcements), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_announcements: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get specific announcement
# Streamlit: Use requests.get(f'http://web-api:4000/announcements/{announcement_id}')
@admin.route("/announcements/<int:announcement_id>", methods=["GET"])
def get_announcement(announcement_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM announcement WHERE announcement_id = %s", (announcement_id,))
        announcement = cursor.fetchone()

        if not announcement:
            return jsonify({"error": "Announcement not found"}), 404
        
        cursor.close()
        return jsonify(announcement), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Create and broadcast announcement
# Streamlit: Use st.form() to compose announcement, then:
#            requests.post('http://web-api:4000/announcements', json={
#                "admin_id": admin_id, "title": "New Feature",
#                "message": "We've added...", "target_audience": "all"
#            })
@admin.route("/announcements", methods=["POST"])
def create_announcement():
    try:
        data = request.get_json()
        
        required_fields = ["admin_id", "title", "message"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        
        query = """
        INSERT INTO announcement (admin_id, title, message, target_audience)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["admin_id"],
            data["title"],
            data["message"],
            data.get("target_audience", "all")
        ))
        
        db.get_db().commit()
        new_announcement_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Announcement created successfully", "announcement_id": new_announcement_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update announcement
# Streamlit: Use st.form() to edit, then:
#            requests.put(f'http://web-api:4000/announcements/{announcement_id}', json={...})
@admin.route("/announcements/<int:announcement_id>", methods=["PUT"])
def update_announcement(announcement_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM announcement WHERE announcement_id = %s", (announcement_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Announcement not found"}), 404

        allowed_fields = ["title", "message", "target_audience"]
        params = []
        update_fields = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(announcement_id)

        query = f"UPDATE announcement SET {', '.join(update_fields)} WHERE announcement_id = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Announcement updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete announcement
# Streamlit: requests.delete(f'http://web-api:4000/announcements/{announcement_id}')
@admin.route("/announcements/<int:announcement_id>", methods=["DELETE"])
def delete_announcement(announcement_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM announcement WHERE announcement_id = %s", (announcement_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Announcement not found"}), 404
        
        cursor.execute("DELETE FROM announcement WHERE announcement_id = %s", (announcement_id,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Announcement deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get admin dashboard metrics
# Streamlit: Use requests.get('http://web-api:4000/admin/dashboard')
#            Display key metrics: active users, pending approvals, reports, etc.
@admin.route("/admin/dashboard", methods=["GET"])
def get_dashboard():
    try:
        cursor = db.get_db().cursor()
        
        # Get various metrics
        metrics = {}
        
        # Count active students
        cursor.execute("SELECT COUNT(*) as count FROM student")
        metrics['total_students'] = cursor.fetchone()['count']
        
        # Count active alumni
        cursor.execute("SELECT COUNT(*) as count FROM alumni")
        metrics['total_alumni'] = cursor.fetchone()['count']
        
        # Count pending applications
        cursor.execute("SELECT COUNT(*) as count FROM application WHERE status = 'pending'")
        metrics['pending_applications'] = cursor.fetchone()['count']
        
        # Count pending reports
        cursor.execute("SELECT COUNT(*) as count FROM report WHERE status = 'pending'")
        metrics['pending_reports'] = cursor.fetchone()['count']
        
        # Count total connections
        cursor.execute("SELECT COUNT(*) as count FROM connection")
        metrics['total_connections'] = cursor.fetchone()['count']
        
        # Count active sessions
        cursor.execute("SELECT COUNT(*) as count FROM session WHERE status = 'scheduled'")
        metrics['active_sessions'] = cursor.fetchone()['count']
        
        cursor.close()
        
        return jsonify(metrics), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500