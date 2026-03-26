from flask import Blueprint, request, jsonify
from backend.db_connection import db
import logging

logger = logging.getLogger(__name__)
scouts = Blueprint('scouts', __name__)


# ------------------------------------------------------------
# GET /scouts/<scout_id>/player_history - Get scouted players list
# [Sara Chin - 6]
@scouts.route('/scouts/<int:scout_id>/player_history', methods=['GET'])
def get_scout_player_history(scout_id):
    """Returns a list of players that the scout has scouted"""
    logger.info(f'GET /scouts/{scout_id}/player_history route')

    query = '''
        SELECT DISTINCT p.playerID, p.firstName, p.lastName,
               ps.position, t.team_name,
               COUNT(pr.reportID) as total_reports
        FROM PlayerReports pr
        JOIN Players p ON pr.playerID = p.playerID
        LEFT JOIN Playsin ps ON p.playerID = ps.playerID
        LEFT JOIN Team t ON ps.team_id = t.team_id
        WHERE pr.scoutID = %s
        GROUP BY p.playerID, p.firstName, p.lastName, ps.position, t.team_name
        ORDER BY total_reports DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (scout_id,))
    players = cursor.fetchall()

    return jsonify(players), 200


# ------------------------------------------------------------
# GET /scouts/<scout_id>/game_history - Get attended games list
# [Sara Chin - 6]
@scouts.route('/scouts/<int:scout_id>/game_history', methods=['GET'])
def get_scout_game_history(scout_id):
    """Returns a list of games that the scout has attended"""
    logger.info(f'GET /scouts/{scout_id}/game_history route')

    query = '''
        SELECT g.gameID, g.date, g.startTime, g.opponent, 
               g.venue, g.score, sa.gamesAttended, sa.notes
        FROM Scout_Activity sa
        JOIN Game g ON sa.gameID = g.gameID
        WHERE sa.scoutID = %s
        ORDER BY g.date DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (scout_id,))
    games = cursor.fetchall()

    return jsonify(games), 200


# ------------------------------------------------------------
# GET /scouts/<scout_id>/verifications - Get scout verifications
# [Ryan Suri - 2]
@scouts.route('/scouts/<int:scout_id>/verifications', methods=['GET'])
def get_scout_verifications(scout_id):
    """Get verification status for scouts"""
    logger.info(f'GET /scouts/{scout_id}/verifications route')

    query = '''
        SELECT scoutID, firstName, lastName, email, 
               acctStatus, role, dateOfBirth, age
        FROM Scout
        WHERE scoutID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (scout_id,))
    scout = cursor.fetchone()

    if not scout:
        return jsonify({'error': 'Scout not found'}), 404

    return jsonify(scout), 200


# ------------------------------------------------------------
# PUT /scouts/<scout_id> - Update scout profile
# [Ryan Suri - 1]
@scouts.route('/scouts/<int:scout_id>', methods=['PUT'])
def update_scout_profile(scout_id):
    """Update scout profiles"""
    logger.info(f'PUT /scouts/{scout_id} route')

    data = request.json

    query = '''
        UPDATE Scout
        SET firstName = %s, lastName = %s, email = %s,
            phoneNum = %s, role = %s, acctStatus = %s
        WHERE scoutID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('firstName'),
        data.get('lastName'),
        data.get('email'),
        data.get('phoneNum'),
        data.get('role'),
        data.get('acctStatus'),
        scout_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Scout profile updated successfully'}), 200


# ------------------------------------------------------------
# DELETE /scouts/<scout_id> - Remove scout (fraud)
# [Ryan Suri - 3]
@scouts.route('/scouts/<int:scout_id>', methods=['DELETE'])
def delete_scout(scout_id):
    """Remove scouts that commit fraud or misinformation"""
    logger.info(f'DELETE /scouts/{scout_id} route')

    cursor = db.get_db().cursor()
    query = 'DELETE FROM Scout WHERE scoutID = %s'
    cursor.execute(query, (scout_id,))
    db.get_db().commit()

    return jsonify({'message': 'Scout removed successfully'}), 200


