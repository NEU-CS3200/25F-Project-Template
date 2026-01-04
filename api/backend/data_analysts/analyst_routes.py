from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for analysts routes 
analysts = Blueprint("analysts", __name__)

# list of dashboard with names, metrics displayed, and last updated timestamp
@analysts.route('/dashboards', methods=['GET'])
def get_all_dashboards():
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("""
            SELECT 
                dashboardID,
                dashboardName,
                metricDisplayed,
                lastUpdated,
                chartType,
                recommendation
            FROM Dashboard
            ORDER BY lastUpdated DESC
        """)
        
        dashboards = cursor.fetchall()
        cursor.close()
        
        # Format the response
        dashboard_list = []
        for dashboard in dashboards:
            dashboard_list.append({
                'dashboardID': dashboard[0],
                'dashboardName': dashboard[1],
                'metricDisplayed': dashboard[2],
                'lastUpdated': dashboard[3].strftime('%Y-%m-%d %H:%M:%S') if dashboard[3] else None,
                'chartType': dashboard[4],
                'recommendation': dashboard[5]
            })
        
        return jsonify({
            'success': True,
            'count': len(dashboard_list),
            'dashboards': dashboard_list
        }), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500

# removing a dashboard 
@analysts.route('/dashboards/<int:dashboardID>/remove', methods=['DELETE'])
def remove_dashboard(dashboardID):
    try:
        cursor = db.get_db().cursor()
        
        # Check if dashboard exists
        cursor.execute("SELECT dashboardName FROM Dashboard WHERE dashboardID = %s", (dashboardID,))
        dashboard = cursor.fetchone()
        
        if not dashboard:
            cursor.close()
            return jsonify({"error": "Dashboard not found"}), 404
        
        dashboard_name = dashboard[0]
        
        # Delete dashboard (cascades to DashboardMetrics due to FK constraints)
        cursor.execute("DELETE FROM Dashboard WHERE dashboardID = %s", (dashboardID,))
        
        # Log the deletion
        cursor.execute("""
            INSERT INTO Reports (adminID, repStatus, userReported, date)
            VALUES (%s, 'completed', %s, NOW())
        """, (3, f"Deleted dashboard: {dashboard_name} (ID: {dashboardID})"))
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({
            "success": True,
            "message": f"Dashboard '{dashboard_name}' has been removed"
        }), 200
        
    except Error as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# returns export details with download URL
@analysts.route('/exports/<int:exportID>', methods=['GET'])
def get_export_details(exportID):
    try:
        cursor = db.get_db().cursor()
        
        # Get basic export info
        cursor.execute("""
            SELECT exportID, format, timestamp, player
            FROM ExportRequests 
            WHERE exportID = %s
        """, (exportID,))
        
        export_info = cursor.fetchone()
        cursor.close()
        
        if not export_info:
            return jsonify({"error": "Export not found"}), 404
        
        # Simple formatted response with just download URL
        return jsonify({
            "exportID": export_info[0],
            "format": export_info[1],
            "downloadURL": f"http://localhost:4000/analysts/exports/{exportID}/download"
        }), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500

# list of data export requets
@analysts.route('/export-requests', methods=['GET'])
def get_export_requests():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT 
                exportID,
                format,
                timestamp,
                player
            FROM ExportRequests
            ORDER BY timestamp DESC
        """)
        export_requests = cursor.fetchall()
        cursor.close()
        
        export_list = []
        for row in export_requests:
            export_list.append({
                'exportID': row[0],
                'format': row[1],
                'timestamp': row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else None,
                'player': row[3]
            })
        
        return jsonify(export_list), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500

# get dashboard metrics 
@analysts.route('/dashboard-metrics', methods=['GET'])
def get_dashboard_metrics():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT 
                metricID,
                dashboardID
            FROM DashboardMetrics
            ORDER BY dashboardID, metricID
        """)
        
        metrics = cursor.fetchall()
        cursor.close()
        
        metrics_list = []
        for row in metrics:
            metrics_list.append({
                'metricID': row[0],
                'dashboardID': row[1]
            })
        
        return jsonify(metrics_list), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500