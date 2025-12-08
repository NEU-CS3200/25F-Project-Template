from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

system_admin = Blueprint("system_admin", __name__)

# GET /system_logs  [Ava-6]
@system_admin.route("/system_logs", methods=["GET"])
def get_system_logs():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM System_Log ORDER BY timestamp DESC")
        logs = cursor.fetchall()
        cursor.close()
        return jsonify(logs), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# GET /system_logs/{action_type}   [Ava-5]
@system_admin.route("/system_logs/<string:action_type>", methods=["GET"])
def get_logs_by_action(action_type):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT * FROM System_Log
            WHERE action_type = %s
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (action_type,))
        logs = cursor.fetchall()
        cursor.close()

        return jsonify(logs), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# POST /user   [Ava-1], [Ava-2]
@system_admin.route("/user", methods=["POST"])
def create_user():
    try:
        data = request.get_json()

        required = ["email", "password_hash", "role"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO User (email, password_hash, role, permissions, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["email"],
            data["password_hash"],
            data["role"],
            data.get("permissions"),
            data.get("created_by")   # system_admin_id
        ))

        db.get_db().commit()
        new_user_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "User created", "user_id": new_user_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500

# GET /user/{id}  [Ava-4]
@system_admin.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# PUT /user/{id}   [Ava-4]
@system_admin.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        allowed = ["permissions", "role"]

        fields = []
        params = []

        for field in allowed:
            if field in data:
                fields.append(f"{field} = %s")
                params.append(data[field])

        if not fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(user_id)

        cursor = db.get_db().cursor()
        query = f"UPDATE User SET {', '.join(fields)} WHERE user_id = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "User updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# POST /trainer  [Ava-1]
@system_admin.route("/trainer", methods=["POST"])
def create_trainer_profile():
    try:
        data = request.get_json()

        required = ["user_id", "first_name", "last_name", "certification", "specialization"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO Trainer (user_id, first_name, last_name, certification, specialization)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["user_id"],
            data["first_name"],
            data["last_name"],
            data["certification"],
            data["specialization"]
        ))

        db.get_db().commit()
        profile_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Trainer profile created", "trainer_id": profile_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# DELETE /user/{id} [Ava-4]
@system_admin.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "User deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# POST /client  [Ava-2]
@system_admin.route("/client", methods=["POST"])
def create_client_profile():
    try:
        data = request.get_json()

        required = ["user_id", "first_name", "last_name"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing {field}"}), 400

        cursor = db.get_db().cursor()
        query = """
            INSERT INTO Client (user_id, first_name, last_name, date_of_birth, fitness_level, goals, join_date)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
        """

        cursor.execute(query, (
            data["user_id"],
            data["first_name"],
            data["last_name"],
            data.get("date_of_birth"),
            data.get("fitness_level"),
            data.get("goals")
        ))

        db.get_db().commit()
        new_client_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Client profile created", "client_id": new_client_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

@system_admin.route("/exercise/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Check if exercise exists first
        cursor.execute("SELECT * FROM Exercise WHERE exercise_id = %s", (exercise_id,))
        existing = cursor.fetchone()

        if not existing:
            cursor.close()
            return jsonify({"error": "Exercise not found"}), 404

        # Perform deletion
        cursor.execute("DELETE FROM Exercise WHERE exercise_id = %s", (exercise_id,))
        conn.commit()
        cursor.close()
        return jsonify({"message": "Exercise deleted"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        # Catches ANY non-database error so Flask never returns HTML
        return jsonify({"error": f"Unhandled error: {str(e)}"}), 500

# PUT /exercise/{exercise_id}   [Ava-5]
@system_admin.route("/exercise/<int:exercise_id>", methods=["PUT"])
def update_exercise(exercise_id):
    try:
        data = request.get_json()
        allowed = ["name", "description", "category"]

        fields = []
        params = []

        for field in allowed:
            if field in data:
                fields.append(f"{field} = %s")
                params.append(data[field])

        if not fields:
            return jsonify({"error": "Nothing to update"}), 400

        params.append(exercise_id)

        cursor = db.get_db().cursor()
        query = f"UPDATE Exercise SET {', '.join(fields)} WHERE exercise_id = %s"
        cursor.execute(query, params)

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Exercise updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# GET /backup_logs [Ava-7]
@system_admin.route("/backup_logs", methods=["GET"])
def get_backup_logs():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Backup_Log ORDER BY backup_end DESC")
        backups = cursor.fetchall()
        cursor.close()
        return jsonify(backups), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# GET /backup_logs/{status} [Ava-7]
@system_admin.route("/backup_logs/status", methods=["GET"])
def get_backup_status():
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT 
                backup_end,
                DATEDIFF(NOW(), backup_end) AS days_since_backup
            FROM Backup_Log
            WHERE status = 'success'
            ORDER BY backup_end DESC
            LIMIT 1;
        """

        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()

        # No backups found
        if not row:
            return jsonify({
                "message": "No successful backups found.",
                "status": "unknown"
            }), 200

        days = row["days_since_backup"]

        if days < 7:
            status = "up_to_date"
            msg = "Backups are current."
        elif days == 7:
            status = "due"
            msg = "Backup is due today."
        else:
            status = "overdue"
            msg = f"Backups are overdue by {days - 7} days."

        return jsonify({
            "status": status,
            "days_since_backup": days,
            "message": msg
        }), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# GET /user/permissions [Ava-6]
@system_admin.route("/user/permissions", methods=["GET"])
def get_all_role_permissions():
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT user_id, role, permissions
            FROM User
            ORDER BY role
        """

        cursor.execute(query)
        perms = cursor.fetchall()
        cursor.close()

        return jsonify(perms), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# PUT /user/permissions [Ava-4]
@system_admin.route("/user/permissions", methods=["PUT"])
def update_role_permissions():
    try:
        data = request.get_json()

        required_fields = ["role", "new_permissions"]
        for f in required_fields:
            if f not in data:
                return jsonify({"error": f"Missing required field: {f}"}), 400

        cursor = db.get_db().cursor()

        query = """
            UPDATE User
            SET permissions = %s
            WHERE role = %s
        """

        cursor.execute(query, (data["new_permissions"], data["role"]))
        db.get_db().commit()
        cursor.close()

        return jsonify({
            "message": f"Updated permissions for all {data['role']} users."
        }), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