# ------------------------------------------------------------
# GET /scouts/<scout_id>/permissions - Get scout permissions
# [Ryan Suri - 6]
@scouts.route('/scouts/<int:scout_id>/permissions', methods=['GET'])
def get_scout_permissions(scout_id):
    """Get scout permissions for accessibility"""
    logger.info(f'GET /scouts/{scout_id}/permissions route')

    query = '''
        SELECT scoutID, role, acctStatus
        FROM Scout
        WHERE scoutID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (scout_id,))
    permissions = cursor.fetchone()

    if not permissions:
        return jsonify({'error': 'Scout not found'}), 404

    return jsonify(permissions), 200


# ------------------------------------------------------------
# PUT /scouts/<scout_id>/permissions - Update scout permissions
# [Ryan Suri - 6]
@scouts.route('/scouts/<int:scout_id>/permissions', methods=['PUT'])
def update_scout_permissions(scout_id):
    """Manage scout permissions for accessibility"""
    logger.info(f'PUT /scouts/{scout_id}/permissions route')

    data = request.json

    query = '''
        UPDATE Scout
        SET role = %s, acctStatus = %s
        WHERE scoutID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('role'),
        data.get('acctStatus'),
        scout_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Scout permissions updated successfully'}), 200


# ------------------------------------------------------------
# POST /footages/<footage_id>/annotation - Add annotation (OLD - DEPRECATED)
# [Sara Chin - 2]
@scouts.route('/footages/<int:footage_id>/annotation', methods=['POST'])
def add_footage_annotation(footage_id):
    """Add new annotation to game footage"""
    logger.info(f'POST /footages/{footage_id}/annotation route')

    data = request.json

    query = '''
        INSERT INTO Annotations (reportID, annotatedBy, text, timestamp)
        VALUES (%s, %s, %s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('reportID'),
        data.get('annotatedBy'),  # scout_id
        data.get('text'),
        data.get('timestamp')
    ))
    db.get_db().commit()

    return jsonify({'message': 'Annotation added successfully'}), 201


# ------------------------------------------------------------
# POST /scouts/<scout_id>/annotations - Add live game annotation (NEW)
# [Sara Chin - 2]
@scouts.route('/scouts/<int:scout_id>/annotations', methods=['POST'])
def add_live_annotation(scout_id):
    """
    Add annotation during live game scouting.
    Creates placeholder report if needed.
    """
    logger.info(f'POST /scouts/{scout_id}/annotations route')

    data = request.json
    cursor = db.get_db().cursor()

    try:
        player_id = data.get('playerID') or 1  # Default to player 1 for general notes

        # Check if report exists for this scout/player
        cursor.execute('''
            SELECT reportID 
            FROM PlayerReports 
            WHERE scoutID = %s AND playerID = %s
            LIMIT 1
        ''', (scout_id, player_id))

        existing_report = cursor.fetchone()

        if existing_report:
            report_id = existing_report['reportID']
        else:
            # Create placeholder report
            cursor.execute('''
                INSERT INTO PlayerReports (playerID, scoutID, summary, strengths, weaknesses)
                VALUES (%s, %s, 'Live scouting session', '', '')
            ''', (player_id, scout_id))
            report_id = cursor.lastrowid

        # Insert annotation
        cursor.execute('''
            INSERT INTO Annotations (reportID, annotatedBy, text, timestamp)
            VALUES (%s, %s, %s, %s)
        ''', (
            report_id,
            scout_id,
            data.get('text'),
            data.get('timestamp', '00:00:00')
        ))

        db.get_db().commit()

        return jsonify({
            'message': 'Annotation added successfully',
            'annotationID': cursor.lastrowid,
            'reportID': report_id
        }), 201

    except Exception as e:
        logger.error(f'Error adding annotation: {str(e)}')
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500


# ------------------------------------------------------------
# GET /games/<game_id>/annotations - Get all annotations for a game
# [Sara Chin - 2]
@scouts.route('/games/<int:game_id>/annotations', methods=['GET'])
def get_game_annotations(game_id):
    """Get all annotations made during a specific game"""
    logger.info(f'GET /games/{game_id}/annotations route')

    query = '''
        SELECT a.annotationID, a.text, a.timestamp,
               s.firstName as scout_first, s.lastName as scout_last,
               p.firstName as player_first, p.lastName as player_last
        FROM Annotations a
        JOIN Scout s ON a.annotatedBy = s.scoutID
        JOIN PlayerReports pr ON a.reportID = pr.reportID
        LEFT JOIN Players p ON pr.playerID = p.playerID
        ORDER BY a.timestamp ASC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    annotations = cursor.fetchall()

    return jsonify(annotations), 200


