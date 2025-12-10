from flask import Blueprint, request, jsonify
from backend.db_connection import db

budgets = Blueprint('budgets', __name__)

# Get budget totals for dashboard
@budgets.route('/user/<int:user_id>/totals', methods=['GET'])
def get_user_totals(user_id):
    cursor = db.get_db().cursor()
    
    # Get total income
    cursor.execute('''
        SELECT COALESCE(SUM(t.amount), 0) as total
        FROM Transaction t
        JOIN Account a ON t.accountID = a.acctID
        WHERE a.userID = %s AND t.amount > 0
    ''', (user_id,))
    income = float(cursor.fetchone()['total'])
    
    # Get total expenses
    cursor.execute('''
        SELECT COALESCE(ABS(SUM(t.amount)), 0) as total
        FROM Transaction t
        JOIN Account a ON t.accountID = a.acctID
        WHERE a.userID = %s AND t.amount < 0
    ''', (user_id,))
    expenditures = float(cursor.fetchone()['total'])
    
    # Get total savings
    cursor.execute('''
        SELECT COALESCE(SUM(currAmt), 0) as total
        FROM Saving
        WHERE userID = %s
    ''', (user_id,))
    savings = float(cursor.fetchone()['total'])
    
    # Get total budget limit
    cursor.execute('''
        SELECT COALESCE(limitAmount, 0) as total
        FROM Budget
        WHERE userID = %s AND budgetType = 'total'
    ''', (user_id,))
    result = cursor.fetchone()
    total_budget = float(result['total']) if result else 0
    
    net_position = income - expenditures
    savings_rate = round((net_position / income) * 100, 1) if income > 0 else 0
    
    cursor.close()
    
    return jsonify({
        'income': income,
        'expenditures': expenditures,
        'savings': savings,
        'netPosition': net_position,
        'savingsRate': savings_rate,
        'totalBudget': total_budget
    }), 200

# Get spending by category with budget limits
@budgets.route('/user/<int:user_id>/categories', methods=['GET'])
def get_user_categories(user_id):
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT c.name as category, 
               COALESCE(ABS(SUM(t.amount)), 0) as spent,
               b.limitAmount as budgetLimit
        FROM Category c
        LEFT JOIN (
            SELECT t.categoryID, t.amount
            FROM Transaction t
            JOIN Account a ON t.accountID = a.acctID
            WHERE a.userID = %s AND t.amount < 0
        ) t ON c.categoryID = t.categoryID
        LEFT JOIN Budget b ON c.categoryID = b.categoryID AND b.userID = %s AND b.budgetType = 'category'
        WHERE c.isExpense = TRUE
        GROUP BY c.categoryID, c.name, b.limitAmount
        HAVING spent > 0
        ORDER BY spent DESC
    ''', (user_id, user_id))
    
    categories = cursor.fetchall()
    cursor.close()
    
    return jsonify(categories), 200

# Get all budgets for user
@budgets.route('/user/<int:user_id>', methods=['GET'])
def get_user_budgets(user_id):
    cursor = db.get_db().cursor()
    
    # Get total expenses for user (for total budget)
    cursor.execute('''
        SELECT COALESCE(ABS(SUM(t.amount)), 0) as total_spent
        FROM Transaction t
        JOIN Account a ON t.accountID = a.acctID
        WHERE a.userID = %s AND t.amount < 0
    ''', (user_id,))
    total_spent = float(cursor.fetchone()['total_spent'])
    
    # Get all budgets with their spent amounts
    cursor.execute('''
        SELECT b.budgetID, b.name, b.limitAmount, b.budgetType, b.categoryID,
               c.name as categoryName,
               COALESCE(ABS(SUM(t.amount)), 0) as spent
        FROM Budget b
        LEFT JOIN Category c ON b.categoryID = c.categoryID
        LEFT JOIN Transaction t ON b.budgetID = t.budgetID
        WHERE b.userID = %s
        GROUP BY b.budgetID, b.name, b.limitAmount, b.budgetType, b.categoryID, c.name
        ORDER BY b.budgetType, b.name
    ''', (user_id,))
    
    budgets_list = cursor.fetchall()
    
    # Override spent amount for total budget type
    result = []
    for budget in budgets_list:
        budget_dict = dict(budget)
        if budget_dict['budgetType'] == 'total':
            budget_dict['spent'] = total_spent
        result.append(budget_dict)
    
    cursor.close()
    
    return jsonify(result), 200

# Get budgets for dropdown (for transaction form)
@budgets.route('/user/<int:user_id>/list', methods=['GET'])
def get_user_budgets_list(user_id):
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT budgetID, name, budgetType
        FROM Budget
        WHERE userID = %s
        ORDER BY budgetType, name
    ''', (user_id,))
    
    budgets_list = cursor.fetchall()
    cursor.close()
    
    return jsonify(budgets_list), 200

