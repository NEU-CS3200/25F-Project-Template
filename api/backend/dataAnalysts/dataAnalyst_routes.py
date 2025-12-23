########
# Data Analyst endpoints
########


from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
dataAnalyst = Blueprint('dataAnalysts', __name__)


#-----User Story 1------
#As a Senior Data Analyst, I want to view available listings with
# their posting dates, so I can monitor listing performance.

@dataAnalyst.route('/listings', methods=['GET'])
def get_all_listings():
    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            ItemID,
            ListedAt,
            COUNT(*) OVER () AS TotalAvailable
        FROM Items
        WHERE IsAvailable = 1;
    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
#-----User Story 1------



#-----User Story 2------
#As a Senior Data Analyst, I want to see user counts by age and gender,
# so I can identify growth opportunities.

@dataAnalyst.route('/users/<gender>/<int:agemin>/<int:agemax>', methods=['GET'])
def get_all_users_by_age_and_gender(gender, agemin, agemax):
    cursor = db.get_db().cursor()

    the_query = '''
    SELECT
       UserID,
       Gender,
       DATE_FORMAT(FROM_DAYS(DATEDIFF(CURDATE(), DOB)), '%%Y') + 0 AS Age
    FROM Users
    WHERE Gender = %s
      AND (DATE_FORMAT(FROM_DAYS(DATEDIFF(CURDATE(), DOB)), '%%Y') + 0)
          BETWEEN %s AND %s;
'''

    cursor.execute(the_query, (gender, agemin, agemax))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#-----User Story 2------



#-----User Story 3------
#As a Senior Data Analyst, I want to count how many listings are in each
# category(pants, shirts, tanks) so I can find what users need more of.

@dataAnalyst.route('/listings/category', methods=['GET'])
def get_listings_category():
    cursor = db.get_db().cursor()
    the_query = '''
        SELECT
            Category,
            COUNT(ItemID) AS AvailableListings
        FROM Items
        WHERE IsAvailable = 1
        GROUP BY Category;
    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
#-----User Story 3------


#-----User Story 4------
#As a Senior Data Analyst, I want to track swaps and takes per user, so I can measure engagement.

@dataAnalyst.route('/users/countorders', methods=['GET'])
def get_orders_per_users():
    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            u.UserID,
            COUNT(o_received.OrderID) AS OrdersReceived,
            COUNT(o_given.OrderID) AS OrdersGiven
        FROM Users u
        LEFT JOIN Orders o_received
               ON u.UserID = o_received.ReceiverID
        LEFT JOIN Orders o_given
               ON u.UserID = o_given.GivenByID
        GROUP BY u.UserID;
    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
#-----User Story 4------



#-----User Story 5------
#As a Senior Data Analyst, I want to see shipments with above-average
# delivery times (excluding those still in transit), so I can flag carriers who have a pattern of delays.

@dataAnalyst.route('/shipments/delay', methods=['GET'])
def get_shipments_delay():
    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            s.ShippingID,
            s.DateShipped,
            s.DateArrived,
            DATEDIFF(s.DateArrived, s.DateShipped) AS DeliveryTime
        FROM Shippings s
        WHERE s.DateArrived IS NOT NULL
          AND DATEDIFF(s.DateArrived, s.DateShipped) > (
                SELECT AVG(DATEDIFF(DateArrived, DateShipped))
                FROM Shippings
                WHERE DateArrived IS NOT NULL
          );
    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
#-----User Story 5------
