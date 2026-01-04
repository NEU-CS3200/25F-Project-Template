from flask import Blueprint, request, jsonify
from backend.db_connection import db
import logging

logger = logging.getLogger(__name__)
analytics = Blueprint('analytics', __name__)


# ------------------------------------------------------------
# GET /analytics/datasets - Get clean standardized datasets
# [Tukey-1]
@analytics.route('/analytics/datasets', methods=['GET'])
def get_clean_datasets():
    """Return clean, standardized game and player statistics with validation status filters"""
    logger.info('GET /analytics/datasets route')

    query = '''
        SELECT gs.gameID, gs.playerID, g.date, g.opponent,
               p.firstName, p.lastName,
               gs.minutes, gs.points, gs.rebounds, gs.assists,
               gs.steals, gs.blocks, gs.turnovers, gs.fouls
        FROM Game_Stats gs
        JOIN Game g ON gs.gameID = g.gameID
        JOIN Players p ON gs.playerID = p.playerID
        ORDER BY g.date DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    datasets = cursor.fetchall()

    return jsonify(datasets), 200


# ------------------------------------------------------------
# POST /analytics/datasets/export - Export data
# [Tukey-5]
@analytics.route('/analytics/datasets/export', methods=['POST'])
def export_datasets():
    """Request data export in specified format (CSV, JSON, Excel)"""
    logger.info('POST /analytics/datasets/export route')

    data = request.json

    query = '''
        INSERT INTO ExportRequest (requestedBy, requestedUserType, format, dataType, status)
        VALUES (%s, %s, %s, %s, 'pending')
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('requestedBy'),
        data.get('requestedUserType', 'analyst'),
        data.get('format', 'CSV'),
        data.get('dataType', 'Player Stats')
    ))
    db.get_db().commit()

    export_id = cursor.lastrowid

    return jsonify({
        'message': 'Export request created successfully',
        'exportID': export_id
    }), 201


# ------------------------------------------------------------
# GET /analytics/metrics - Get all custom metrics
# [Tukey-2]
@analytics.route('/analytics/metrics', methods=['GET'])
def get_all_metrics():
    """Return list of all custom metric formulas"""
    logger.info('GET /analytics/metrics route')

    query = '''
        SELECT formulaID, formulaName, createdBy, dateCreated
        FROM MetricsFormulas
        ORDER BY dateCreated DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    metrics = cursor.fetchall()

    return jsonify(metrics), 200


# ------------------------------------------------------------
# POST /analytics/metrics - Create custom metric
# [Tukey-2]
@analytics.route('/analytics/metrics', methods=['POST'])
def create_custom_metric():
    """Create new custom metric formula"""
    logger.info('POST /analytics/metrics route')

    data = request.json

    query = '''
        INSERT INTO MetricsFormulas (formulaName, createdBy)
        VALUES (%s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('formulaName'),
        data.get('createdBy')
    ))
    db.get_db().commit()

    formula_id = cursor.lastrowid

    return jsonify({
        'message': 'Metric formula created successfully',
        'formulaID': formula_id
    }), 201


# ------------------------------------------------------------
# PUT /analytics/metrics/<formula_id> - Update metric formula
# [Tukey-2]
@analytics.route('/analytics/metrics/<int:formula_id>', methods=['PUT'])
def update_metric_formula(formula_id):
    """Update existing metric formula definition"""
    logger.info(f'PUT /analytics/metrics/{formula_id} route')

    data = request.json

    query = '''
        UPDATE MetricsFormulas
        SET formulaName = %s
        WHERE formulaID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('formulaName'),
        formula_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Metric formula updated successfully'}), 200


# ------------------------------------------------------------
# DELETE /analytics/metrics/<formula_id> - Delete metric formula
# [Tukey-2]
@analytics.route('/analytics/metrics/<int:formula_id>', methods=['DELETE'])
def delete_metric_formula(formula_id):
    """Remove custom metric formula"""
    logger.info(f'DELETE /analytics/metrics/{formula_id} route')

    cursor = db.get_db().cursor()
    query = 'DELETE FROM MetricsFormulas WHERE formulaID = %s'
    cursor.execute(query, (formula_id,))
    db.get_db().commit()

    return jsonify({'message': 'Metric formula deleted successfully'}), 200


# ------------------------------------------------------------
# POST /analytics/metrics/<formula_id>/calculate - Calculate metric
# [Tukey-2]
@analytics.route('/analytics/metrics/<int:formula_id>/calculate', methods=['POST'])
def calculate_metric(formula_id):
    """Execute metric calculation on specified player/game data"""
    logger.info(f'POST /analytics/metrics/{formula_id}/calculate route')

    data = request.json

    query = '''
        INSERT INTO CalculatedMetrics (gameID, playerID, formulaID, metricName)
        VALUES (%s, %s, %s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('gameID'),
        data.get('playerID'),
        formula_id,
        data.get('metricName')
    ))
    db.get_db().commit()

    return jsonify({'message': 'Metric calculated successfully'}), 201


