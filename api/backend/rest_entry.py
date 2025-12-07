from flask import Flask
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

from backend.db_connection import db
# Import all your NU Connect blueprints
from backend.students.student_routes import students
from backend.alumni.alumni_routes import alumni
from backend.connections.connection_routes import connections
from backend.sessions.session_routes import sessions
from backend.applications.application_routes import applications
from backend.admin.admin_routes import admin
from backend.analytics.analytics_routes import analytics
from backend.job_postings.job_posting_routes import job_postings

def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    # Load environment variables
    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME").strip()

    # Initialize the database object with the settings above.
    app.logger.info("current_app(): starting the database connection")
    db.init_app(app)

    # Register all NU Connect blueprints
    app.logger.info("create_app(): registering blueprints with Flask app object.")
    app.register_blueprint(students)
    app.register_blueprint(alumni)
    app.register_blueprint(connections)
    app.register_blueprint(sessions)
    app.register_blueprint(applications)
    app.register_blueprint(admin)
    app.register_blueprint(analytics)
    app.register_blueprint(job_postings)

    # Don't forget to return the app object
    return app

def setup_logging(app):
    """
    Configure logging for the Flask application in both files and console (Docker Desktop for this project)
    
    Args:
        app: Flask application instance to configure logging for
    """
    pass