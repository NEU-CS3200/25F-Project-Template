from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

taker = Blueprint('taker', __name__)

#-----User Story 1------
# As a Taker, I want to look through listings and take clothing pieces 
# without having to swap, so I can get second-hand clothes without having to give clothes up.

@taker.route('/listings/up_for_grabs', methods=['GET'])
def get_up_for_grabs_listings():
    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            i.ItemID, i.Title, i.Category, i.Description, i.Size, i.Condition, u.Name as OwnerName,
            GROUP_CONCAT(t.Title SEPARATOR ', ') as Tags,
            i.ListedAt
        FROM Items i
        JOIN Users u ON i.OwnerID = u.UserID
        LEFT JOIN ItemTags it ON i.ItemID = it.ItemID
        LEFT JOIN Tags t ON it.TagID = t.TagID
        WHERE i.IsAvailable = 1
        GROUP BY i.ItemID, i.Title, i.Category, i.Description, i.Size, i.Condition, u.Name, i.ListedAt
        ORDER BY i.ListedAt DESC;
    '''

    cursor.execute(the_query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData), 200)
    the_response.mimetype = "application/json"
    return the_response
#-----User Story 1------


#-----User Story 2------
# As a Taker, I want to see listing that are labeled as up for grabs 
# and filter by size, condition, and tags, so I can find items that suit me

@taker.route('/listings/filter', methods=['GET'])
def get_filter_listings():
    size = request.args.get('size')
    condition = request.args.get('condition')
    tags = request.args.get('tags')

    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            i.itemID, i.title, i.category, i.description, i.size, i.condition, u.name as ownerName,
            GROUP_CONCAT(t.Title SEPARATOR ', ') as Tags,
            i.ListedAt
        FROM Items i
        JOIN Users u ON i.OwnerID = u.UserID
        LEFT JOIN ItemTags it ON i.ItemID = it.ItemID
        LEFT JOIN Tags t ON it.TagID = t.TagID
        WHERE i.IsAvailable = 1
    '''

    query_params = []

    if size:
        the_query += ' AND i.size = %s'
        query_params.append(size)

    if condition:
        conditions = condition.split(',')
        placeholders = ', '.join(['%s'] * len(conditions))
        the_query += f' AND i.condition IN ({placeholders})'
        query_params.extend(conditions)

    if tags:
        tag_list = tags.split(',')
        placeholders = ', '.join(['%s'] * len(tag_list))
        the_query += f' AND (t.Title IN ({placeholders}) OR t.Title IS NULL)'
        query_params.extend(tag_list)

    the_query += '''
        GROUP BY i.itemID, i.title, i.category, i.description, i.size, i.Condition, u.name, i.ListedAt
        ORDER BY i.ListedAt DESC;
    '''

    cursor.execute(the_query, query_params)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData), 200)
    the_response.mimetype = "application/json"
    return the_response
#-----User Story 2------


#-----User Story 3------
# As a Taker, I want to be able to cancel take requests that I changed my mind on.

@taker.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_take_request(order_id):
    user_id = request.args.get('user_id')

    cursor = db.get_db().cursor()

    delete_query = '''
        DELETE FROM OrderItems
        WHERE OrderID = %s
          AND OrderID IN (
              SELECT OrderID
              FROM Orders
              WHERE ReceiverID = %s
                AND ShippingID IS NULL
          );
    '''

    cursor.execute(delete_query, (order_id, user_id))
    rows_affected = cursor.rowcount
    db.get_db().commit()

    if rows_affected > 0:
        the_response = make_response(jsonify({"message": "Take request canceled successfully."}), 200)
    else:
        the_response = make_response(jsonify({"message": "No matching take request found."}), 404)

    the_response.mimetype = "application/json"
    return the_response
#-----User Story 3------


#-----User Story 4------
# As a taker, I want to receive notifications when a new item that matches 
# my order history styles and sizes is posted as a 'take', 
# so I can quickly request popular items

@taker.route('/recommendations/<int:taker_id>', methods=['GET'])
def get_recommendations(taker_id):
    size = request.args.get('size', default='M', type=str)
    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            i.ItemID, i.Title, i.Category, i.Size, u.Name as OwnerName
        FROM Items i
        JOIN Users u ON i.OwnerID = u.UserID
        WHERE i.IsAvailable = 1
          AND i.ListedAt >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
          AND i.Size = %s
        ORDER BY i.ListedAt DESC;
    '''

    cursor.execute(the_query, (size,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData), 200)
    the_response.mimetype = "application/json"
    return the_response
#-----User Story 4------


#-----User Story 5------
# As a taker, I want to be able to track the status of my incoming package

@taker.route('/track_package/<int:user_id>', methods=['GET'])
def track_package(user_id):
    cursor = db.get_db().cursor()

    the_query = '''
        SELECT
            o.OrderID, i.Title, o.CreatedAt as RequestDate, s.Carrier, s.TrackingNum, s.DateShipped, s.DateArrived
        FROM Orders o
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        JOIN Items i ON oi.ItemID = i.ItemID
        LEFT JOIN Shippings s ON o.ShippingID = s.ShippingID
        WHERE o.ReceiverID = %s
        ORDER BY o.CreatedAt DESC;
    '''

    cursor.execute(the_query, (user_id,))
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData), 200)
    the_response.mimetype = "application/json"
    return the_response
#-----User Story 5------