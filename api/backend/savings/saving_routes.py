from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

savings = Blueprint('savings', __name__)

# Get all savings for a user
@savings.route('/user/<int:user_id>', methods=['GET'])
def get_user_savings(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT savingID, goalName, targAmt, currAmt, targetDeadline, monthlyContribution, userID
        FROM Saving
        WHERE userID = %s
        ORDER BY targetDeadline ASC
    ''', (user_id,))
    
    savings_list = cursor.fetchall()
    cursor.close()
    
    return jsonify(savings_list), 200

# Get a specific saving
@savings.route('/<int:saving_id>', methods=['GET'])
def get_saving(saving_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT savingID, goalName, targAmt, currAmt, targetDeadline, monthlyContribution, userID
        FROM Saving
        WHERE savingID = %s
    ''', (saving_id,))
    
    saving = cursor.fetchone()
    cursor.close()
    
    if saving:
        return jsonify(saving), 200
    return jsonify({"error": "Saving not found"}), 404

# Create a new saving goal
@savings.route('/', methods=['POST'])
def create_saving():
    data = request.json
    
    goal_name = data.get('goalName')
    targ_amt = data.get('targAmt')
    curr_amt = data.get('currAmt', 0)
    target_deadline = data.get('targetDeadline')
    monthly_contribution = data.get('monthlyContribution', 0)
    user_id = data.get('userID')
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        INSERT INTO Saving (goalName, targAmt, currAmt, targetDeadline, monthlyContribution, userID)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (goal_name, targ_amt, curr_amt, target_deadline, monthly_contribution, user_id))
    
    db.get_db().commit()
    new_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({"savingID": new_id, "message": "Saving goal created"}), 201

# Update a saving goal
@savings.route('/<int:saving_id>', methods=['PUT'])
def update_saving(saving_id):
    data = request.json
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        UPDATE Saving
        SET goalName = %s, targAmt = %s, currAmt = %s, targetDeadline = %s, monthlyContribution = %s
        WHERE savingID = %s
    ''', (data.get('goalName'), data.get('targAmt'), data.get('currAmt'), 
          data.get('targetDeadline'), data.get('monthlyContribution'), saving_id))
    
    db.get_db().commit()
    cursor.close()
    
    return jsonify({"message": "Saving goal updated"}), 200

# Add money to a saving goal
@savings.route('/<int:saving_id>/add', methods=['PUT'])
def add_to_saving(saving_id):
    data = request.json
    amount = data.get('amount', 0)
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        UPDATE Saving 
        SET currAmt = currAmt + %s 
        WHERE savingID = %s
    ''', (amount, saving_id))
    db.get_db().commit()
    cursor.close()
    
    return jsonify({"message": "Amount added successfully"}), 200

# Remove money from a saving goal
@savings.route('/<int:saving_id>/remove', methods=['PUT'])
def remove_from_saving(saving_id):
    data = request.json
    amount = data.get('amount', 0)
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        UPDATE Saving 
        SET currAmt = GREATEST(currAmt - %s, 0)
        WHERE savingID = %s
    ''', (amount, saving_id))
    db.get_db().commit()
    cursor.close()
    
    return jsonify({"message": "Amount removed successfully"}), 200

# Delete a saving goal
@savings.route('/<int:saving_id>', methods=['DELETE'])
def delete_saving(saving_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Saving WHERE savingID = %s', (saving_id,))
    db.get_db().commit()
    cursor.close()
    
    return jsonify({"message": "Saving goal deleted"}), 200