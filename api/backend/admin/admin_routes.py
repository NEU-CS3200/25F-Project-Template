from flask import Blueprint, request, jsonify, make_response
from backend.db_connection.db import db

admin_bp = Blueprint('admin', __name__)

# USER STORY 1 — View unresolved reports
@admin_bp.route('/reports/pending', methods=['GET'])
def get_pending_reports():
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT ReportID, Severity, Note, ReportedItem
        FROM Reports
        WHERE Resolved = 0;
    """)
    data = cursor.fetchall()

    the_response = make_response(jsonify(data))
    the_response.status_code = 200
    return the_response


# USER STORY 1 — Resolve a report
@admin_bp.route('/reports/<int:report_id>/resolve', methods=['PUT'])
def resolve_report(report_id):
    cursor = db.get_db().cursor()
    cursor.execute("""
        UPDATE Reports
        SET Resolved = 1, ResolvedAt = NOW()
        WHERE ReportID = %s;
    """, (report_id,))

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Report resolved"}))
    the_response.status_code = 200
    return the_response


# USER STORY 2 — Update user role
@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    new_role = request.json.get("role")

    cursor = db.get_db().cursor()
    cursor.execute("""
        UPDATE Users
        SET Role = %s
        WHERE UserID = %s;
    """, (new_role, user_id))

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "User role updated"}))
    the_response.status_code = 200
    return the_response


# USER STORY 3 — Deactivate user
@admin_bp.route('/users/<int:user_id>/deactivate', methods=['PUT'])
def deactivate_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute("""
        UPDATE Users
        SET IsActive = 0
        WHERE UserID = %s;
    """, (user_id,))

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "User deactivated"}))
    the_response.status_code = 200
    return the_response


# USER STORY 4 — Create announcement
@admin_bp.route('/announcements', methods=['POST'])
def create_announcement():
    data = request.json
    announcer = data.get("announcer_id")
    message = data.get("message")

    cursor = db.get_db().cursor()

    cursor.execute("""
        INSERT INTO Announcements (AnnouncerID, Message, AnnouncedAt)
        VALUES (%s, %s, NOW());
    """, (announcer, message))

    announcement_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO AnnouncementsReceived (AnnouncementID, UserID)
        SELECT %s, UserID FROM Users WHERE IsActive = 1;
    """, (announcement_id,))

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Announcement created"}))
    the_response.status_code = 201
    return the_response


# USER STORY 5 — Analytics summary
@admin_bp.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM Users) AS TotalUsers,
            (SELECT COUNT(*) FROM Items) AS TotalListings,
            (SELECT COUNT(*) FROM Reports WHERE Resolved = 0) AS OpenReports;
    """)
    data = cursor.fetchall()

    the_response = make_response(jsonify(data))
    the_response.status_code = 200
    return the_response


# USER STORY 6 — Delete duplicate items
@admin_bp.route('/items/duplicates', methods=['DELETE'])
def delete_duplicate_items():
    cursor = db.get_db().cursor()
    cursor.execute("""
        DELETE i FROM Items i
        JOIN (
            SELECT Title, OwnerID, MIN(ItemID) AS KeepID
            FROM Items
            GROUP BY Title, OwnerID
        ) base
        ON i.Title = base.Title
        AND i.OwnerID = base.OwnerID
        AND i.ItemID != base.KeepID;
    """)

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Duplicate items removed"}))
    the_response.status_code = 200
    return the_response


# USER STORY 6 + 1 — Delete specific item
@admin_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("DELETE FROM Images WHERE ItemID = %s;", (item_id,))
        cursor.execute("DELETE FROM ItemTags WHERE ItemID = %s;", (item_id,))
        cursor.execute("DELETE FROM OrderItems WHERE ItemID = %s;", (item_id,))
        cursor.execute("DELETE FROM Reports WHERE ReportedItem = %s;", (item_id,))
        cursor.execute("DELETE FROM Items WHERE ItemID = %s;", (item_id,))

        db.get_db().commit()

        the_response = make_response(jsonify({"message": "Item removed"}))
        the_response.status_code = 200
        return the_response

    except Exception as e:
        db.get_db().rollback()

        the_response = make_response(jsonify({"error": str(e)}))
        the_response.status_code = 500
        return the_response
