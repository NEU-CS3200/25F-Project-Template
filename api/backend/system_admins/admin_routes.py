from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for NGO routes
admins = Blueprint("admins", __name__)

# remove a player for fraud 
@admins.route('/players/<int:playerID>/remove', methods=['DELETE'])
def remove_player_fraud(playerID):
    try:
        cursor = db.get_db().cursor()
        
        # First check if player exists
        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        player = cursor.fetchone()
        
        if not player:
            cursor.close()
            return jsonify({"error": "Player not found"}), 404
        
        # Log the removal reason (you might want a separate audit table)
        cursor.execute("""
            INSERT INTO Reports (adminID, repStatus, userReported, date)
            VALUES (%s, 'completed', %s, NOW())
        """, (3, f"Player {playerID} - Fraud/Misinformation"))  

        cursor.execute("DELETE FROM Players WHERE playerID = %s", (playerID,))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({
            "success": True,
            "message": f"Player {playerID} removed for fraud/misinformation"
        }), 200
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500


# remove fraudulent game statistics 
@admins.route('/stats/fraudulent/<int:gameStatID>/remove', methods=['DELETE'])
def remove_fraudulent_stats(gameStatID):
    try:
        cursor = db.get_db().cursor()
        
        # Check if the stat exists
        cursor.execute("SELECT * FROM GameStats WHERE gameStatID = %s", (gameStatID,))
        stat = cursor.fetchone()
        
        if not stat:
            cursor.close()
            return jsonify({"error": "Game stat not found"}), 404
        
        # Log the removal in Reports table
        cursor.execute("""
            INSERT INTO Reports (adminID, repStatus, userReported, date)
            VALUES (%s, 'completed', %s, NOW())
        """, (4, f"GameStat {gameStatID} - Fraudulent stats removed"))
        
        # Delete the fraudulent stat
        cursor.execute("DELETE FROM GameStats WHERE gameStatID = %s", (gameStatID,))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({
            "success": True,
            "message": f"Fraudulent game stat {gameStatID} has been removed"
        }), 200
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# update player profile information
@admins.route('/players/<int:playerID>/update', methods=['PUT'])
def update_player_profile(playerID):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Check if player exists
        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Player not found"}), 404
        
        # Build dynamic UPDATE query based on provided fields
        update_fields = []
        values = []
        
        # Allowed fields to update
        allowed_fields = ['firstName', 'lastName', 'email', 'dateOfBirth', 
                         'phoneNumber', 'userBio', 'height', 'weight', 
                         'position', 'teamID', 'acctStatus']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                values.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        # Add playerID at the end for WHERE clause
        values.append(playerID)
        
        # Execute update
        update_query = f"""
            UPDATE Players 
            SET {', '.join(update_fields)}
            WHERE playerID = %s
        """
        
        cursor.execute(update_query, values)
        
        # Log the update
        cursor.execute("""
            INSERT INTO Reports (adminID, repStatus, userReported, date)
            VALUES (%s, 'completed', %s, NOW())
        """, (1, f"Updated profile for Player {playerID}"))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({
            "success": True,
            "message": f"Player {playerID} profile updated successfully",
            "updated_fields": list(data.keys())
        }), 200
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500   


# verify scouts joining the app
@admins.route('/scouts/<int:scout_id>/verify', methods=['PUT'])
def verify_scout(scout_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT scoutID, firstName, lastName, acctStatus FROM Scouts WHERE scoutID = %s", (scout_id,))
        scout = cursor.fetchone()
        
        if not scout:
            cursor.close()
            return jsonify({'success': False, 'message': f'Scout {scout_id} not found'}), 404
        
        cursor.execute("UPDATE Scouts SET acctStatus = 'active' WHERE scoutID = %s", (scout_id,))
        
        cursor.execute("INSERT INTO Reports (adminID, repStatus, userReported, date) VALUES (%s, 'completed', %s, NOW())", (1, f"Verified scout {scout_id}"))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': f'Scout {scout_id} verified successfully', 'scout': {'scoutID': scout['scoutID'], 'firstName': scout['firstName'], 'lastName': scout['lastName'], 'acctStatus': 'active'}}), 200
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# updating scout profiles 
@admins.route('/scouts/<int:scout_id>/update', methods=['PUT'])
def update_scout_profile(scout_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Scouts WHERE scoutID = %s", (scout_id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'message': 'Scout not found'}), 404
        
        update_fields = []
        values = []
        
        allowed_fields = ['firstName', 'lastName', 'email', 'dateOfBirth', 'age', 'phoneNum', 'acctStatus', 'role']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                values.append(data[field])
        
        if not update_fields:
            return jsonify({'success': False, 'message': 'No valid fields to update'}), 400
        
        values.append(scout_id)
        
        update_query = f"UPDATE Scouts SET {', '.join(update_fields)} WHERE scoutID = %s"
        
        cursor.execute(update_query, values)
        
        cursor.execute("INSERT INTO Reports (adminID, repStatus, userReported, date) VALUES (%s, 'completed', %s, NOW())", (1, f"Updated profile for Scout {scout_id}"))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': f'Scout {scout_id} profile updated successfully', 'updated_fields': list(data.keys())}), 200
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500