# ------------------------------------------------------------
# GET /players/<player_id>/schedule - Get player's future games
# [Sara Chin - 5]
@scouts.route('/players/<int:player_id>/schedule', methods=['GET'])
def get_player_schedule(player_id):
    """Returns future games that the player will be playing in"""
    logger.info(f'GET /players/{player_id}/schedule route')

    query = '''
        SELECT g.gameID, g.date, g.startTime, g.opponent, 
               g.venue, g.tournament
        FROM PlayerSchedule ps
        JOIN Game g ON ps.gameID = g.gameID
        WHERE ps.playerID = %s 
          AND g.date >= CURDATE()
        ORDER BY g.date ASC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    schedule = cursor.fetchall()

    return jsonify(schedule), 200


# ------------------------------------------------------------
# GET /players/<player_id>/stats/filtered - Get filtered stats
# [Sara Chin - 1]
@scouts.route('/players/<int:player_id>/stats/filtered', methods=['GET'])
def get_filtered_player_stats(player_id):
    """Returns player stats recommended by data analyst scout"""
    logger.info(f'GET /players/{player_id}/stats/filtered route')

    # Get query parameters for filtering
    min_points = request.args.get('min_points', 0)
    min_assists = request.args.get('min_assists', 0)

    query = '''
        SELECT gs.gameID, g.date, g.opponent,
               gs.points, gs.rebounds, gs.assists, gs.steals,
               gs.blocks, gs.minutes
        FROM Game_Stats gs
        JOIN Game g ON gs.gameID = g.gameID
        WHERE gs.playerID = %s
          AND gs.points >= %s
          AND gs.assists >= %s
        ORDER BY gs.points DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id, min_points, min_assists))
    stats = cursor.fetchall()

    return jsonify(stats), 200


# ------------------------------------------------------------
# POST /players/<player_id>/report/footage - Add footage to report
# [Sara Chin - 4]
@scouts.route('/players/<int:player_id>/report/footage', methods=['POST'])
def add_report_footage(player_id):
    """Add footage to player reports"""
    logger.info(f'POST /players/{player_id}/report/footage route')

    data = request.json

    query = '''
        INSERT INTO Footage (gameID, playerID, URL, duration)
        VALUES (%s, %s, %s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('gameID'),
        player_id,
        data.get('URL'),
        data.get('duration')
    ))
    db.get_db().commit()

    return jsonify({'message': 'Footage added to report successfully'}), 201

# ------------------------------------------------------------
# POST /scouts/<scout_id>/schedule - Add game to scout's schedule
# [Sara Chin - 5]
@scouts.route('/scouts/<int:scout_id>/schedule', methods=['POST'])
def add_scout_schedule(scout_id):
    """Add game to scout's schedule"""
    logger.info(f'POST /scouts/{scout_id}/schedule route')

    data = request.json
    cursor = db.get_db().cursor()

    try:
        # Insert into Scout_Activity
        query = '''
            INSERT INTO Scout_Activity (scoutID, gameID, gamesAttended, notes)
            VALUES (%s, %s, 1, %s)
        '''
        cursor.execute(query, (
            scout_id,
            data.get('gameID'),
            data.get('notes', '')
        ))

        db.get_db().commit()

        logger.info(f'Game {data.get("gameID")} added to scout {scout_id} schedule')

        return jsonify({
            'message': 'Game added to schedule successfully',
            'scoutID': scout_id,
            'gameID': data.get('gameID')
        }), 201

    except Exception as e:
        logger.error(f'Error adding to schedule: {str(e)}')
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500