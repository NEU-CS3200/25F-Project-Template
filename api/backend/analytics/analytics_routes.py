from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

analytics = Blueprint("analytics", __name__)

# Get all majors
# Streamlit: Use requests.get('http://web-api:4000/majors')
#            Display list of majors for filtering or analysis
@analytics.route("/majors", methods=["GET"])
def get_all_majors():
    try:
        current_app.logger.info('Starting get_all_majors request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM major")
        majors = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(majors)} majors')
        return jsonify(majors), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_majors: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get all companies
# Streamlit: Use requests.get('http://web-api:4000/companies')
#            Display list of companies for analysis
@analytics.route("/companies", methods=["GET"])
def get_all_companies():
    try:
        current_app.logger.info('Starting get_all_companies request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM company")
        companies = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(companies)} companies')
        return jsonify(companies), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_companies: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get locations with student/alumni counts
# Streamlit: Use requests.get('http://web-api:4000/locations')
#            Display geographic distribution with counts
#            Create map visualization
@analytics.route("/locations", methods=["GET"])
def get_all_locations():
    try:
        current_app.logger.info('Starting get_all_locations request')
        cursor = db.get_db().cursor()
        
        query = """
            SELECT 
                l.location_id,
                l.city,
                l.state,
                l.country,
                COUNT(DISTINCT s.student_id) as student_count,
                COUNT(DISTINCT a.alumni_id) as alumni_count,
                COUNT(DISTINCT s.student_id) + COUNT(DISTINCT a.alumni_id) as total_count
            FROM location l
            LEFT JOIN student s ON l.location_id = s.location_id
            LEFT JOIN alumni a ON l.location_id = a.location_id
            GROUP BY l.location_id, l.city, l.state, l.country
        """
        
        cursor.execute(query)
        locations = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(locations)} locations')
        return jsonify(locations), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_locations: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get match rates and connection statistics
# Streamlit: Use requests.get('http://web-api:4000/analytics/matches')
#            Display connection success rates, average time to match, etc.
#            Create charts showing trends
@analytics.route("/analytics/matches", methods=["GET"])
def get_match_statistics():
    try:
        current_app.logger.info('Starting get_match_statistics request')
        cursor = db.get_db().cursor()
        
        stats = {}
        
        # Total connections
        cursor.execute("SELECT COUNT(*) as count FROM connection")
        stats['total_connections'] = cursor.fetchone()['count']
        
        # Accepted connections
        cursor.execute("SELECT COUNT(*) as count FROM connection WHERE status = 'accepted'")
        stats['accepted_connections'] = cursor.fetchone()['count']
        
        # Pending connections
        cursor.execute("SELECT COUNT(*) as count FROM connection WHERE status = 'pending'")
        stats['pending_connections'] = cursor.fetchone()['count']
        
        # Calculate acceptance rate
        if stats['total_connections'] > 0:
            stats['acceptance_rate'] = (stats['accepted_connections'] / stats['total_connections']) * 100
        else:
            stats['acceptance_rate'] = 0
        
        # Total sessions completed
        cursor.execute("SELECT COUNT(*) as count FROM session WHERE status = 'completed'")
        stats['completed_sessions'] = cursor.fetchone()['count']
        
        # Average sessions per connection
        if stats['accepted_connections'] > 0:
            stats['avg_sessions_per_connection'] = stats['completed_sessions'] / stats['accepted_connections']
        else:
            stats['avg_sessions_per_connection'] = 0
        
        # Connections by major
        cursor.execute("""
            SELECT m.major_name, COUNT(c.connection_id) as connection_count
            FROM major m
            LEFT JOIN student s ON m.major_id = s.major_id
            LEFT JOIN connection c ON s.student_id = c.student_id
            GROUP BY m.major_id, m.major_name
            ORDER BY connection_count DESC
        """)
        stats['connections_by_major'] = cursor.fetchall()
        
        cursor.close()
        
        return jsonify(stats), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_match_statistics: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get top mentors (alumni ranked by mentorship activity)
# Streamlit: Use requests.get('http://web-api:4000/analytics/top-mentors')
#            Display leaderboard of most active mentors
#            Show recognition for top contributors
@analytics.route("/analytics/top-mentors", methods=["GET"])
def get_top_mentors():
    try:
        current_app.logger.info('Starting get_top_mentors request')
        cursor = db.get_db().cursor()
        
        # Get optional limit parameter
        limit = request.args.get("limit", 10)
        
        query = """
            SELECT 
                a.alumni_id,
                a.name,
                a.email,
                a.current_role,
                a.field,
                COUNT(DISTINCT c.connection_id) as total_connections,
                COUNT(DISTINCT s.session_id) as total_sessions,
                COUNT(DISTINCT CASE WHEN s.status = 'completed' THEN s.session_id END) as completed_sessions
            FROM alumni a
            LEFT JOIN connection c ON a.alumni_id = c.alumni_id AND c.status = 'accepted'
            LEFT JOIN session s ON a.alumni_id = s.alumni_id
            GROUP BY a.alumni_id, a.name, a.email, a.current_role, a.field
            HAVING total_connections > 0 OR total_sessions > 0
            ORDER BY completed_sessions DESC, total_connections DESC
            LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        top_mentors = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(top_mentors)} top mentors')
        return jsonify(top_mentors), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_top_mentors: {str(e)}')
        return jsonify({"error": str(e)}), 500