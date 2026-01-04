from flask import Blueprint, request, jsonify
from backend.db_connection import db
import logging

logger = logging.getLogger(__name__)
admin = Blueprint('admin', __name__)


# ------------------------------------------------------------
# GET /reports - Generate reports for suspicious activity
# [Ryan Suri - 5]
@admin.route('/reports', methods=['GET'])
def get_reports():
    """Generate reports so suspicious activity can be detected"""
    logger.info('GET /reports route')

    query = '''
        SELECT reportID, reportName, reportType, 
               createdBy, createdDate, description, status
        FROM Reports
        ORDER BY createdDate DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    reports = cursor.fetchall()

    return jsonify(reports), 200


# ------------------------------------------------------------
# POST /reports - Create a new report
# [Ryan Suri - 5]
@admin.route('/reports', methods=['POST'])
def create_report():
    """Create a new system report"""
    logger.info('POST /reports route')

    data = request.json

    query = '''
        INSERT INTO Reports (reportName, reportType, createdBy, description, status)
        VALUES (%s, %s, %s, %s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('reportName'),
        data.get('reportType'),
        data.get('createdBy'),
        data.get('description'),
        data.get('status', 'active')
    ))
    db.get_db().commit()

    report_id = cursor.lastrowid

    return jsonify({
        'message': 'Report created successfully',
        'reportID': report_id
    }), 201


# ------------------------------------------------------------
# GET /players/<player_id>/verifications - Get player verifications
# [Ryan Suri - 2]
@admin.route('/players/<int:player_id>/verifications', methods=['GET'])
def get_player_verifications(player_id):
    """Get verification status for players joining the platform"""
    logger.info(f'GET /players/{player_id}/verifications route')

    query = '''
        SELECT v.validationID, v.playerID, v.verificationType,
               v.documentType, v.status, v.submittedDate,
               v.verifiedBy, v.verifiedDate, v.notes,
               p.firstName, p.lastName, p.email
        FROM Verification v
        JOIN Players p ON v.playerID = p.playerID
        WHERE v.playerID = %s
        ORDER BY v.submittedDate DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    verifications = cursor.fetchall()

    return jsonify(verifications), 200


# ------------------------------------------------------------
# POST /players/<player_id>/verifications - Create verification
# [Ryan Suri - 2]
@admin.route('/players/<int:player_id>/verifications', methods=['POST'])
def create_player_verification(player_id):
    """Create a verification request for a player"""
    logger.info(f'POST /players/{player_id}/verifications route')

    data = request.json

    query = '''
        INSERT INTO Verification (playerID, verificationType, documentType, 
                                 status, submittedDate)
        VALUES (%s, %s, %s, %s, CURDATE())
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        player_id,
        data.get('verificationType'),
        data.get('documentType'),
        data.get('status', 'pending')
    ))
    db.get_db().commit()

    verification_id = cursor.lastrowid

    return jsonify({
        'message': 'Verification request created successfully',
        'validationID': verification_id
    }), 201


# ------------------------------------------------------------
# PUT /players/<player_id>/verifications/<verification_id> - Update verification
# [Ryan Suri - 2]
@admin.route('/players/<int:player_id>/verifications/<int:verification_id>', methods=['PUT'])
def update_player_verification(player_id, verification_id):
    """Update verification status (approve/reject)"""
    logger.info(f'PUT /players/{player_id}/verifications/{verification_id} route')

    data = request.json

    query = '''
        UPDATE Verification
        SET status = %s, verifiedBy = %s, verifiedDate = CURDATE(), notes = %s
        WHERE validationID = %s AND playerID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('status'),
        data.get('verifiedBy'),
        data.get('notes'),
        verification_id,
        player_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Verification updated successfully'}), 200


# ------------------------------------------------------------
# GET /players/<player_id>/permissions - Get player permissions
# [Ryan Suri - 6]
@admin.route('/players/<int:player_id>/permissions', methods=['GET'])
def get_player_permissions(player_id):
    """Get player permissions for correct accessibility"""
    logger.info(f'GET /players/{player_id}/permissions route')

    query = '''
        SELECT playerID, AcctStatus, firstName, lastName, email
        FROM Players
        WHERE playerID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    permissions = cursor.fetchone()

    if not permissions:
        return jsonify({'error': 'Player not found'}), 404

    return jsonify(permissions), 200


# ------------------------------------------------------------
# PUT /players/<player_id>/permissions - Update player permissions
# [Ryan Suri - 6]
@admin.route('/players/<int:player_id>/permissions', methods=['PUT'])
def update_player_permissions(player_id):
    """Manage player permissions for correct accessibility"""
    logger.info(f'PUT /players/{player_id}/permissions route')

    data = request.json

    query = '''
        UPDATE Players
        SET AcctStatus = %s
        WHERE playerID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('AcctStatus'),
        player_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Player permissions updated successfully'}), 200


# ------------------------------------------------------------
# PUT /admin/users/players/<player_id>/permissions - Alternative route for managing player permissions
# Used by Manage Users page
@admin.route('/admin/users/players/<int:player_id>/permissions', methods=['PUT'])
def update_player_permissions_alt(player_id):
    """Manage player permissions (alternative route for admin UI)"""
    logger.info(f'PUT /admin/users/players/{player_id}/permissions route')

    data = request.json

    query = '''
        UPDATE Players
        SET AcctStatus = %s
        WHERE playerID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('AcctStatus'),
        player_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Player permissions updated successfully'}), 200


