from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for requirements routes
requirements = Blueprint('requirements', __name__)


# GET /courses
# Return list of all reuirements needed
@requirements.route("/requirements", methods=["GET"])
def get_requirements():

    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            requirementID,
            creditsNeeded,
            requirementType,
            corequisites,
            prerequisites
        FROM Requirements
        WHERE requirementID = %s;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    cursor.close()
    
    return jsonify(theData)
