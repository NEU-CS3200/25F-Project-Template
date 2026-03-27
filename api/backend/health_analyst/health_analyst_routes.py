from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

health_analyst = Blueprint("health_analyst", __name__)

# --------------------------------------------------------------------------------
# 3.1 Average Workout Duration (Completed Workouts Only)
# --------------------------------------------------------------------------------
@health_analyst.route("/avg_duration", methods=["GET"])
def get_average_workout_duration():
    try:
        query = """
            SELECT
              c.client_id,
              YEAR(cwl.date) AS year,
              WEEK(cwl.date, 1) AS week,
              AVG(cwl.duration_minutes) AS avg_duration
            FROM Client c JOIN Client_Workout_Log cwl ON c.client_id = cwl.client_id
            WHERE cwl.completion_status = 'completed'
            GROUP BY c.client_id, YEAR(cwl.date), WEEK(cwl.date, 1)
            ORDER BY c.client_id, year, week;
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return jsonify(data), 200

    except Error as e:
        current_app.logger.error(f"Error in avg_duration: {str(e)}")
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------------------------------
# 3.2 Client Demographic Information
# --------------------------------------------------------------------------------
@health_analyst.route("/client_info", methods=["GET"])
def get_client_info():
    try:
        query = """
            SELECT
             c.client_id,
             c.first_name,
             c.last_name,
             c.date_of_birth,
             c.Goals,
             c.fitness_level,
             c.Age,
             c.join_date
            FROM Client c;
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return jsonify(data), 200

    except Error as e:
        current_app.logger.error(f"Error in client_info: {str(e)}")
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------------------------------
# 3.3 Most Recent Health Metrics Per Client
# --------------------------------------------------------------------------------
@health_analyst.route("/recent_metrics", methods=["GET"])
def get_recent_health_metrics():
    try:
        query = """
            SELECT
              hm.client_id,
              hm.record_date,
              hm.weight_kg,
              hm.body_fat_percentage,
              hm.heart_rate
            FROM Health_Metrics hm
            WHERE hm.record_date = (
              SELECT MAX(record_date)
              FROM Health_Metrics
              WHERE client_id = hm.client_id
            );
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return jsonify(data), 200

    except Error as e:
        current_app.logger.error(f"Error in recent_metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------------------------------
# 3.4 Health Progression (Weight + Body Fat by Month)
# --------------------------------------------------------------------------------
@health_analyst.route("/health_progression", methods=["GET"])
def get_health_progression():
    try:
        query = """
            SELECT
             client_id,
             MONTH(hm.record_date) AS month,
             AVG(weight_kg),
             AVG(body_fat_percentage)
            FROM Health_Metrics hm
            GROUP BY client_id, MONTH(hm.record_date)
            ORDER BY client_id, month;
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return jsonify(data), 200

    except Error as e:
        current_app.logger.error(f"Error in health_progression: {str(e)}")
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------------------------------
# 3.5 Workout Program Completion Rates
# --------------------------------------------------------------------------------
@health_analyst.route("/completion_rates", methods=["GET"])
def get_program_completion_rates():
    try:
        query = """
            SELECT
              cswp.program_id,
              cswp.name AS program_name,
              COUNT(cwl.log_id) AS total_workouts,
              SUM(cwl.completion_status = 'completed') AS completed_workouts,
              ROUND(
                  SUM(cwl.completion_status = 'completed') / COUNT(cwl.log_id),
                  3
              ) AS completion_rate
            FROM Client_Specific_Workout_Program cswp JOIN Client_Workout_Log cwl
              ON cswp.workout_id = cwl.workout_id
              AND cswp.client_id = cwl.client_id
            GROUP BY cswp.program_id, cswp.name
            ORDER BY completion_rate DESC;
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return jsonify(data), 200

    except Error as e:
        current_app.logger.error(f"Error in completion_rates: {str(e)}")
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------------------------------
# 3.6 Workout Template Usage Frequency
# --------------------------------------------------------------------------------
@health_analyst.route("/template_usage", methods=["GET"])
def get_workout_template_usage():
    try:
        query = """
            SELECT
              cwl.workout_id,
              wst.name,
              COUNT(*) AS used
            FROM Client_Workout_Log cwl JOIN Workout_Session_Template wst
              ON cwl.workout_id = wst.workout_id
            GROUP BY cwl.workout_id, wst.name
            ORDER BY used DESC;
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return jsonify(data), 200

    except Error as e:
        current_app.logger.error(f"Error in template_usage: {str(e)}")
        return jsonify({"error": str(e)}), 500
