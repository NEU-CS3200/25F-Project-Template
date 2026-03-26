from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db
import logging

logger = logging.getLogger(__name__)
players = Blueprint('players', __name__)


# ------------------------------------------------------------
# GET /players/<player_id> - Get player profile
# [Sean-4]
@players.route('/players/<int:player_id>', methods=['GET'])
def get_player_profile(player_id):
    """Return full profile info for this player (bio, height, position, team)"""
    logger.info(f'GET /players/{player_id} route')

    query = '''
        SELECT p.playerID, p.firstName, p.lastName, p.email, p.phone_Number,
               p.UserBio, p.DateofBirth, p.height, p.weight, p.AcctStatus,
               t.team_name, t.city as team_city, ps.position, ps.jerseyNumber
        FROM Players p
        LEFT JOIN Playsin ps ON p.playerID = ps.playerID
        LEFT JOIN Team t ON ps.team_id = t.team_id
        WHERE p.playerID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'Player not found'}), 404

    return jsonify(result), 200


# ------------------------------------------------------------
# PUT /players/<player_id> - Update player profile
# [Sean-4]
@players.route('/players/<int:player_id>', methods=['PUT'])
def update_player_profile(player_id):
    """Update profile information (bio, height, team, etc.)"""
    logger.info(f'PUT /players/{player_id} route')

    data = request.json

    query = '''
        UPDATE Players 
        SET firstName = %s, lastName = %s, email = %s, 
            phone_Number = %s, UserBio = %s, height = %s, weight = %s
        WHERE playerID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('firstName'),
        data.get('lastName'),
        data.get('email'),
        data.get('phone_Number'),
        data.get('UserBio'),
        data.get('height'),
        data.get('weight'),
        player_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Player profile updated successfully'}), 200


# ------------------------------------------------------------
# DELETE /players/<player_id> - Remove player (fraud/misinformation)
# [Ryan Suri - 3]
@players.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    """Remove players that commit fraud or misinformation"""
    logger.info(f'DELETE /players/{player_id} route')

    cursor = db.get_db().cursor()

    # Delete player (cascade will handle related records)
    query = 'DELETE FROM Players WHERE playerID = %s'
    cursor.execute(query, (player_id,))
    db.get_db().commit()

    return jsonify({'message': 'Player removed successfully'}), 200


# ------------------------------------------------------------
# GET /players/<player_id>/stats - Get player stats
# [Sean-1]
@players.route('/players/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """Return all game stats for this player across the season"""
    logger.info(f'GET /players/{player_id}/stats route')

    query = '''
        SELECT gs.gameID, g.date, g.opponent, g.venue,
               gs.minutes, gs.points, gs.rebounds, gs.assists,
               gs.steals, gs.blocks, gs.turnovers, gs.fouls, gs.three_pt
        FROM Game_Stats gs
        JOIN Game g ON gs.gameID = g.gameID
        WHERE gs.playerID = %s
        ORDER BY g.date DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    stats = cursor.fetchall()

    return jsonify(stats), 200


# ------------------------------------------------------------
# POST /players/<player_id>/stats - Add game statistics
# [Sean-1]
@players.route('/players/<int:player_id>/stats', methods=['POST'])
def add_player_stats(player_id):
    """Add a new game's statistics for this player"""
    logger.info(f'POST /players/{player_id}/stats route')

    data = request.json

    query = '''
        INSERT INTO Game_Stats (gameID, playerID, minutes, points, rebounds, 
                               assists, steals, blocks, turnovers, fouls, three_pt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('gameID'),
        player_id,
        data.get('minutes'),
        data.get('points'),
        data.get('rebounds'),
        data.get('assists'),
        data.get('steals'),
        data.get('blocks'),
        data.get('turnovers'),
        data.get('fouls'),
        data.get('three_pt')
    ))
    db.get_db().commit()

    return jsonify({'message': 'Stats added successfully'}), 201