# Create budget
@budgets.route('/', methods=['POST'])
def create_budget():
    data = request.json
    cursor = db.get_db().cursor()
    
    budget_type = data.get('budgetType', 'custom')
    category_id = data.get('categoryID')
    
    # Check if category budget already exists
    if budget_type == 'category' and category_id:
        cursor.execute('''
            SELECT budgetID FROM Budget 
            WHERE userID = %s AND categoryID = %s AND budgetType = 'category'
        ''', (data['userID'], category_id))
        existing = cursor.fetchone()
        if existing:
            # Update existing instead
            cursor.execute('''
                UPDATE Budget SET limitAmount = %s WHERE budgetID = %s
            ''', (data['limitAmount'], existing['budgetID']))
            db.get_db().commit()
            cursor.close()
            return jsonify({'message': 'Budget updated', 'budgetID': existing['budgetID']}), 200
    
    # Check if total budget already exists
    if budget_type == 'total':
        cursor.execute('''
            SELECT budgetID FROM Budget 
            WHERE userID = %s AND budgetType = 'total'
        ''', (data['userID'],))
        existing = cursor.fetchone()
        if existing:
            cursor.execute('''
                UPDATE Budget SET limitAmount = %s WHERE budgetID = %s
            ''', (data['limitAmount'], existing['budgetID']))
            db.get_db().commit()
            cursor.close()
            return jsonify({'message': 'Budget updated', 'budgetID': existing['budgetID']}), 200
    
    cursor.execute('''
        INSERT INTO Budget (name, limitAmount, budgetType, userID, categoryID)
        VALUES (%s, %s, %s, %s, %s)
    ''', (
        data['name'],
        data['limitAmount'],
        budget_type,
        data['userID'],
        category_id
    ))
    
    db.get_db().commit()
    new_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({'message': 'Budget created', 'budgetID': new_id}), 201

# Update budget
@budgets.route('/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    data = request.json
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        UPDATE Budget
        SET name = %s, limitAmount = %s
        WHERE budgetID = %s
    ''', (
        data['name'],
        data['limitAmount'],
        budget_id
    ))
    
    db.get_db().commit()
    cursor.close()
    
    return jsonify({'message': 'Budget updated'}), 200

# Delete budget
@budgets.route('/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    cursor = db.get_db().cursor()
    
    # Remove budget reference from transactions first
    cursor.execute('UPDATE Transaction SET budgetID = NULL WHERE budgetID = %s', (budget_id,))
    
    # Delete the budget
    cursor.execute('DELETE FROM Budget WHERE budgetID = %s', (budget_id,))
    db.get_db().commit()
    cursor.close()
    
    return jsonify({'message': 'Budget deleted'}), 200

# Get all categories
@budgets.route('/categories', methods=['GET'])
def get_categories():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT categoryID, name, description, isExpense FROM Category ORDER BY name')
    categories = cursor.fetchall()
    cursor.close()
    
    return jsonify(categories), 200

# Create new category
@budgets.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        INSERT INTO Category (name, description, isExpense)
        VALUES (%s, %s, %s)
    ''', (data['name'], data.get('description', ''), data.get('isExpense', True)))
    
    db.get_db().commit()
    new_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({'message': 'Category created', 'categoryID': new_id}), 201

# Delete category
@budgets.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Category WHERE categoryID = %s', (cat_id,))
    db.get_db().commit()
    cursor.close()
    
    return jsonify({'message': 'Category deleted'}), 200