# ------------------------------------------------------------
# GET /analytics/dashboards - Get all dashboards
# [Tukey-3]
@analytics.route('/analytics/dashboards', methods=['GET'])
def get_all_dashboards():
    """Return list of all dashboards"""
    logger.info('GET /analytics/dashboards route')

    query = '''
        SELECT dashboardID, dashboardName, metricDisplayed, 
               chartType, lastUpdated
        FROM Dashboard
        ORDER BY lastUpdated DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    dashboards = cursor.fetchall()

    return jsonify(dashboards), 200


# ------------------------------------------------------------
# POST /analytics/dashboards - Create dashboard
# [Tukey-3]
@analytics.route('/analytics/dashboards', methods=['POST'])
def create_dashboard():
    """Create new dashboard with specified metrics and chart types"""
    logger.info('POST /analytics/dashboards route')

    data = request.json

    query = '''
        INSERT INTO Dashboard (dashboardName, metricDisplayed, chartType, filterCriteria)
        VALUES (%s, %s, %s, %s)
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('dashboardName'),
        data.get('metricDisplayed'),
        data.get('chartType'),
        data.get('filterCriteria')
    ))
    db.get_db().commit()

    dashboard_id = cursor.lastrowid

    return jsonify({
        'message': 'Dashboard created successfully',
        'dashboardID': dashboard_id
    }), 201


# ------------------------------------------------------------
# PUT /analytics/dashboards/<dashboard_id> - Update dashboard
# [Tukey-3]
@analytics.route('/analytics/dashboards/<int:dashboard_id>', methods=['PUT'])
def update_dashboard(dashboard_id):
    """Update dashboard configuration, metrics, or filters"""
    logger.info(f'PUT /analytics/dashboards/{dashboard_id} route')

    data = request.json

    query = '''
        UPDATE Dashboard
        SET dashboardName = %s, metricDisplayed = %s, 
            chartType = %s, filterCriteria = %s
        WHERE dashboardID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (
        data.get('dashboardName'),
        data.get('metricDisplayed'),
        data.get('chartType'),
        data.get('filterCriteria'),
        dashboard_id
    ))
    db.get_db().commit()

    return jsonify({'message': 'Dashboard updated successfully'}), 200


# ------------------------------------------------------------
# DELETE /analytics/dashboards/<dashboard_id> - Delete dashboard
# [Tukey-3]
@analytics.route('/analytics/dashboards/<int:dashboard_id>', methods=['DELETE'])
def delete_dashboard(dashboard_id):
    """Remove dashboard"""
    logger.info(f'DELETE /analytics/dashboards/{dashboard_id} route')

    cursor = db.get_db().cursor()
    query = 'DELETE FROM Dashboard WHERE dashboardID = %s'
    cursor.execute(query, (dashboard_id,))
    db.get_db().commit()

    return jsonify({'message': 'Dashboard deleted successfully'}), 200


# ------------------------------------------------------------
# GET /analytics/dashboards/<dashboard_id> - Get dashboard data
# [Tukey-3]
@analytics.route('/analytics/dashboards/<int:dashboard_id>', methods=['GET'])
def get_dashboard_data(dashboard_id):
    """Return complete dashboard data including all calculated metrics"""
    logger.info(f'GET /analytics/dashboards/{dashboard_id} route')

    query = '''
        SELECT d.dashboardID, d.dashboardName, d.metricDisplayed,
               d.chartType, d.lastUpdated, d.filterCriteria
        FROM Dashboard d
        WHERE d.dashboardID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (dashboard_id,))
    dashboard = cursor.fetchone()

    if not dashboard:
        return jsonify({'error': 'Dashboard not found'}), 404

    return jsonify(dashboard), 200