# ------------------------------------------------------------
# POST /players/<player_id>/game-and-stats - Add NEW game + stats
# [Sean-1] - Enhanced version that creates game first
@players.route('/players/<int:player_id>/game-and-stats', methods=['POST'])
def add_game_and_stats(player_id):
    """
    Add a new game and the player's stats for that game in one operation.
    This is useful when a player wants to log a game that isn't in the system yet.
    """
    logger.info(f'POST /players/{player_id}/game-and-stats route')

    data = request.json
    cursor = db.get_db().cursor()

    try:
        # Step 1: Create the game
        game_query = '''
            INSERT INTO Game (date, startTime, endTime, opponent, venue, tournament, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(game_query, (
            data['date'],
            data.get('startTime', '00:00:00'),
            data.get('endTime', '00:00:00'),
            data['opponent'],
            data['venue'],
            data.get('tournament', ''),
            data.get('score', '')
        ))

        # Step 2: Get the new gameID that was just created
        new_game_id = cursor.lastrowid
        logger.info(f'Created new game with ID: {new_game_id}')

        # Step 3: Insert the player's stats for that game
        stats_query = '''
            INSERT INTO Game_Stats (gameID, playerID, minutes, points, rebounds, assists, steals, blocks, turnovers, fouls, three_pt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(stats_query, (
            new_game_id,
            player_id,
            data['minutes'],
            data['points'],
            data['rebounds'],
            data['assists'],
            data['steals'],
            data['blocks'],
            data['turnovers'],
            data['fouls'],
            data['three_pt']
        ))

        # CRITICAL: Commit the changes!
        db.get_db().commit()

        logger.info(f'Successfully added game {new_game_id} and stats for player {player_id}')

        return jsonify({
            'message': 'Game and stats added successfully',
            'gameID': new_game_id,
            'playerID': player_id
        }), 201

    except Exception as e:
        # If anything goes wrong, rollback
        logger.error(f'Error adding game and stats: {str(e)}')
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500


# ------------------------------------------------------------
# PUT /players/<player_id>/stats - Update player stats (admin)
# [Ryan Suri - 1]
@players.route('/players/<int:player_id>/stats/<int:game_id>', methods=['PUT'])
def update_player_stats(player_id, game_id):
    """Update player profiles/stats"""
    logger.info(f'PUT /players/{player_id}/stats/{game_id} route')

    data = request.json

    query = '''
        UPDATE Game_Stats 
        SET minutes = %s, points = %s, rebounds = %s, assists = %s,
            steals = %s, blocks = %s, turnovers = %s, fouls = %s, three_pt = %s
        WHERE playerID = %s AND gameID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('minutes'),
        data.get('points'),
        data.get('rebounds'),
        data.get('assists'),
        data.get('steals'),
        data.get('blocks'),
        data.get('turnovers'),
        data.get('fouls'),
        data.get('three_pt'),
        player_id,
        game_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Stats updated successfully'}), 200


# ------------------------------------------------------------
# DELETE /players/<player_id>/stats/<game_id> - Remove fraudulent stats
# [Ryan Suri - 4]
@players.route('/players/<int:player_id>/stats/<int:game_id>', methods=['DELETE'])
def delete_fraudulent_stats(player_id, game_id):
    """Remove fraudulent statistics"""
    logger.info(f'DELETE /players/{player_id}/stats/{game_id} route')

    cursor = db.get_db().cursor()
    query = 'DELETE FROM Game_Stats WHERE playerID = %s AND gameID = %s'
    cursor.execute(query, (player_id, game_id))
    db.get_db().commit()

    return jsonify({'message': 'Fraudulent stats removed successfully'}), 200


# ------------------------------------------------------------
# GET /players/<player_id>/videos - Get player videos
# [Player-2], [Sara Chin - 2]
@players.route('/players/<int:player_id>/videos', methods=['GET'])
def get_player_videos(player_id):
    """Return all uploaded highlight videos for this player"""
    logger.info(f'GET /players/{player_id}/videos route')

    query = '''
        SELECT f.footageID, f.URL, f.duration, g.date, g.opponent
        FROM Footage f
        JOIN Game g ON f.gameID = g.gameID
        WHERE f.playerID = %s
        ORDER BY g.date DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    videos = cursor.fetchall()

    return jsonify(videos), 200


# ------------------------------------------------------------
# POST /players/<player_id>/videos - Upload highlight video
# [Sean-2]
@players.route('/players/<int:player_id>/videos', methods=['POST'])
def upload_player_video(player_id):
    """Upload a new highlight video (URL or file reference)"""
    logger.info(f'POST /players/{player_id}/videos route')

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

    return jsonify({'message': 'Video uploaded successfully'}), 201


# ------------------------------------------------------------
# GET /players/<player_id>/feedback - Get scout feedback
# [Sean-3]
@players.route('/players/<int:player_id>/feedback', methods=['GET'])
def get_player_feedback(player_id):
    """Return feedback written by scouts for this player"""
    logger.info(f'GET /players/{player_id}/feedback route')

    query = '''
        SELECT pr.reportID, pr.summary, pr.strengths, pr.weaknesses,
               s.firstName as scout_first, s.lastName as scout_last,
               s.role
        FROM PlayerReports pr
        JOIN Scout s ON pr.scoutID = s.scoutID
        WHERE pr.playerID = %s
        ORDER BY pr.reportID DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    feedback = cursor.fetchall()

    return jsonify(feedback), 200


# ------------------------------------------------------------
# GET /players/<player_id>/comparisons - Compare to similar players
# [Sean-5]
@players.route('/players/<int:player_id>/comparisons', methods=['GET'])
def get_player_comparisons(player_id):
    """Return comparison of this player's stats to similar players"""
    logger.info(f'GET /players/{player_id}/comparisons route')

    # First get the target player's info
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT height, ps.position
        FROM Players p
        LEFT JOIN Playsin ps ON p.playerID = ps.playerID
        WHERE p.playerID = %s
    ''', (player_id,))

    player_info = cursor.fetchone()

    if not player_info:
        return jsonify({'error': 'Player not found'}), 404

    # Get similar players with their stats
    query = '''
        SELECT p.playerID, p.firstName, p.lastName,
               AVG(gs.points) as avg_points,
               AVG(gs.rebounds) as avg_rebounds,
               AVG(gs.assists) as avg_assists,
               AVG(gs.steals) as avg_steals
        FROM Players p
        JOIN Playsin ps ON p.playerID = ps.playerID
        JOIN Game_Stats gs ON p.playerID = gs.playerID
        WHERE ps.position = %s 
          AND p.height BETWEEN %s - 2 AND %s + 2
          AND p.playerID != %s
        GROUP BY p.playerID, p.firstName, p.lastName
        LIMIT 10
    '''

    cursor.execute(query, (
        player_info['position'],
        player_info['height'],
        player_info['height'],
        player_id
    ))
    similar_players = cursor.fetchall()

    return jsonify(similar_players), 200