# ------------------------------------------------------------
# GET /admin/users - Get all users (players and scouts)
# [Ryan Suri - 1]
@admin.route('/admin/users', methods=['GET'])
def get_all_users():
    """Get all users for management"""
    logger.info('GET /admin/users route')

    user_type = request.args.get('type', 'all')

    users = {'players': [], 'scouts': []}

    cursor = db.get_db().cursor()

    if user_type in ['all', 'players']:
        cursor.execute('''
            SELECT playerID as id, firstName, lastName, email, 
                   AcctStatus as status, 'player' as user_type
            FROM Players
            ORDER BY lastName
        ''')
        users['players'] = cursor.fetchall()

    if user_type in ['all', 'scouts']:
        cursor.execute('''
            SELECT scoutID as id, firstName, lastName, email,
                   acctStatus as status, 'scout' as user_type
            FROM Scout
            ORDER BY lastName
        ''')
        users['scouts'] = cursor.fetchall()

    return jsonify(users), 200


# ------------------------------------------------------------
# GET /admin/pending-verifications - Get pending verifications
# [Ryan Suri - 2, 5]
@admin.route('/admin/pending-verifications', methods=['GET'])
def get_pending_verifications():
    """Get all pending verification requests"""
    logger.info('GET /admin/pending-verifications route')

    query = '''
        SELECT v.validationID, v.playerID, v.verificationType,
               v.documentType, v.status, v.submittedDate,
               p.firstName, p.lastName, p.email
        FROM Verification v
        JOIN Players p ON v.playerID = p.playerID
        WHERE v.status = 'pending'
        ORDER BY v.submittedDate ASC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    pending = cursor.fetchall()

    return jsonify(pending), 200


# ------------------------------------------------------------
# GET /admin/flagged-accounts - Get flagged accounts
# [Ryan Suri - 3, 5]
@admin.route('/admin/flagged-accounts', methods=['GET'])
def get_flagged_accounts():
    """Get all flagged accounts for review"""
    logger.info('GET /admin/flagged-accounts route')

    query = '''
        SELECT ur.reportID, ur.reportedUserID, ur.reportedUserType,
               ur.reason, ur.severity, ur.status, ur.reportDate
        FROM UserReported ur
        WHERE ur.status IN ('pending', 'under_review')
        ORDER BY ur.severity DESC, ur.reportDate ASC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    flagged = cursor.fetchall()

    return jsonify(flagged), 200


# ------------------------------------------------------------
# POST /admin/flag-user - Flag a user
# [Ryan Suri - 5]
@admin.route('/admin/flag-user', methods=['POST'])
def flag_user():
    """Flag a user for suspicious activity"""
    logger.info('POST /admin/flag-user route')

    data = request.json

    query = '''
        INSERT INTO UserReported (reportedBy, reportedUserID, reportedUserType,
                                 reason, severity, status)
        VALUES (%s, %s, %s, %s, %s, 'pending')
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('reportedBy'),
        data.get('reportedUserID'),
        data.get('reportedUserType'),
        data.get('reason'),
        data.get('severity', 'medium')
    ))
    db.get_db().commit()

    return jsonify({'message': 'User flagged successfully'}), 201


# ------------------------------------------------------------
# GET /admin/statistics - Get system statistics
# [Ryan Suri - 5]
@admin.route('/admin/statistics', methods=['GET'])
def get_system_statistics():
    """Get overall system statistics"""
    logger.info('GET /admin/statistics route')

    cursor = db.get_db().cursor()

    stats = {}

    # Total players
    cursor.execute('SELECT COUNT(*) as count FROM Players')
    stats['total_players'] = cursor.fetchone()['count']

    # Total scouts
    cursor.execute('SELECT COUNT(*) as count FROM Scout')
    stats['total_scouts'] = cursor.fetchone()['count']

    # Total games
    cursor.execute('SELECT COUNT(*) as count FROM Game')
    stats['total_games'] = cursor.fetchone()['count']

    # Pending verifications
    cursor.execute("SELECT COUNT(*) as count FROM Verification WHERE status = 'pending'")
    stats['pending_verifications'] = cursor.fetchone()['count']

    # Flagged accounts
    cursor.execute("SELECT COUNT(*) as count FROM UserReported WHERE status IN ('pending', 'under_review')")
    stats['flagged_accounts'] = cursor.fetchone()['count']

    return jsonify(stats), 200