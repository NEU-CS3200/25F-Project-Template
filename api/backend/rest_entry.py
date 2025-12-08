from flask import Flask
from backend.db_connection import db

from .system_admin.admin_routes import system_admin
from .health_analyst.health_analyst_routes import health_analyst
from .trainer.trainer_routes_client_logs import trainer_logs
from .trainer.trainer_routes_client_program import trainer_programs
from .trainer.trainer_routes_feedback import trainer_feedback
from .trainer.trainer_routes_workout_specific_exercise import trainer_workout_exercises
from .trainer.trainer_routes_workout_template import trainer_templates
from .client.client_routes import client

import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# comment
    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('create_app(): registering blueprints with Flask app object.')
    app.register_blueprint(system_admin, url_prefix="/system_admin")
    app.register_blueprint(health_analyst, url_prefix="/health_analyst")
    app.register_blueprint(trainer_logs, url_prefix="/trainer_logs")
    app.register_blueprint(trainer_programs, url_prefix="/trainer_programs")
    app.register_blueprint(trainer_feedback, url_prefix="/trainer_feedback")
    app.register_blueprint(trainer_templates, url_prefix="/trainer_templates")
    app.register_blueprint(trainer_workout_exercises, url_prefix="/trainer_workout_excs")
    app.register_blueprint(client, url_prefix="/client")

    # Don't forget to return the app object
    return app