# ------------------------------------------------------------
# POST /analytics/dashboards/<dashboard_id>/refresh - Refresh dashboard
# [Tukey-3]
@analytics.route('/analytics/dashboards/<int:dashboard_id>/refresh', methods=['POST'])
def refresh_dashboard(dashboard_id):
    """Trigger recalculation of all metrics in dashboard"""
    logger.info(f'POST /analytics/dashboards/{dashboard_id}/refresh route')

    query = '''
        UPDATE Dashboard
        SET lastUpdated = CURRENT_TIMESTAMP
        WHERE dashboardID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (dashboard_id,))
    db.get_db().commit()

    return jsonify({'message': 'Dashboard refreshed successfully'}), 200


# ------------------------------------------------------------
# GET /analytics/competition-context - Get competition context data
# [Tukey-4]
@analytics.route('/analytics/competition-context', methods=['GET'])
def get_competition_context():
    """Return player performance data segmented by competition tier/level"""
    logger.info('GET /analytics/competition-context route')

    query = '''
        SELECT p.playerID, p.firstName, p.lastName,
               t.tier as competition_level,
               AVG(gs.points) as avg_points,
               AVG(gs.rebounds) as avg_rebounds,
               AVG(gs.assists) as avg_assists
        FROM Players p
        JOIN Playsin pin ON p.playerID = pin.playerID
        JOIN Team t ON pin.team_id = t.team_id
        JOIN Game_Stats gs ON p.playerID = gs.playerID
        GROUP BY p.playerID, p.firstName, p.lastName, t.tier
        ORDER BY t.tier DESC, avg_points DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    context_data = cursor.fetchall()

    return jsonify(context_data), 200


# ------------------------------------------------------------
# GET /analytics/competition-context/<player_id> - Get player context
# [Tukey-4]
@analytics.route('/analytics/competition-context/<int:player_id>', methods=['GET'])
def get_player_competition_context(player_id):
    """Return specific player's performance across different competition levels"""
    logger.info(f'GET /analytics/competition-context/{player_id} route')

    query = '''
        SELECT t.tier as competition_level,
               COUNT(gs.gameID) as games_played,
               AVG(gs.points) as avg_points,
               AVG(gs.rebounds) as avg_rebounds,
               AVG(gs.assists) as avg_assists,
               AVG(gs.steals) as avg_steals
        FROM Game_Stats gs
        JOIN Game g ON gs.gameID = g.gameID
        JOIN Players p ON gs.playerID = p.playerID
        JOIN Playsin pin ON p.playerID = pin.playerID
        JOIN Team t ON pin.team_id = t.team_id
        WHERE p.playerID = %s
        GROUP BY t.tier
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (player_id,))
    context = cursor.fetchall()

    return jsonify(context), 200


# ------------------------------------------------------------
# GET /analytics/validation/flagged - Get flagged data
# [Tukey-6]
@analytics.route('/analytics/validation/flagged', methods=['GET'])
def get_flagged_data():
    """Return list of data entries flagged for review"""
    logger.info('GET /analytics/validation/flagged route')

    query = '''
        SELECT validationID, entityType, entityID, 
               fieldName, errorMessage, validatedDate
        FROM Validation
        WHERE isValid = FALSE
        ORDER BY validatedDate DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    flagged = cursor.fetchall()

    return jsonify(flagged), 200


