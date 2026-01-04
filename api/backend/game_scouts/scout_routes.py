from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for scout routes
scouts = Blueprint("scouts", __name__)

# Returns player stats that were recommended by the data analyst scout
@scouts.route("/players/<int:playerID>/stats/filtered", methods=["GET"])
def get_filtered_player_stats(playerID):
    try:
        cursor = db.get_db().cursor()
        # Get recommended players with their stats based on scout reports
        cursor.execute("""
            SELECT DISTINCT
                p.playerID,
                p.firstName,
                p.lastName,
                p.height,
                p.weight,
                ps.ptsPerGame,
                ps.rebPerGame,
                ps.astPerGame,
                d.metricDisplayed
            FROM Players p
                JOIN PlayerStats ps ON p.playerID = ps.playerID
                JOIN Exports e ON e.playerID = p.playerID
                JOIN ExportRequests er ON e.exportID = er.exportID
                JOIN MetricExports me ON me.exportID = er.exportID
                JOIN MetricFormula mf ON mf.formulaID = me.formulaID
                JOIN CalculatedMetrics cm ON cm.formulaID = mf.formulaID
                JOIN DashboardMetrics dm ON dm.metricID = cm.metricID
                JOIN Dashboard d ON d.dashboardID = dm.dashboardID
            WHERE p.playerID = %s AND d.recommendation IS NOT NULL
        """, (playerID,))
        
        stats = cursor.fetchall()
        cursor.close()
        
        if not stats:
            return jsonify({"message": "No recommended stats found for this player"}), 404
        
        return jsonify(stats), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Get all uploaded highlight videos for this player 
@scouts.route("/players/<int:playerID>/videos", methods=["GET"])
def get_player_videos(playerID):
    try:
        cursor = db.get_db().cursor()
        
        # Check if player exists 
        cursor.execute("SELECT playerID FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Player not found"}), 404
        
        # Get all videos for games this player played in
        cursor.execute("""
            SELECT DISTINCT
                f.footageID,
                f.gameID,
                f.URL,
                f.duration
            FROM Footage f
                JOIN Games g ON f.gameID = g.gameID
                JOIN PlayerSchedules ps ON g.gameID = ps.gameID
            WHERE ps.playerID = %s
            ORDER BY g.date DESC, f.footageID DESC
        """, (playerID,))
        
        videos = cursor.fetchall()
        cursor.close()
        
        if not videos:
            return jsonify({"message": "No videos found for this player"}), 200
        
        return jsonify(videos), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

# add footage to player reports 
@scouts.route('/<int:scout_id>/players/<int:player_id>/report/footage', methods=['POST'])
def add_footage_to_player_report(scout_id, player_id):
    try:
        data = request.json
        cursor = db.get_db().cursor()
        
        # Validate that scout exists
        cursor.execute("SELECT scoutID FROM Scouts WHERE scoutID = %s", (scout_id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({
                'success': False,
                'message': f'Scout {scout_id} not found'
            }), 404
        
        # Validate that player exists
        cursor.execute("SELECT playerID FROM Players WHERE playerID = %s", (player_id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({
                'success': False,
                'message': f'Player {player_id} not found'
            }), 404
        
        # Insert footage record
        cursor.execute("""
            INSERT INTO Footage 
            (gameID, URL, duration)
            VALUES (%s, %s, %s)
        """, (
            data.get('gameID'),
            data.get('URL'),
            data.get('duration')
        ))
        
        footage_id = cursor.lastrowid
        db.get_db().commit()
        cursor.close()
        
        return jsonify({
            'success': True,
            'message': 'Footage added successfully',
            'footageID': footage_id,
            'playerID': player_id,
            'scoutID': scout_id
        }), 201
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# returns future games that the player will be playing in 
@scouts.route('/players/<int:player_id>/future-games', methods=['GET'])
def get_player_future_games(player_id):
    """
    Returns future games that the player will be playing in
    """
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("""
            SELECT 
                g.gameID,
                g.date as gameDate,
                g.startTime,
                g.endTime,
                g.opponent,
                g.venue,
                g.tournament,
                g.score
            FROM Games g
            JOIN PlayerSchedules ps ON g.gameID = ps.gameID
            WHERE ps.playerID = %s 
            AND g.date >= CURDATE()
            ORDER BY g.date ASC, g.startTime ASC
        """, (player_id,))
        
        games = cursor.fetchall()
        cursor.close()
        
        if not games:
            return jsonify({
                'success': True,
                'playerID': player_id,
                'message': 'No future games scheduled',
                'games': []
            }), 200
        
        game_list = []
        for game in games:
            game_list.append({
                'gameID': game[0],
                'gameDate': game[1].strftime('%Y-%m-%d') if game[1] else None,
                'startTime': str(game[2]) if game[2] else None,
                'endTime': str(game[3]) if game[3] else None,
                'opponent': game[4],
                'venue': game[5],
                'tournament': game[6],
                'score': game[7]
            })
        
        return jsonify({
            'success': True,
            'playerID': player_id,
            'gameCount': len(game_list),
            'games': game_list
        }), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500

# add new annotation to game footage 
@scouts.route('/footage/<int:footage_id>/annotations', methods=['POST'])
def add_annotation_to_footage(footage_id):
    """
    Add new annotation to game footage
    """
    try:
        data = request.json
        cursor = db.get_db().cursor()
        
        # Validate that footage exists
        cursor.execute("SELECT footageID FROM Footage WHERE footageID = %s", (footage_id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({
                'success': False,
                'message': f'Footage {footage_id} not found'
            }), 404
        
        # Insert annotation
        cursor.execute("""
            INSERT INTO Annotations 
            (reportID, annotatedBy, timestamp, text, footageID)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get('reportID'),  # Optional - can be NULL
            data.get('annotatedBy'),  # Scout ID who is annotating
            data.get('timestamp'),  # Format: 'HH:MM:SS'
            data.get('text'),  # The annotation text
            footage_id
        ))
        
        annotation_id = cursor.lastrowid
        db.get_db().commit()
        cursor.close()
        
        return jsonify({
            'success': True,
            'message': 'Annotation added successfully',
            'annotationID': annotation_id,
            'footageID': footage_id
        }), 201
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

