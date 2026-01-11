########
# swapper endpoints
########


from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
swapper = Blueprint('swappers', __name__)


#-----User Story 1------
#As a Senior Data Analyst, I want to view available listings with
# their posting dates, so I can monitor listing performance.

@swapper.route('/listings/<SizeFilter>/<ConditionFilter>/<TagFilter>/', methods=['GET'])
def get_all_listings():
    cursor = db.get_db().cursor()

    the_query = '''
        SET @SizeFilter = 'M';
        SET @ConditionFilter = 'Good';
        SET @TagFilter = 'Vintage';


        SELECT DISTINCT i.ItemID, i.Title, i.Category, i.Description, i.Size, i.`Condition`, i.`Type`, u.Name AS OwnerName
        FROM Items i
        INNER JOIN Users u ON i.OwnerID = u.UserID
        LEFT JOIN ItemTags it ON i.ItemID = it.ItemID
        LEFT JOIN Tags t ON it.TagID = t.TagID
        WHERE i.IsAvailable = 1
            AND i.`Type` = 'Swap'
            AND i.Size = @SizeFilter
            AND i.`Condition` = @ConditionFilter
            AND t.Title = @TagFilter;

    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
#-----User Story 1------