# ------------------------------------------------------------
# GET /players/stats/aggregate - Get aggregated player stats
# [Tukey-1], [Tukey-4]
@analytics.route('/players/stats/aggregate', methods=['GET'])
def get_aggregate_player_stats():
    """Return full list of player statistics with filtering"""
    logger.info('GET /players/stats/aggregate route')

    # Get query parameters
    position = request.args.get('position')
    min_points = request.args.get('min_points', 0)

    query = '''
        SELECT p.playerID, p.firstName, p.lastName,
               pin.position, t.team_name,
               AVG(gs.points) as avg_points,
               AVG(gs.rebounds) as avg_rebounds,
               AVG(gs.assists) as avg_assists,
               COUNT(gs.gameID) as games_played
        FROM Players p
        JOIN Playsin pin ON p.playerID = pin.playerID
        JOIN Team t ON pin.team_id = t.team_id
        JOIN Game_Stats gs ON p.playerID = gs.playerID
        WHERE 1=1
    '''

    params = []

    if position:
        query += ' AND pin.position = %s'
        params.append(position)

    query += '''
        GROUP BY p.playerID, p.firstName, p.lastName, pin.position, t.team_name
        HAVING AVG(gs.points) >= %s
        ORDER BY avg_points DESC
    '''
    params.append(min_points)

    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))
    stats = cursor.fetchall()

    return jsonify(stats), 200


# ------------------------------------------------------------
# GET /analytics/calculated-metrics - Get all calculated metrics
# [Tukey-1], [Tukey-3]
@analytics.route('/analytics/calculated-metrics', methods=['GET'])
def get_calculated_metrics():
    """Return all calculated metric results with timestamps and associated games/players"""
    logger.info('GET /analytics/calculated-metrics route')

    query = '''
        SELECT cm.metricID, cm.gameID, cm.playerID, cm.formulaID,
               cm.metricName, cm.calcTimestamp,
               p.firstName, p.lastName,
               mf.formulaName
        FROM CalculatedMetrics cm
        LEFT JOIN Players p ON cm.playerID = p.playerID
        JOIN MetricsFormulas mf ON cm.formulaID = mf.formulaID
        ORDER BY cm.calcTimestamp DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    metrics = cursor.fetchall()

    return jsonify(metrics), 200


# ------------------------------------------------------------
# DELETE /analytics/calculated-metrics - Remove outdated metrics
# [Tukey-2]
@analytics.route('/analytics/calculated-metrics/<int:metric_id>', methods=['DELETE'])
def delete_calculated_metric(metric_id):
    """Remove outdated calculated metrics"""
    logger.info(f'DELETE /analytics/calculated-metrics/{metric_id} route')

    cursor = db.get_db().cursor()
    query = 'DELETE FROM CalculatedMetrics WHERE metricID = %s'
    cursor.execute(query, (metric_id,))
    db.get_db().commit()

    return jsonify({'message': 'Calculated metric deleted successfully'}), 200


# ------------------------------------------------------------
# GET /analytics/export-requests - Get all export requests
# [Tukey-5]
@analytics.route('/analytics/export-requests', methods=['GET'])
def get_export_requests():
    """Return list of data export requests with status and download links"""
    logger.info('GET /analytics/export-requests route')

    query = '''
        SELECT er.exportID, er.requestedBy, er.requestedUserType,
               er.format, er.dataType, er.timestamp, er.status, er.completedAt,
               sa.firstName as admin_firstName, sa.lastName as admin_lastName
        FROM ExportRequest er
        LEFT JOIN SystemAdmin sa ON er.requestedBy = sa.adminID
        ORDER BY er.timestamp DESC
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    requests_list = cursor.fetchall()

    return jsonify(requests_list), 200


# ------------------------------------------------------------
# GET /analytics/export-requests/{exportID} - Get specific export
# [Tukey-5]
@analytics.route('/analytics/export-requests/<int:export_id>', methods=['GET'])
def get_export_request_detail(export_id):
    """Return specific export file details and download link"""
    logger.info(f'GET /analytics/export-requests/{export_id} route')

    query = '''
        SELECT er.exportID, er.requestedBy, er.requestedUserType,
               er.format, er.dataType, er.timestamp, er.status, er.completedAt,
               e.fileName, e.filePath, e.fileSize, e.downloadCount
        FROM ExportRequest er
        LEFT JOIN Exports e ON er.exportID = e.exportRequestID
        WHERE er.exportID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (export_id,))
    export_detail = cursor.fetchone()

    if not export_detail:
        return jsonify({'error': 'Export request not found'}), 404

    return jsonify(export_detail), 200