# ------------------------------------------------------------
# GET /players/<player_id>/recruiting - Get recruiting schools
# [Sean-6]
@players.route('/players/<int:player_id>/recruiting', methods=['GET'])
def get_recruiting_schools(player_id):
    """Return list of schools recruiting players with similar profiles"""
    logger.info(f'GET /players/{player_id}/recruiting route')

    query = '''
        SELECT DISTINCT s.schoolID, s.name, s.city, s.state,
               COUNT(o.offerID) as total_offers
        FROM School s
        JOIN Offers o ON s.schoolID = o.schoolID
        WHERE o.status = 'active'
        GROUP BY s.schoolID, s.name, s.city, s.state
        ORDER BY total_offers DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    schools = cursor.fetchall()

    return jsonify(schools), 200


# ------------------------------------------------------------
# GET /players/<player_id>/schedule - Get player's upcoming games
# [Sara Chin - 5]
@players.route('/players/<int:player_id>/schedule', methods=['GET'])
def get_player_schedule(player_id):
    """Returns future games that the player will be playing in"""
    logger.info(f'GET /players/{player_id}/schedule route')

    query = '''
        SELECT g.gameID, g.date, g.startTime, g.opponent, g.venue, g.tournament
        FROM Game g
        JOIN PlayerSchedule ps ON g.gameID = ps.gameID
        WHERE ps.playerID = %s AND g.date >= CURDATE()
        ORDER BY g.date ASC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    schedule = cursor.fetchall()

    return jsonify(schedule), 200


# ------------------------------------------------------------
# GET /players/stats/aggregate - Get aggregated player stats with filters
# [John Tukey - 1, 4]
@players.route('/players/stats/aggregate', methods=['GET'])
def get_aggregate_player_stats():
    """
    Return clean, standardized datasets for analysis.
    Supports filtering by position, competition level, etc.
    """
    logger.info('GET /players/stats/aggregate route')

    # Get query parameters for filtering
    position = request.args.get('position')
    min_points = request.args.get('min_points', 0)

    query = '''
        SELECT 
            p.playerID,
            p.firstName,
            p.lastName,
            ps.position,
            COUNT(DISTINCT gs.gameID) as games_played,
            AVG(gs.points) as avg_points,
            AVG(gs.rebounds) as avg_rebounds,
            AVG(gs.assists) as avg_assists,
            AVG(gs.steals) as avg_steals
        FROM Players p
        JOIN Playsin ps ON p.playerID = ps.playerID
        JOIN Game_Stats gs ON p.playerID = gs.playerID
        WHERE 1=1
    '''

    params = []

    if position:
        query += ' AND ps.position = %s'
        params.append(position)

    query += '''
        GROUP BY p.playerID, p.firstName, p.lastName, ps.position
        HAVING AVG(gs.points) >= %s
        ORDER BY avg_points DESC
    '''
    params.append(min_points)

    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    stats = cursor.fetchall()

    return jsonify(stats), 200